from django.urls import path
from . import views


urlpatterns = [
    path('breeds/list/', views.BreedListView.as_view(), name='breed_list'),  # noqa
    path('breeds/create/', views.BreedCreateView.as_view(), name='breed_create'),  # noqa
    path('breeds/<int:pk>/detail/', views.BreedDetailView.as_view(), name='breed_detail'), # noqa
    path('breeds/<int:pk>/update/', views.BreedUpdateView.as_view(), name='breed_update'),  # noqa
    path('breeds/<int:pk>/delete/', views.BreedDeleteView.as_view(), name='breed_delete'),  # noqa
]
