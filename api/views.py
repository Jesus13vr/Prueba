from django.shortcuts import render, redirect, redirect, get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from api.models import CustomUser
from .models import *
import datetime
from datetime import datetime as fe
import secrets
import string 
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.db.models import Subquery, OuterRef, Exists
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(login_required, name='dispatch')
class Home(APIView):
    template_name = "index.html"
    def get(self, request):
        if request.user.is_authenticated:
            permisos = request.user.fk_Rol.id_Rol
            user_id = request.user.id
            ultimo_periodo = Periodo.objects.latest('id_Periodo')
            calificaciones = Calificacion.objects.filter(fk_Asignacion__fk_Alumno=user_id, fk_Asignacion__fk_Periodo__Periodo=ultimo_periodo.Periodo)
            return render(request, self.template_name, {"calificaciones": calificaciones, "permisos": permisos})
        else:
            return redirect("signin")
    def post(self, request):
        if request.user.is_authenticated:
            permisos = request.user.fk_Rol.id_Rol
            user_id = request.user.id
            ultimo_periodo = Periodo.objects.latest('id_Periodo')
            calificaciones = Calificacion.objects.filter(fk_Asignacion__fk_Alumno=user_id, fk_Asignacion__fk_Periodo__Periodo=ultimo_periodo.Periodo)
            return render(request, self.template_name, {"calificaciones": calificaciones, "permisos": permisos})
        else:
            return redirect("signin")
    
def signup(request):
    if request.method =='GET':
        return render(request, 'signup.html',{
            'form' : UserCreationForm
        })
    else:
            try:
                user = CustomUser.objects.create_user(first_name=request.POST['first_name'], email=request.POST['email'], last_name=request.POST['last_name'], username=request.POST['username'], password=request.POST['password'])
                user.save()
                nombre = request.POST['first_name']
                correo = request.POST['email']
                apellido = request.POST['last_name']
                usuario = request.POST['username']
                contra = request.POST['password']
                return redirect('enviar_correo', nombre=nombre, correo=correo, apellido=apellido, usuario=usuario, contra=contra)
                                
            except IntegrityError:
                return render(request, 'signup.html',{
                    'form' : UserCreationForm,
                    "mensaje" : 'Username already exist'
                })
                #return HttpResponse('Username already exist')
        #return HttpResponse('Password do not match')       

class signin(APIView):
    template_name= "signin.html"
    def get(self, request):
        if request.user.is_authenticated:
           
            return redirect('/')
        else:
            return render(request, self.template_name, {
                'form': AuthenticationForm
            })
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, self.template_name, {
                    'form': AuthenticationForm,
                    
                    'error': 'Usuario o contraseña incorrecta'
                })
            else:
                login(request, user)
                return redirect('/')

class Signout(APIView):
    def get(self,request):
        logout(request)
        return redirect('index')

class forgotpas(APIView):
    def get(self,request):
        return
 
def enviar_correo(request, nombre, correo, apellido, usuario, contra):
    subject = 'Bienvenida'
    from_email = 'jesusvillanueva203@gmail.com'
    recipient_list = [correo]

    # Renderiza la plantilla HTML con el contexto
    contexto = {'nombre': nombre,
                'correo': correo,
                'apellido': apellido,
                'usuario': usuario,
                "contra": contra}
    contenido_correo = render_to_string('enviar_correo.html', contexto)

    # Envía el correo
    send_mail(subject, '', from_email, recipient_list, html_message=contenido_correo)
    #ventana reseteo de contraseña
    return redirect('signin')

