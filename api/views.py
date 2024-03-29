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
from django.shortcuts import render
from django.http import HttpResponse
from openpyxl import Workbook
from django.db.models import Avg, F, FloatField, IntegerField, ExpressionWrapper
from django.db.models.functions import Coalesce
import statistics

# Create your views here.
@method_decorator(login_required, name='dispatch')
class Home(APIView):
    template_name = "index.html"
    def get(self, request):
        if request.user.is_authenticated:
            permisos = request.user.fk_Rol.id_Rol
            user_id = request.user.id
            ultimo_periodo = Periodo.objects.latest('id_Periodo')
            if permisos == 4:
                calificaciones = Calificacion.objects.filter(fk_Asignacion__fk_Alumno=user_id, fk_Asignacion__fk_Periodo__Periodo=ultimo_periodo.Periodo)
                total_calificaciones = []
                for calificacion in calificaciones:
                    total = calificacion.Parcial_1 + calificacion.Parcial_2 + calificacion.Parcial_3
                    average = total / 3
                    total_calificaciones.append({
                        "calificacion": calificacion,
                        "total": total,
                        "average": average
                    })
                if total_calificaciones:
                        best_average = max(total_calificaciones, key=lambda x: x["average"])
                        worst_average = min(total_calificaciones, key=lambda x: x["average"])
                        best_subject_name = best_average["calificacion"].fk_Asignacion.fk_Materia.Materia
                        worst_subject_name = worst_average["calificacion"].fk_Asignacion.fk_Materia.Materia
                        
                        permisos = request.user.fk_Rol.id_Rol
                        return render(request, self.template_name, {
                            "calificaciones": calificaciones,
                            "permisos": permisos,
                            "best_average": best_average,
                            "worst_average": worst_average,
                            "best_subject_name": best_subject_name,
                            "worst_subject_name": worst_subject_name,
                        })
                else:
                    return render(request, self.template_name, {
                        "calificaciones": calificaciones,
                        "permisos": permisos
                    })
                
            elif permisos == 3:
                calificaciones = Calificacion.objects.filter(fk_Asignacion__fk_Docente=user_id, fk_Asignacion__fk_Periodo__Periodo=ultimo_periodo.Periodo)
                materias = list(calificaciones.values_list('fk_Asignacion__fk_Materia__Materia', flat=True).distinct())
                print(materias)
                promedios_por_materia = {}
                for calificacion in calificaciones:
                    materia = calificacion.fk_Asignacion.fk_Materia.Materia
                    calificacion_final = (calificacion.Parcial_1 + calificacion.Parcial_2 + calificacion.Parcial_3) / 3
                    
                    if materia in promedios_por_materia:
                        promedios_por_materia[materia].append(calificacion_final)
                    else:
                        promedios_por_materia[materia] = [calificacion_final]
                
                # Calcular el promedio de las calificaciones finales para cada materia
                promedios_finales_por_materia = {}
                desviaciones_estandar_por_materia = {}
                for materia, calificaciones_finales in promedios_por_materia.items():
                    promedio_final = sum(calificaciones_finales) / len(calificaciones_finales)
                    promedios_finales_por_materia[materia] = promedio_final
                    
                    # Verificar que haya al menos dos puntos de datos antes de calcular la desviación estándar
                    if len(calificaciones_finales) >= 2:
                        desviacion = statistics.stdev(calificaciones_finales)
                    else:
                        desviacion = None  # Si no hay suficientes datos, asignamos None a la desviación
                    desviaciones_estandar_por_materia[materia] = desviacion
                    if desviacion is not None:
                        print("Desviación estándar de", materia, ":", desviacion)
                    else:
                        print("No hay suficientes datos para calcular la desviación estándar de", materia)

                print(promedios_finales_por_materia)
                permisos = request.user.fk_Rol.id_Rol
                
                # Obtener los IDs de los CustomUser con fk_Rol=4
                alumnos = CustomUser.objects.filter(fk_Rol=4).values_list('id', flat=True)

                # Obtener el promedio de calificaciones de cada alumno
                promedios = Calificacion.objects.filter(fk_Asignacion__fk_Alumno_id__in=alumnos)\
                    .values('fk_Asignacion__fk_Alumno')\
                    .annotate(promedio=Avg(F('Parcial_1') + F('Parcial_2') + F('Parcial_3'))/3.0)
                print("PROMEDIOS: ", promedios)

                # Filtrar por la materia específica
                materia_id = 2  # ID de la materia específica
                promedios = promedios.filter(fk_Asignacion__fk_Materia_id=materia_id)

                # Ordenar por promedio de mayor a menor
                promedios = promedios.order_by('-promedio')

                # Obtener los nombres de los alumnos
                alumnos_con_promedio = CustomUser.objects.filter(id__in=promedios.values('fk_Asignacion__fk_Alumno'))\
                    .values('first_name', 'last_name')

                # Imprimir resultados
                print("ALUMNOS RANKEADOS")
                datos_alumnos = []
                for alumno, promedio in zip(alumnos_con_promedio, promedios):
                    datos_alumnos.append({
                        'nombre': alumno['first_name'],
                        'apellido': alumno['last_name'],
                        'promedio': promedio['promedio']
                    })

                    
                return render(request, self.template_name, {
                    "calificaciones": calificaciones,
                    "materias": materias,
                    "permisos": permisos,
                    "promedios": promedios_finales_por_materia,
                    "desviaciones": desviaciones_estandar_por_materia,
                    'datos_alumnos': datos_alumnos
                })
            
            elif permisos == 1 or permisos == 2 :
                calificaciones = Calificacion.objects.filter(fk_Asignacion__fk_Periodo__Periodo=ultimo_periodo.Periodo)
                materias = list(calificaciones.values_list('fk_Asignacion__fk_Materia__Materia', flat=True).distinct())
                grupos = list(calificaciones.values_list('fk_Asignacion__fk_Grupo__Grupo', flat=True).distinct())
                print(materias)
                promedios_por_materia = {}
                for calificacion in calificaciones:
                    materia = calificacion.fk_Asignacion.fk_Materia.Materia
                    calificacion_final = (calificacion.Parcial_1 + calificacion.Parcial_2 + calificacion.Parcial_3) / 3
                    
                    if materia in promedios_por_materia:
                        promedios_por_materia[materia].append(calificacion_final)
                    else:
                        promedios_por_materia[materia] = [calificacion_final]
                
                # Calcular el promedio de las calificaciones finales para cada materia
                promedios_finales_por_materia = {}
                for materia, calificaciones_finales in promedios_por_materia.items():
                    promedio_final = sum(calificaciones_finales) / len(calificaciones_finales)
                    promedios_finales_por_materia[materia] = promedio_final
                print(promedios_finales_por_materia)
                permisos = request.user.fk_Rol.id_Rol
                return render(request, self.template_name, {
                    "calificaciones": calificaciones,
                    "materias": materias,
                    "permisos": permisos,
                    "promedios": promedios_finales_por_materia
                })
              
            else:
                return render(request, self.template_name, {
                    "permisos": permisos,
                })
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

                # Verificar que el campo no esté vacío
                if not grupo:
                    return render(request, self.template_name, {"error": 'El campo Grupo no puede estar vacío', "grupos": grupos, "permisos": permisos})

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

                # Verificar que los campos obligatorios no estén vacíos
                if not (first_name and last_name and email and username and password):
                    return render(request, self.template_name, {"error": 'Todos los campos son obligatorios', "docentes": docentes, "permisos": permisos})

                # Obtener objetos relacionados
                rol = get_object_or_404(Rol, id_Rol=3)
                status = get_object_or_404(Status, id_Status=1)

                # Crear y guardar el docente
                registrarDocente = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password, fk_Rol=rol, fk_Status=status)
                registrarDocente.save()

                # Otros procesamientos y retornar la respuesta
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
        elif 'Modificar' in request.POST:
            try:
                docente_id = request.POST.get('Modificar')
                docente = get_object_or_404(CustomUser, id=docente_id)
                first_name_modificado = request.POST.get('first_name_modificado')
                last_name_modificado = request.POST.get('last_name_modificado')
                email_modificado = request.POST.get('email_modificado')
                docente.first_name = first_name_modificado
                docente.last_name = last_name_modificado
                docente.email = email_modificado
                docente.save()
                return render(request, self.template_name, {'mensaje': 'El docente ha sido modificado', "docentes": docentes, "permisos": permisos})
            except models.ProtectedError as e:
                return render(request, self.template_name, {'error': 'No se pudo modificar el docente', "docentes": docentes, "permisos": permisos})
            except Exception as e:
                return render(request, self.template_name, {'error': 'Algo salio mal', "docentes": docentes, "permisos": permisos})
        elif 'Alta' in request.POST:
            try:
                docente_id = request.POST.get('Alta')
                docente = get_object_or_404(CustomUser, id=docente_id)
                status = get_object_or_404(Status, id_Status=1)
                docente.fk_Status = status
                docente.save()
                return render(request, self.template_name, {'mensaje': 'El docente se ha dado de alta correctamente', "docentes": docentes, "permisos": permisos})
            except IntegrityError:
                return render(request, self.template_name, {'error': 'No se pudo modificar el status del docente', "docentes": docentes, "permisos": permisos})

        elif 'Baja' in request.POST:
            try:
                docente_id = request.POST.get('Baja')
                docente = get_object_or_404(CustomUser, id=docente_id)
                status = get_object_or_404(Status, id_Status=2)
                docente.fk_Status = status
                docente.save()
                return render(request, self.template_name, {'mensaje': 'El docente se ha dado de baja correctamente', "docentes": docentes, "permisos": permisos})
            except Exception as e:
                return render(request, self.template_name, {'error': 'No se pudo modificar el status del docente', "docentes": docentes, "permisos": permisos})
       
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

                # Verificar que los campos obligatorios no estén vacíos
                if not (materia and clave and no_creditos):
                    return render(request, self.template_name, {"error": 'Todos los campos son obligatorios', "materias": materias, "permisos": permisos})

                # Crear y guardar la materia
                registrarMateria = Materia(Materia=materia, Clave=clave, No_creditos=no_creditos)
                registrarMateria.save()

                # Otros procesamientos y retornar la respuesta
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
        elif 'Modificar' in request.POST:
            try:
                materia_id = request.POST.get('Modificar')
                materia = get_object_or_404(Materia, id_Materia=materia_id)
                materia_modificado = request.POST.get('materia_modificado')
                clave_modificado = request.POST.get('clave_modificado')
                no_creditos_modificado = request.POST.get('no_creditos_modificado')
                materia.Materia = materia_modificado
                materia.Clave = clave_modificado
                materia.No_creditos = no_creditos_modificado
                materia.save()
                return render(request, self.template_name, {'mensaje': 'La materia ha sido modificada', "materias": materias, "permisos": permisos})
            except Exception as e:
                return render(request, self.template_name, {'error': 'No se pudo modificar la materia', "materias": materias, "permisos": permisos})

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

                # Verificar que los campos obligatorios no estén vacíos
                if not periodo:
                    return render(request, self.template_name, {"error": 'El campo Periodo no puede estar vacío', "periodos": periodos, "ultimo_periodo": ultimo_periodo, "permisos": permisos})

                # Obtener objetos relacionados
                status = get_object_or_404(Status, id_Status=1)

                # Crear y guardar el periodo
                registrarPeriodo = Periodo(Periodo=periodo, fk_Status=status)
                registrarPeriodo.save()

                # Obtener el último periodo registrado
                ultimo_periodo = Periodo.objects.latest('id_Periodo')

                # Otros procesamientos y retornar la respuesta
                return render(request, self.template_name, {"mensaje": 'Periodo registrado con éxito', "periodos": periodos, "ultimo_periodo": ultimo_periodo, "permisos": permisos})
            except IntegrityError:
                return render(request, self.template_name, {"error": 'Error al registrar el periodo', "periodos": periodos, "ultimo_periodo": ultimo_periodo, "permisos": permisos})

        # Otros bloques de código si hay más acciones en el formulario
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

                # Verificar que los campos obligatorios no estén vacíos
                if not (first_name and last_name and email and username and password):
                    return render(request, self.template_name, {"error": 'Todos los campos son obligatorios', "alumnos": alumnos, "permisos": permisos})

                # Obtener objetos relacionados
                rol = get_object_or_404(Rol, id_Rol=4)
                status = get_object_or_404(Status, id_Status=1)

                # Crear y guardar el alumno
                registrarAlumno = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password, fk_Rol=rol, fk_Status=status)
                registrarAlumno.save()

                # Otros procesamientos y retornar la respuesta
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
                asignacion_existente = Asignacion.objects.filter(
                    fk_Alumno=fk_Alumno,
                    fk_Materia=fk_Materia,
                    fk_Periodo=periodo
                ).exists()
                if asignacion_existente:
                    # Si ya existe, mostrar un mensaje de error
                    return render(request, self.template_name, {'error':'Este alumno ya tiene asignada esta materia en este periodo.',"alumnos": alumnos, "materias": materias, "grupos": grupos, "ultimo_periodo":ultimo_periodo, "docentes": docentes, "asignaciones": asignaciones, "permisos": permisos})
                else:

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
        docente = request.user.id
        ultimo_periodo = Periodo.objects.latest('id_Periodo')
        calificaciones = Calificacion.objects.filter(fk_Asignacion__fk_Periodo__Periodo=ultimo_periodo.Periodo)
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
        return render(request, self.template_name, {"calificaciones": calificaciones, "asignacionesuno": asignaciones_sin_calificaciones, "asignacionesdos": asignaciones_sin_calificaciones_parcial_2, "asignacionestres": asignaciones_sin_calificaciones_parcial_3, "user_id": user_id, "permisos": permisos, "grupos": grupos})
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

