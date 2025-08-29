from django.urls import path
from . import views


urlpatterns = [
    path('animals/list/', views.AnimalListView.as_view(), name='animal_list'),  # noqa
    path('animals/create/', views.AnimalCreateView.as_view(), name='animal_create'),  # noqa
    path('animals/<int:pk>/detail/', views.AnimalDetailView.as_view(), name='animal_detail'), # noqa
    path('animals/<int:pk>/update/', views.AnimalUpdateView.as_view(), name='animal_update'),  # noqa
    path('animals/<int:pk>/culling/', views.AnimalCullingView.as_view(), name='animal_culling'),  # noqa
    path('animals/<int:pk>/delete/', views.AnimalDeleteView.as_view(), name='animal_delete'),  # noqa
]
