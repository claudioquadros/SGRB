from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', include('companies.urls')),
    path('', include('categories.urls')),
    path('', include('breeds.urls')),
    path('', include('farms.urls')),
    path('', include('animals.urls')),
    path('', include('inseminations.urls')),
    path('', include('births.urls')),
]