@method_decorator(login_required, name='dispatch')
class SeguimientoCalificaciones(APIView):
    template_name = "seguimiento_calificaciones.html"
    def get(self, request):
        permisos = request.user.fk_Rol.id_Rol
        docente = request.user.id
        grupos = Grupo.objects.all()
        ultimo_periodo = Periodo.objects.latest('id_Periodo')
        calificaciones = Calificacion.objects.filter(fk_Asignacion__fk_Periodo__Periodo=ultimo_periodo.Periodo, fk_Asignacion__fk_Docente__id=docente)
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

@method_decorator(login_required, name='dispatch')
class Unauthorized(APIView):
    template_name = "unauthorized.html"
    def get(self, request):
        permisos = request.user.fk_Rol.id_Rol
        rol = request.user.fk_Rol.Rol
        return render(request, self.template_name, {'permisos': permisos, 'rol': rol})
    def post(self, request):
        return render(request, self.template_name)

def page_not_found(request, exception):
    return render(request, '404.html', status=404)

def server_error(request):
    return render(request, '500.html', status=500)

def export_to_excel(request):
    if request.method == 'POST':
        selected_cells = request.POST.getlist('selected_cells[]')  # Obtener celdas seleccionadas

        # Procesar las celdas seleccionadas para extraer los datos correspondientes
        data = []
        for cell in selected_cells:
            row_index, col_index = map(int, cell.split('_')[1:])  # Separar índices de fila y columna
            data.append((row_index, col_index, request.POST.get(f'data_{row_index}_{col_index}')))

        # Generar archivo Excel
        workbook = Workbook()
        sheet = workbook.active

        for row_index, col_index, value in data:
            sheet.cell(row=row_index, column=col_index, value=value)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=datos.xlsx'
        workbook.save(response)
        return response
    else:
        # Aquí deberías pasar los datos de tu modelo a la plantilla HTML
        return render(request, 'export.html', context={})