@method_decorator(login_required, name='dispatch')
class Grupos(APIView):
    template_name = "grupo.html"
    def get(self, request):
        permisos = request.user.fk_Rol.id_Rol
        grupos = Grupo.objects.all()
        return render(request, self.template_name, {'grupos': grupos, "permisos": permisos})
    def post(self, request):
        permisos = request.user.fk_Rol.id_Rol
        grupos = Grupo.objects.all()
        if 'Crear' in request.POST:
            try:
                grupo = request.POST.get('Grupo')
                registrarGrupo = Grupo(Grupo=grupo)
                registrarGrupo.save()
                return render(request, self.template_name, {"mensaje": 'Grupo registrado con éxito', "grupos": grupos, "permisos": permisos})
            except IntegrityError:
                return render(request, self.template_name, {"error": 'Error al registrar el grupo', "grupos": grupos, "permisos": permisos})
        elif 'Borrar' in request.POST:
            try:
                grupo_id = request.POST.get('Borrar')
                grupo = get_object_or_404(Grupo, id_Grupo=grupo_id)
                grupo.delete()
                return render(request,self.template_name, {'mensaje': 'El grupo ha sido eliminado', "grupos": grupos, "permisos": permisos})
            except models.ProtectedError as e:
                return render(request, self.template_name, {'error': 'El grupo no se elimino porque esta siendo utilizado', "grupos": grupos, "permisos": permisos})
            except Exception as e:
                return render(request, self.template_name, {'error': 'No se pudo eliminar el grupo', "grupos": grupos, "permisos": permisos})

@method_decorator(login_required, name='dispatch')
class Docentes(APIView):
    template_name = "docente.html"
    def get(self, request):
        permisos = request.user.fk_Rol.id_Rol
        docentes = CustomUser.objects.filter(fk_Rol=3)
        return render(request, self.template_name, {"docentes": docentes, "permisos": permisos})
    def post(self, request):
        permisos = request.user.fk_Rol.id_Rol
        docentes = CustomUser.objects.filter(fk_Rol=3)
        if 'Crear' in request.POST:
            try:
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                username = request.POST.get('username')
                password = request.POST.get('password')
                rol = get_object_or_404(Rol, id_Rol=3)
                status = get_object_or_404(Status, id_Status=1)
                registrarDocente = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password, fk_Rol=rol, fk_Status=status)
                registrarDocente.save()
                return render(request, self.template_name, {"mensaje": 'Docente registrado con éxito', "docentes": docentes, "permisos": permisos})
            except IntegrityError:
                return render(request, self.template_name, {"error": 'Error al registrar el docente', "docentes": docentes, "permisos": permisos})
        elif 'Borrar' in request.POST:
            try:
                docente_id = request.POST.get('Borrar')
                docente = get_object_or_404(CustomUser, id=docente_id)
                docente.delete()
                return render(request,self.template_name, {'mensaje': 'El docente ha sido eliminado', "docentes": docentes, "permisos": permisos})
            except models.ProtectedError as e:
                return render(request, self.template_name, {'error': 'El docente no se elimino porque esta siendo utilizado', "docentes": docentes, "permisos": permisos})
            except Exception as e:
                return render(request, self.template_name, {'error': 'No se pudo eliminar el docente', "docentes": docentes, "permisos": permisos})

@method_decorator(login_required, name='dispatch')
class Materias(APIView):
    template_name = "materia.html"
    def get(self, request):
        permisos = request.user.fk_Rol.id_Rol
        materias = Materia.objects.all()
        return render(request, self.template_name, {"materias": materias, "permisos": permisos})
    def post(self, request):
        permisos = request.user.fk_Rol.id_Rol
        materias = Materia.objects.all()
        if 'Crear' in request.POST:
            try:
                materia = request.POST.get('materia')
                clave = request.POST.get('clave')
                no_creditos = request.POST.get('no_creditos')
                registrarMateria = Materia(Materia=materia, Clave=clave, No_creditos=no_creditos)
                registrarMateria.save()
                return render(request, self.template_name, {"mensaje": 'Materia registrada con éxito', "materias": materias, "permisos": permisos})
            except IntegrityError:
                return render(request, self.template_name, {"error": 'Error al registrar la materia', "materias": materias, "permisos": permisos})
        elif 'Borrar' in request.POST:
            try:
                materia_id = request.POST.get('Borrar')
                materia = get_object_or_404(Materia, id_Materia=materia_id)
                materia.delete()
                return render(request,self.template_name, {'mensaje': 'La materia ha sido eliminada', "materias": materias, "permisos": permisos})
            except models.ProtectedError as e:
                return render(request, self.template_name, {'error': 'La materia no se elimino porque esta siendo utilizada', "materias": materias, "permisos": permisos})
            except Exception as e:
                return render(request, self.template_name, {'error': 'No se pudo eliminar la materia', "materias": materias, "permisos": permisos})

