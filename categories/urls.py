from django.urls import path
from . import views


urlpatterns = [
    path('categories/list/', views.CategoryListView.as_view(), name='category_list'),  # noqa
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),  # noqa
    path('categories/<int:pk>/detail/', views.CategoryDetailView.as_view(), name='category_detail'), # noqa
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),  # noqa
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),  # noqa
]
