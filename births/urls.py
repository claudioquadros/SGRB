from django.urls import path
from . import views


urlpatterns = [
    path('births/list/', views.BirthListView.as_view(), name='birth_list'),  # noqa
    path('births/create/', views.BirthCreateView.as_view(), name='birth_create'),  # noqa
    path('births/<int:pk>/detail/', views.BirthDetailView.as_view(), name='birth_detail'), # noqa
    path('births/<int:pk>/update/', views.BirthUpdateView.as_view(), name='birth_update'),  # noqa
    path('births/<int:pk>/delete/', views.BirthDeleteView.as_view(), name='birth_delete'),  # noqa
    path('births/<int:pk>/check_dry/', views.CheckDryUpdateView.as_view(), name='birth_check_dry'),  # noqa
    path('births/<int:pk>/check_birth/', views.CheckBirthUpdateView.as_view(), name='birth_check_birth'),  # noqa
]