@method_decorator(login_required, name='dispatch')
class Periodos(APIView):
    template_name = "periodo.html"
    def get(self, request):
        permisos = request.user.fk_Rol.id_Rol
        periodos = Periodo.objects.all()
        ultimo_periodo = Periodo.objects.latest('id_Periodo')
        return render(request, self.template_name, {"periodos": periodos, "ultimo_periodo": ultimo_periodo, "permisos": permisos})
    def post(self, request):
        permisos = request.user.fk_Rol.id_Rol
        periodos = Periodo.objects.all()
        if 'Crear' in request.POST:
            try:
                periodo = request.POST.get('periodo')
                status = get_object_or_404(Status, id_Status=1)
                registrarPeriodo = Periodo(Periodo=periodo, fk_Status=status)
                registrarPeriodo.save()
                ultimo_periodo = Periodo.objects.latest('id_Periodo')
                return render(request, self.template_name, {"mensaje": 'Periodo registrado con éxito', "periodos": periodos, "ultimo_periodo": ultimo_periodo, "permisos": permisos})
            except IntegrityError:
                return render(request, self.template_name, {"error": 'Error al registrar el periodo', "periodos": periodos, "ultimo_periodo": ultimo_periodo, "permisos": permisos})
        elif 'Borrar' in request.POST:
            try:
                periodo_id = request.POST.get('Borrar')
                periodo = get_object_or_404(Periodo, id_Periodo=periodo_id)
                status = get_object_or_404(Status, id_Status=4)
                periodo.fk_Status = status
                periodo.save()
                ultimo_periodo = Periodo.objects.latest('id_Periodo')
                return render(request,self.template_name, {'mensaje': 'El periodo ha concluido', "periodos": periodos, "ultimo_periodo": ultimo_periodo, "permisos": permisos})
            except Exception as e:
                return render(request, self.template_name, {'error': 'No se pudo concluir el periodo', "periodos": periodos, "ultimo_periodo": ultimo_periodo, "permisos": permisos})

@method_decorator(login_required, name='dispatch')
class Alumno(APIView):
    template_name = "alumno.html"
    def get(self, request):
        permisos = request.user.fk_Rol.id_Rol
        alumnos = CustomUser.objects.filter(fk_Rol=4)
        return render(request, self.template_name, {"alumnos": alumnos, "permisos": permisos})
    def post(self, request):
        permisos = request.user.fk_Rol.id_Rol
        alumnos = CustomUser.objects.filter(fk_Rol=4)
        if 'Crear' in request.POST:
            try:
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                username = request.POST.get('username')
                password = request.POST.get('password')
                rol = get_object_or_404(Rol, id_Rol=4)
                status = get_object_or_404(Status, id_Status=1)
                registrarDocente = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password, fk_Rol=rol, fk_Status=status)
                registrarDocente.save()
                return render(request, self.template_name, {"mensaje": 'Alumno registrado con éxito', "alumnos": alumnos, "permisos": permisos})
            except IntegrityError:
                return render(request, self.template_name, {"error": 'Error al registrar el alumno', "alumnos": alumnos, "permisos": permisos})
        elif 'Egresar' in request.POST:
            try:
                alumno_id = request.POST.get('Egresar')
                alumno = get_object_or_404(CustomUser, id=alumno_id)
                status = get_object_or_404(Status, id_Status=3)
                alumno.fk_Status = status
                alumno.save()
                return render(request,self.template_name, {'mensaje': 'El status del alumno a cambiado a egresado y este no puede ser modificado nuevamente', "alumnos": alumnos, "permisos": permisos})
            except Exception as e:
                return render(request, self.template_name, {'error': 'No se pudo modificar ek status del alumno', "alumnos": alumnos, "permisos": permisos})
        elif 'Alta' in request.POST:
            try:
                alumno_id = request.POST.get('Alta')
                alumno = get_object_or_404(CustomUser, id=alumno_id)
                status = get_object_or_404(Status, id_Status=1)
                alumno.fk_Status = status
                alumno.save()
                return render(request,self.template_name, {'mensaje': 'El alumno se ha dado de alta correctamente', "alumnos": alumnos, "permisos": permisos})
            except Exception as e:
                return render(request, self.template_name, {'error': 'No se pudo modificar ek status del alumno', "alumnos": alumnos, "permisos": permisos})
        elif 'Baja' in request.POST:
            try:
                alumno_id = request.POST.get('Baja')
                alumno = get_object_or_404(CustomUser, id=alumno_id)
                status = get_object_or_404(Status, id_Status=2)
                alumno.fk_Status = status
                alumno.save()
                return render(request,self.template_name, {'mensaje': 'El alumno se ha dado de baja correctamente', "alumnos": alumnos, "permisos": permisos})
            except Exception as e:
                return render(request, self.template_name, {'error': 'No se pudo modificar ek status del alumno', "alumnos": alumnos, "permisos": permisos})
    
