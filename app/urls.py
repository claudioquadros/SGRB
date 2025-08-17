from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('companies.urls')),
    path('', include('categories.urls')),
    path('', include('breeds.urls')),
    path('', include('farms.urls')),
    path('', include('animals.urls')),
    path('', include('inseminations.urls')),
]
