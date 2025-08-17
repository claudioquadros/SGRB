from django.urls import path
from . import views


urlpatterns = [
    path('companies/list/', views.CompanyListView.as_view(), name='company_list'),  # noqa
    path('companies/create/', views.CompanyCreateView.as_view(), name='company_create'),  # noqa
    path('companies/<int:pk>/detail/', views.CompanyDetailView.as_view(), name='company_detail'), # noqa
    path('companies/<int:pk>/update/', views.CompanyUpdateView.as_view(), name='company_update'),  # noqa
    path('companies/<int:pk>/delete/', views.CompanyDeleteView.as_view(), name='company_delete'),  # noqa
]