@method_decorator(login_required, name='dispatch')  
class Asignaciones(APIView):
    template_name = "asignaciones.html"
    def get(self, request):
        permisos = request.user.fk_Rol.id_Rol
        alumnos = CustomUser.objects.filter(fk_Rol=4, fk_Status=1)
        materias = Materia.objects.all()
        grupos = Grupo.objects.all()
        ultimo_periodo = Periodo.objects.latest('id_Periodo')
        docentes = CustomUser.objects.filter(fk_Rol=3, fk_Status=1)
        asignaciones = Asignacion.objects.all()
        return render(request, self.template_name, {"alumnos": alumnos, "materias": materias, "grupos": grupos, "ultimo_periodo": ultimo_periodo, "docentes": docentes, "asignaciones": asignaciones, "permisos": permisos})
    def post(self, request):
        permisos = request.user.fk_Rol.id_Rol
        alumnos = CustomUser.objects.filter(fk_Rol=4, fk_Status=1)
        materias = Materia.objects.all()
        grupos = Grupo.objects.all()
        ultimo_periodo = Periodo.objects.latest('id_Periodo')
        docentes = CustomUser.objects.filter(fk_Rol=3, fk_Status=1)
        asignaciones = Asignacion.objects.all()
        if 'Crear' in request.POST:
            try:
                fk_Alumno = request.POST.get('fk_Alumno')
                fk_Grupo = request.POST.get('fk_Grupo')
                fk_Materia = request.POST.get('fk_Materia')
                fk_Docente = request.POST.get('fk_Docente')
                alumno = get_object_or_404(CustomUser, id=fk_Alumno)
                grupo = get_object_or_404(Grupo, id_Grupo=fk_Grupo)
                materia = get_object_or_404(Materia, id_Materia=fk_Materia)
                periodo = get_object_or_404(Periodo, id_Periodo=ultimo_periodo.id_Periodo)
                docente = get_object_or_404(CustomUser, id=fk_Docente)
                registrarAsignacion = Asignacion(fk_Alumno=alumno, fk_Grupo=grupo, fk_Materia=materia, fk_Periodo=periodo, fk_Docente=docente)
                registrarAsignacion.save()
                return render(request, self.template_name, {"mensaje": 'Asignación registrada con éxito', "alumnos": alumnos, "materias": materias, "grupos": grupos, "ultimo_periodo":ultimo_periodo, "docentes": docentes, "asignaciones": asignaciones, "permisos": permisos})
            except IntegrityError:
                return render(request, self.template_name, {"error": 'Error al crear la asignación', "alumnos": alumnos, "materias": materias, "grupos": grupos, "ultimo_periodo":ultimo_periodo, "docentes": docentes, "asignaciones": asignaciones, "permisos": permisos})
        elif 'Borrar' in request.POST:
            try:
                asignacion_id = request.POST.get('Borrar')
                asignacion = get_object_or_404(Asignacion, id_Asignacion=asignacion_id)
                asignacion.delete()
                return render(request,self.template_name, {'mensaje': 'La asignacion ha sido eliminado', "alumnos": alumnos, "materias": materias, "grupos": grupos, "ultimo_periodo":ultimo_periodo, "docentes": docentes, "asignaciones": asignaciones, "permisos": permisos})
            except models.ProtectedError as e:
                return render(request, self.template_name, {'error': 'La asignacion no se elimino porque esta siendo utilizado', "alumnos": alumnos, "materias": materias, "grupos": grupos, "ultimo_periodo":ultimo_periodo, "docentes": docentes, "asignaciones": asignaciones, "permisos": permisos})
            except Exception as e:
                return render(request, self.template_name, {'error': 'No se pudo eliminar la asignacion', "alumnos": alumnos, "materias": materias, "grupos": grupos, "ultimo_periodo":ultimo_periodo, "docentes": docentes, "asignaciones": asignaciones, "permisos": permisos})

