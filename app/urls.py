from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import AnimalOverviewListView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', AnimalOverviewListView.as_view(), name='animal_overview'),

    path('', include('companies.urls')),
    path('', include('categories.urls')),
    path('', include('breeds.urls')),
    path('', include('farms.urls')),
    path('', include('animals.urls')),
    path('', include('inseminations.urls')),
    path('', include('births.urls')),
]
