from django.contrib import admin
from django.urls import path
from api import views
from api.views import *
from django.conf.urls import handler404
from api.views import page_not_found

handler404 = 'api.views.page_not_found'

urlpatterns = [
    #path('admin/', admin.site.urls),
     path('', Home.as_view(),name='index'),
     path('signin/', signin.as_view(),name='signin'),
     path('signup/', views.signup,name='signup'),
     path('logout/', Signout.as_view(), name='logout'),
     path('grupo/', Grupos.as_view(),name='grupo'),
     path('docente/', Docentes.as_view(),name='docente'),
     path('materia/', Materias.as_view(),name='materia'),
     path('periodo/', Periodos.as_view(),name='periodo'),
     path('alumno/', Alumno.as_view(),name='alumno'),
     path('asignacion/', Asignaciones.as_view(),name='asignacion'),
     path('calificaciones/', Calificaciones.as_view(),name='calificaciones'),
     path('parciales/', Parciales.as_view(),name='parciales'),
     path('historial_academico/', Historial.as_view(),name='historial'),
     path('calificaciones_por_grupo/', CalificacionesGrupos.as_view(),name='calificaciones_grupo'),
     path('charts/', Charts.as_view(),name='charts'),
     path('enviar-contrasena-temporal/<str:correo>/',views.enviar_contrasena_temporal, name='enviar-cotrasena-temporal'),
     path('enviar_correo/<str:nombre>/<str:correo>/<str:apellido>/<str:usuario>/<str:contra>/', views.enviar_correo, name='enviar_correo'),
     path('prueba/', Prueba.as_view(),name='prueba'),
]