@method_decorator(login_required, name='dispatch')
class Calificaciones(APIView):
    template_name = "calificaciones.html"
    def get(self, request):
        permisos = request.user.fk_Rol.id_Rol
        grupos = Grupo.objects.all()
        asignaciones_sin_calificaciones = Asignacion.objects.exclude(id_Asignacion__in=Subquery(Calificacion.objects.values('fk_Asignacion')))
        asignaciones_sin_calificaciones_parcial_2 = Asignacion.objects.exclude(
            id_Asignacion__in=Subquery(
                Calificacion.objects.filter(
                    Parcial_2__gt=0.0,
                    fk_Asignacion=OuterRef('id_Asignacion')  # Verificar que haya al menos una calificación asociada
                ).values('fk_Asignacion')
            )
        ).exclude(
            ~Exists(
                Calificacion.objects.filter(
                    fk_Asignacion=OuterRef('id_Asignacion')
                )
            )
        )
        asignaciones_sin_calificaciones_parcial_3 = Asignacion.objects.exclude(
            id_Asignacion__in=Subquery(
                Calificacion.objects.filter(
                    Parcial_3__gt=0.0,
                    fk_Asignacion=OuterRef('id_Asignacion')  # Verificar que haya al menos una calificación asociada
                ).values('fk_Asignacion')
            )
        ).exclude(
            ~Exists(
                Calificacion.objects.filter(
                    fk_Asignacion=OuterRef('id_Asignacion')
                )
            )
        )
        user_id = request.user.id
        return render(request, self.template_name, {"asignacionesuno": asignaciones_sin_calificaciones, "asignacionesdos": asignaciones_sin_calificaciones_parcial_2, "asignacionestres": asignaciones_sin_calificaciones_parcial_3, "user_id": user_id, "permisos": permisos, "grupos": grupos})
    def post(self, request):
        permisos = request.user.fk_Rol.id_Rol
        grupos = Grupo.objects.all()
        asignaciones_sin_calificaciones = Asignacion.objects.exclude(id_Asignacion__in=Subquery(Calificacion.objects.values('fk_Asignacion')))
        asignaciones_sin_calificaciones_parcial_2 = Asignacion.objects.exclude(
            id_Asignacion__in=Subquery(
                Calificacion.objects.filter(
                    Parcial_2__gt=0.0,
                    fk_Asignacion=OuterRef('id_Asignacion')  # Verificar que haya al menos una calificación asociada
                ).values('fk_Asignacion')
            )
        ).exclude(
            ~Exists(
                Calificacion.objects.filter(
                    fk_Asignacion=OuterRef('id_Asignacion')
                )
            )
        )
        asignaciones_sin_calificaciones_parcial_3 = Asignacion.objects.exclude(
            id_Asignacion__in=Subquery(
                Calificacion.objects.filter(
                    Parcial_3__gt=0.0,
                    fk_Asignacion=OuterRef('id_Asignacion')  # Verificar que haya al menos una calificación asociada
                ).values('fk_Asignacion')
            )
        ).exclude(
            ~Exists(
                Calificacion.objects.filter(
                    fk_Asignacion=OuterRef('id_Asignacion')
                )
            )
        )
        user_id = request.user.id
        if 'Parcial1' in request.POST:
            try:
                fk_Asignacion = request.POST.get('fk_Asignacion')
                calificacion = request.POST.get('calificacion')
                asignacion = get_object_or_404(Asignacion, id_Asignacion=fk_Asignacion)
                registrarCalificacion = Calificacion(fk_Asignacion=asignacion, Parcial_1=calificacion)
                registrarCalificacion.save()
                return render(request, self.template_name, {"mensaje": 'Calificación del 1er parcial registrada con éxito', "asignacionesuno": asignaciones_sin_calificaciones, "asignacionesdos": asignaciones_sin_calificaciones_parcial_2, "asignacionestres": asignaciones_sin_calificaciones_parcial_3, "user_id": user_id, "permisos": permisos, "grupos": grupos})
            except IntegrityError:
                return render(request, self.template_name, {"error": 'Error al registrar la calificación del 1er parcial.', "asignacionesuno": asignaciones_sin_calificaciones, "asignacionesdos": asignaciones_sin_calificaciones_parcial_2, "asignacionestres": asignaciones_sin_calificaciones_parcial_3, "user_id": user_id, "permisos": permisos, "grupos": grupos})
        if 'Parcial2' in request.POST:
            try:
                asignacion_id = request.POST.get('fk_Asignacion')
                calificacion = get_object_or_404(Calificacion, fk_Asignacion=asignacion_id)
                calificacion.Parcial_2 = request.POST.get('calificacion')
                calificacion.save()
                return render(request, self.template_name, {"mensaje": 'Calificación del 2do parcial registrada con éxito', "asignacionesuno": asignaciones_sin_calificaciones, "asignacionesdos": asignaciones_sin_calificaciones_parcial_2, "asignacionestres": asignaciones_sin_calificaciones_parcial_3, "user_id": user_id, "permisos": permisos, "grupos": grupos})
            except IntegrityError:
                return render(request, self.template_name, {"error": 'Error al registrar la calificación del 2do parcial ', "asignacionesuno": asignaciones_sin_calificaciones, "asignacionesdos": asignaciones_sin_calificaciones_parcial_2, "asignacionestres": asignaciones_sin_calificaciones_parcial_3, "user_id": user_id, "permisos": permisos, "grupos": grupos})
        if 'Parcial3' in request.POST:
            try:
                asignacion_id = request.POST.get('fk_Asignacion')
                calificacion = get_object_or_404(Calificacion, fk_Asignacion=asignacion_id)
                calificacion.Parcial_3 = request.POST.get('calificacion')
                calificacion.save()
                return render(request, self.template_name, {"mensaje": 'Calificación del 3er parcial registrada con éxito', "asignacionesuno": asignaciones_sin_calificaciones, "asignacionesdos": asignaciones_sin_calificaciones_parcial_2, "asignacionestres": asignaciones_sin_calificaciones_parcial_3, "user_id": user_id, "permisos": permisos, "grupos": grupos})
            except IntegrityError:
                return render(request, self.template_name, {"error": 'Error al registrar la calificación del 3er parcial ', "asignacionesuno": asignaciones_sin_calificaciones, "asignacionesdos": asignaciones_sin_calificaciones_parcial_2, "asignacionestres": asignaciones_sin_calificaciones_parcial_3, "user_id": user_id, "permisos": permisos, "grupos": grupos})

