from django.urls import path
from . import views


urlpatterns = [
    path('farms/list/', views.FarmListView.as_view(), name='farm_list'),  # noqa
    path('farms/create/', views.FarmCreateView.as_view(), name='farm_create'),  # noqa
    path('farms/<int:pk>/detail/', views.FarmDetailView.as_view(), name='farm_detail'), # noqa
    path('farms/<int:pk>/update/', views.FarmUpdateView.as_view(), name='farm_update'),  # noqa
    path('farms/<int:pk>/delete/', views.FarmDeleteView.as_view(), name='farm_delete'),  # noqa
]
