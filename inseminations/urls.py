from django.urls import path
from . import views


urlpatterns = [
    path('inseminations/list/', views.InseminationListView.as_view(), name='insemination_list'),  # noqa
    path('inseminations/create/', views.InseminationCreateView.as_view(), name='insemination_create'),  # noqa
    path('inseminations/<int:pk>/detail/', views.InseminationDetailView.as_view(), name='insemination_detail'), # noqa
    path('inseminations/<int:pk>/update/', views.InseminationUpdateView.as_view(), name='insemination_update'),  # noqa
    path('inseminations/<int:pk>/delete/', views.InseminationDeleteView.as_view(), name='insemination_delete'),  # noqa
]