@method_decorator(login_required, name='dispatch')
class Parciales(APIView):
    template_name = "parciales.html"
    def get(self, request):
        permisos = request.user.fk_Rol.id_Rol
        user_id = request.user.id
        ultimo_periodo = Periodo.objects.latest('id_Periodo')
        calificaciones = Calificacion.objects.filter(fk_Asignacion__fk_Alumno=user_id, fk_Asignacion__fk_Periodo__Periodo=ultimo_periodo.Periodo)
        return render(request, self.template_name, {"calificaciones": calificaciones, "permisos": permisos})
    def post(self, request):
        permisos = request.user.fk_Rol.id_Rol
        return render(request, self.template_name, {"permisos": permisos})

@method_decorator(login_required, name='dispatch')
class Historial(APIView):
    template_name = "historial.html"
    def get(self, request):
        permisos = request.user.fk_Rol.id_Rol
        user_id = request.user.id
        calificaciones = Calificacion.objects.filter(fk_Asignacion__fk_Alumno=user_id)
        return render(request, self.template_name, {"calificaciones": calificaciones, "permisos": permisos})
    def post(self, request):
        permisos = request.user.fk_Rol.id_Rol
        return render(request, self.template_name, {"permisos": permisos})

@method_decorator(login_required, name='dispatch')
class CalificacionesGrupos(APIView):
    template_name = "calificaciones_grupos.html"
    def get(self, request):
        permisos = request.user.fk_Rol.id_Rol
        grupos = Grupo.objects.all()
        ultimo_periodo = Periodo.objects.latest('id_Periodo')
        calificaciones = Calificacion.objects.filter(fk_Asignacion__fk_Periodo__Periodo=ultimo_periodo.Periodo)
        return render(request, self.template_name, {"calificaciones": calificaciones, "permisos": permisos, "grupos": grupos})
    def post(self, request):
        permisos = request.user.fk_Rol.id_Rol
        return render(request, self.template_name, {"permisos": permisos})

