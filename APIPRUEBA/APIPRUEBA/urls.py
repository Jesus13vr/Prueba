from django.contrib import admin
from django.urls import path
from api.views import login,inicio,registro

urlpatterns = [
    path('admin/', admin.site.urls),
     path('login/', login.as_view(),name='login'),
     path('inicio/', inicio.as_view(),name='inicio'),
     path('registro/', registro.as_view(),name='registro'),
]
