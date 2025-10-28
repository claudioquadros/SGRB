from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin  # noqa
from django.views.generic import ListView, FormView, TemplateView
from django.db.models import Subquery, OuterRef, Case, When, IntegerField, Value, Q, BooleanField  # noqa
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import AppSettingsForm
from django.http import HttpResponse
from .config import get_int, load_config, save_config
from animals.models import Animal
from inseminations.models import Insemination
from births.models import Birth
from farms.models import Farm


class AnimalOverviewListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):  # noqa
    model = Animal
    template_name = "animal_overview.html"
    context_object_name = "animals"
    paginate_by = 10
    permission_required = 'animals.view_animal'

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.select_related("category")
        # Somente fêmeas reprodutivas na visão geral
        queryset = queryset.filter(category__is_reproductive_female=True)

        last_insemination = Insemination.objects.filter(
            animal=OuterRef('pk')
        ).order_by('-date_of_insemination')

        queryset = queryset.annotate(
            ultima_inseminacao_id=Subquery(last_insemination.values('id')[:1]),
            ultima_inseminacao=Subquery(last_insemination.values('date_of_insemination')[:1]),  # noqa
            touro=Subquery(last_insemination.values('bull')[:1]),  # noqa
            prenhez_verificacao=Subquery(last_insemination.values('expected_pregnancy')[:1]),  # noqa
            prenhez_verificada=Subquery(last_insemination.values('pregnancy_check')[:1]),  # noqa
            esta_prenha=Subquery(last_insemination.values('is_pregnant')[:1]),
        )

        last_birth = Birth.objects.filter(
            insemination=OuterRef('ultima_inseminacao_id')
        ).order_by('-created_at')

        queryset = queryset.annotate(
            parto_previsto=Subquery(last_birth.values('expected_birth')[:1]),
            secagem_prevista=Subquery(last_birth.values('expected_dry')[:1]),
            secagem=Subquery(last_birth.values('dry')[:1]),
            parto=Subquery(last_birth.values('birth')[:1]),
            birth_id=Subquery(last_birth.values('id')[:1]),
        )

        today = now().date()
        today_minus_40 = today - timedelta(days=get_int("REBREED_AFTER_BIRTH_DAYS", 40))
        today_minus_18 = today - timedelta(days=get_int("RECHECK_OR_REINSEMINATE_MIN_DAYS", 18))

        queryset = queryset.annotate(
            pode_inseminar=Case(
                When(
                    ultima_inseminacao_id__isnull=True,
                    then=Value(True)
                ),
                When(
                    Q(parto__lte=today_minus_40) &
                    (Q(prenhez_verificada__isnull=False)),
                    then=Value(True)
                ),
                # 3ª regra: inseminada mas falhou ou não checada após 18 dias
                When(
                    Q(ultima_inseminacao__lte=today_minus_18) &  # noqa
                    (
                        Q(esta_prenha='N') |
                        Q(ultima_inseminacao__isnull=True)
                    ),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField()
            )
        )

        # prioridade color (0 = vermelho, 1 = amarelo, 2 = normal)

        today_plus_10 = today + timedelta(days=get_int("UPCOMING_WINDOW_DAYS", 10))

        queryset = queryset.annotate(
            prioridade=Case(
                # 0: previsões vencidas
                When(
                    Q(prenhez_verificacao__lte=today) & Q(prenhez_verificada__isnull=True)  # noqa
                    |
                    Q(parto_previsto__lte=today) & Q(parto__isnull=True)
                    |
                    Q(secagem_prevista__lte=today) & Q(secagem__isnull=True),
                    then=Value(0)
                ),
                # 1: apto a inseminação (pode_inseminar=True)
                When(
                    Q(pode_inseminar=True),
                    then=Value(1)
                ),
                # 1 (amarelo): previsão nos próximos 10 dias
                When(
                    (
                        (Q(prenhez_verificacao__gt=today) & Q(prenhez_verificacao__lte=today_plus_10) & Q(prenhez_verificada__isnull=True)) # noqa
                        |
                        (Q(parto_previsto__gt=today) & Q(parto_previsto__lte=today_plus_10) & Q(parto__isnull=True))  # noqa
                        |
                        (Q(secagem_prevista__gt=today) & Q(secagem_prevista__lte=today_plus_10) & Q(secagem__isnull=True))  # noqa
                    ),
                    then=Value(1)
                ),
                # 2: normal
                default=Value(2),
                output_field=IntegerField()
            )
        )

        # Seleção de fazenda via GET ou sessão
        if 'farm' in self.request.GET:
            self.request.session['selected_farm_id'] = self.request.GET.get('farm') or None
        farm_id = self.request.GET.get('farm') or self.request.session.get('selected_farm_id')
        if farm_id:
            queryset = queryset.filter(farm_id=farm_id)

        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        queryset = queryset.order_by('prioridade', 'name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["farms"] = Farm.objects.all()
        context["today"] = now().date()
        context["today_plus_10"] = now().date() + timedelta(days=get_int("UPCOMING_WINDOW_DAYS", 10))
        return context


class AppSettingsView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "app_settings.html"
    form_class = AppSettingsForm

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        save_config(form.cleaned_data)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config"] = load_config()
        return context


class TaskReportFormView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "report_tasks_form.html"
    form_class = AppSettingsForm.__class__.__mro__[1]  # placeholder, will override get_form_class
    permission_required = 'animals.view_animal'

    def get_form_class(self):
        from .forms import TaskReportForm
        return TaskReportForm

    def get_initial(self):
        from datetime import date
        first_day = date.today().replace(day=1)
        return {"start_date": first_day, "end_date": date.today()}

    def form_valid(self, form):
        from django.urls import reverse
        from django.shortcuts import redirect
        data = form.cleaned_data
        params = f"start_date={data['start_date']}&end_date={data['end_date']}"
        if 'selected_farm_id' in self.request.session and self.request.session['selected_farm_id']:
            params += f"&farm={self.request.session['selected_farm_id']}"
        return redirect(f"{reverse('report_tasks_pdf')}?{params}")


class TaskReportPdfView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "report_tasks.html"
    permission_required = 'animals.view_animal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from datetime import datetime
        s = self.request.GET.get('start_date')
        e = self.request.GET.get('end_date')
        try:
            start_date = datetime.strptime(s, '%Y-%m-%d').date() if s else now().date().replace(day=1)
            end_date = datetime.strptime(e, '%Y-%m-%d').date() if e else now().date()
        except ValueError:
            start_date = now().date().replace(day=1)
            end_date = now().date()

        farm_id = self.request.GET.get('farm') or self.request.session.get('selected_farm_id')
        farm_obj = None
        if farm_id:
            try:
                farm_obj = Farm.objects.filter(pk=farm_id).first()
            except Exception:
                farm_obj = None

        today = end_date
        today_minus_40 = today - timedelta(days=get_int("REBREED_AFTER_BIRTH_DAYS", 40))
        today_minus_18 = today - timedelta(days=get_int("RECHECK_OR_REINSEMINATE_MIN_DAYS", 18))

        last_insem = Insemination.objects.filter(animal=OuterRef('pk')).order_by('-date_of_insemination')
        last_birth = Birth.objects.filter(insemination=OuterRef('ultima_inseminacao_id')).order_by('-created_at')

        animals_qs = Animal.objects.select_related('category', 'breed')
        # Considerar somente fêmeas reprodutivas no relatório
        animals_qs = animals_qs.filter(category__is_reproductive_female=True)
        if farm_id:
            animals_qs = animals_qs.filter(farm_id=farm_id)
        animals_qs = animals_qs.annotate(
            ultima_inseminacao_id=Subquery(last_insem.values('id')[:1]),
            ultima_inseminacao=Subquery(last_insem.values('date_of_insemination')[:1]),
            prenhez_verificada=Subquery(last_insem.values('pregnancy_check')[:1]),
            esta_prenha=Subquery(last_insem.values('is_pregnant')[:1]),
        ).annotate(
            parto=Subquery(last_birth.values('birth')[:1]),
        ).annotate(
            pode_inseminar=Case(
                When(ultima_inseminacao_id__isnull=True, then=Value(True)),
                When(Q(parto__lte=today_minus_40) & Q(prenhez_verificada__isnull=False), then=Value(True)),
                When(Q(ultima_inseminacao__lte=today_minus_18) & (Q(esta_prenha='N') | Q(ultima_inseminacao__isnull=True)), then=Value(True)),
                default=Value(False), output_field=BooleanField()
            )
        ).filter(pode_inseminar=True).order_by('name')

        preg_check_qs = Insemination.objects.filter(
            expected_pregnancy__range=(start_date, end_date),
            pregnancy_check__isnull=True,
            animal__category__is_reproductive_female=True,
        ).select_related('animal', 'animal__breed', 'animal__category')
        if farm_id:
            preg_check_qs = preg_check_qs.filter(animal__farm_id=farm_id)

        dry_qs = Birth.objects.filter(
            expected_dry__range=(start_date, end_date),
            dry__isnull=True,
            birth__isnull=True,
            animal__category__is_reproductive_female=True,
        ).select_related('animal', 'animal__breed', 'animal__category')
        if farm_id:
            dry_qs = dry_qs.filter(animal__farm_id=farm_id)

        births_qs = Birth.objects.filter(
            expected_birth__range=(start_date, end_date),
            birth__isnull=True,
            animal__category__is_reproductive_female=True,
        ).select_related('animal', 'animal__breed', 'animal__category')
        if farm_id:
            births_qs = births_qs.filter(animal__farm_id=farm_id)

        context.update({
            'start_date': start_date,
            'end_date': end_date,
            'farm_id': farm_id,
            'farm': farm_obj,
            'can_inseminate': animals_qs,
            'pregnancy_checks': preg_check_qs,
            'dry_tasks': dry_qs,
            'expected_births': births_qs,
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        # Geração de PDF estilizado via ReportLab Platypus; fallback para HTML se indisponível
        try:
            from io import BytesIO
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
            from reportlab.lib.units import cm
        except Exception:
            return super().render_to_response(context, **response_kwargs)

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=1.8*cm,
            bottomMargin=1.5*cm,
            title="Relatório de Tarefas",
        )

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='TitleCenter', parent=styles['Title'], alignment=1))
        styles.add(ParagraphStyle(name='H2', parent=styles['Heading2'], spaceBefore=12, spaceAfter=6))
        styles.add(ParagraphStyle(name='Small', parent=styles['Normal'], fontSize=9, textColor=colors.grey))

        story = []

        # Cabeçalho
        farm_name = context.get('farm').name if context.get('farm') else 'Todas as Propriedades'
        title = f"Relatório de Tarefas — {farm_name}"
        generated_at = now().strftime('%d/%m/%Y %H:%M')
        subtitle = f"Período: {context['start_date'].strftime('%d/%m/%Y')} a {context['end_date'].strftime('%d/%m/%Y')} | Gerado em: {generated_at}"
        story.append(Paragraph(title, styles['TitleCenter']))
        story.append(Paragraph(subtitle, styles['Small']))
        story.append(Spacer(1, 10))

        def table_from_queryset(headers, rows):
            data = [headers] + rows
            tbl = Table(data, hAlign='LEFT')
            tbl.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#343a40')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 10),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.HexColor('#f8f9fa')]),
                ('FONTSIZE', (0,1), (-1,-1), 10),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            return tbl

        # 1) Pode inseminar
        story.append(Paragraph('Vacas/Novilhas que podem ser inseminadas', styles['H2']))
        can_rows = []
        for a in context['can_inseminate']:
            can_rows.append([
                a.name,
                a.birth.strftime('%d/%m/%Y') if getattr(a, 'birth', None) else '-',
                getattr(a.breed, 'name', '-') if getattr(a, 'breed', None) else '-',
                getattr(a.category, 'name', '-') if getattr(a, 'category', None) else '-',
                a.ultima_inseminacao.strftime('%d/%m/%Y') if getattr(a, 'ultima_inseminacao', None) else '-',
            ])
        if can_rows:
            story.append(table_from_queryset(['Animal', 'Nascimento', 'Raça', 'Categoria', 'Última IA'], can_rows))
        else:
            story.append(Paragraph('Nenhum animal elegível no período.', styles['Normal']))
        story.append(Spacer(1, 8))

        # 2) Prenhezes a verificar
        story.append(Paragraph('Prenhezes que devem ser verificadas', styles['H2']))
        preg_rows = []
        for i in context['pregnancy_checks']:
            a = i.animal
            preg_rows.append([
                a.name,
                a.birth.strftime('%d/%m/%Y') if getattr(a, 'birth', None) else '-',
                getattr(a.breed, 'name', '-') if getattr(a, 'breed', None) else '-',
                getattr(a.category, 'name', '-') if getattr(a, 'category', None) else '-',
                i.expected_pregnancy.strftime('%d/%m/%Y') if i.expected_pregnancy else '-',
            ])
        if preg_rows:
            story.append(table_from_queryset(['Animal', 'Nascimento', 'Raça', 'Categoria', 'Prevista'], preg_rows))
        else:
            story.append(Paragraph('Nenhuma verificação no período.', styles['Normal']))
        story.append(Spacer(1, 8))

        # 3) Secagens a realizar
        story.append(Paragraph('Secagens que devem ser realizadas', styles['H2']))
        dry_rows = []
        for b in context['dry_tasks']:
            a = b.animal
            dry_rows.append([
                a.name,
                a.birth.strftime('%d/%m/%Y') if getattr(a, 'birth', None) else '-',
                getattr(a.breed, 'name', '-') if getattr(a, 'breed', None) else '-',
                getattr(a.category, 'name', '-') if getattr(a, 'category', None) else '-',
                b.expected_dry.strftime('%d/%m/%Y') if b.expected_dry else '-',
            ])
        if dry_rows:
            story.append(table_from_queryset(['Animal', 'Nascimento', 'Raça', 'Categoria', 'Prevista'], dry_rows))
        else:
            story.append(Paragraph('Nenhuma secagem no período.', styles['Normal']))
        story.append(Spacer(1, 8))

        # 4) Partos previstos
        story.append(Paragraph('Partos previstos', styles['H2']))
        birth_rows = []
        for b in context['expected_births']:
            a = b.animal
            birth_rows.append([
                a.name,
                a.birth.strftime('%d/%m/%Y') if getattr(a, 'birth', None) else '-',
                getattr(a.breed, 'name', '-') if getattr(a, 'breed', None) else '-',
                getattr(a.category, 'name', '-') if getattr(a, 'category', None) else '-',
                b.expected_birth.strftime('%d/%m/%Y') if b.expected_birth else '-',
            ])
        if birth_rows:
            story.append(table_from_queryset(['Animal', 'Nascimento', 'Raça', 'Categoria', 'Previsto'], birth_rows))
        else:
            story.append(Paragraph('Nenhum parto previsto no período.', styles['Normal']))

        # Rodapé com número de página
        def on_page(canvas, doc):
            canvas.setFont('Helvetica', 8)
            canvas.setFillColor(colors.grey)
            page_txt = f"Página {doc.page}"
            canvas.drawRightString(A4[0] - 2*cm, 1*cm, page_txt)

        doc.build(story, onFirstPage=on_page, onLaterPages=on_page)

        pdf = buffer.getvalue()
        buffer.close()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_tarefas.pdf"'
        return response