class Charts(APIView):
    template_name= "googlecharts.html"
    def get(self, request):
        user_id = request.user.id
        ultimo_periodo = Periodo.objects.latest('id_Periodo')
        calificaciones = Calificacion.objects.filter(fk_Asignacion__fk_Alumno=user_id, fk_Asignacion__fk_Periodo__Periodo=ultimo_periodo.Periodo)
        return render(request, self.template_name, {"calificaciones": calificaciones})
    
def generar_contrasena_temporal(length=10):
    caracteres=string.ascii_letters + string.digits
    contraseña_temporal=''.join(secrets.choice(caracteres)for i in range(length))
    return contraseña_temporal

def enviar_contrasena_temporal(request, username):
    usuario = usuario.objects.get(username=username)  # Recupera el usuario por su nombre de usuario

    # Genera una contraseña temporal
    contrasena_temporal = generar_contrasena_temporal()

    # Asigna la contraseña temporal al usuario
    usuario.set_password(contrasena_temporal)
    usuario.save()

    # Envía un correo electrónico con la contraseña temporal
    subject = 'Contraseña temporal'
    message = f'Tu contraseña temporal es: {contrasena_temporal}'
    from_email = 'jesusvillanueva203@gmail.com'
    recipient_list = [usuario.email]

    send_mail(subject, message, from_email, recipient_list)

    return render(request,'enviar_correo.html')

class Prueba(APIView):
    template_name = "prueba.html"
    def get(self, request):
        permisos = request.user.fk_Rol.id_Rol
        user_id = request.user.id
        ultimo_periodo = Periodo.objects.latest('id_Periodo')
        calificaciones = Calificacion.objects.filter(fk_Asignacion__fk_Alumno=user_id, fk_Asignacion__fk_Periodo__Periodo=ultimo_periodo.Periodo)
        return render(request, self.template_name, {"calificaciones": calificaciones, "permisos": permisos})
    
def page_not_found(request, exception):
    return render(request, '404.html', status=404)
