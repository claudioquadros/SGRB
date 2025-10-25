from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import AnimalOverviewListView, AppSettingsView, TaskReportFormView, TaskReportPdfView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', AnimalOverviewListView.as_view(), name='animal_overview'),
    path('', AnimalOverviewListView.as_view(), name='animal_overview'),
    path('settings/', AppSettingsView.as_view(), name='app_settings'),
    path('reports/tasks/', TaskReportFormView.as_view(), name='report_tasks_form'),
    path('reports/tasks/pdf/', TaskReportPdfView.as_view(), name='report_tasks_pdf'),

    path('', include('companies.urls')),
    path('', include('categories.urls')),
    path('', include('breeds.urls')),
    path('', include('farms.urls')),
    path('', include('animals.urls')),
    path('', include('inseminations.urls')),
    path('', include('births.urls')),
]
