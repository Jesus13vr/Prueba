from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Materia,Periodo,Grupo
import datetime
from datetime import datetime as fe
import secrets
import string 
from django.contrib.auth import  authenticate
from django.db import IntegrityError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse

# Create your views here.
class Home(APIView):
    template_name = "index.html"
    def post(self, request):
        return render(request,self.template_name)
    def get(self, request):
        return render(request,self.template_name,{'form': AuthenticationForm})
def signup(request):
    if request.method =='GET':
        return render(request, 'signup.html',{
            'form' : UserCreationForm
        })
    else:
            try:
                user = User.objects.create_user(first_name=request.POST['first_name'], email=request.POST['email'], last_name=request.POST['last_name'], username=request.POST['username'], password=request.POST['password'])
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


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm, 'error': 'Usuario o contraseña incorrecta'})

        # Acciones específicas según la cantidad de dígitos en la matrícula
        if len(username) == 10:
            # Acción para usuarios con matrícula de 10 dígitos 
            # Por ejemplo, podrías considerarlos como alumnos
            return render(request, 'index.html', {'user': user})
        elif len(username) == 11:
            # Acción para usuarios con matrícula de 11 dígitos
            # Por ejemplo, podrías considerarlos como docentes
            return render(request, 'index3.html', {'user': user})
        elif len(username) == 12:
            # Acción para usuarios con matrícula de 12 dígitos
            # Por ejemplo, podrías considerarlos como jefes
            return render(request, 'index2.html', {'user': user})
        elif len(username) == 5:
            # Acción para usuarios con matrícula de 12 dígitos
            # Por ejemplo, podrías considerarlos como jefes
            return render(request, 'index4.html', {'user': user}
                          )
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

class forgotpas(APIView):
    def get(self,request):
        return
    
class registrarMateria(APIView):
    template_name = "materia.html"
    def get(self,request):
        return render(request, self.template_name)
    def post(self,request):
        nombre=request.POST.get('nombre')
        semestre=request.POST.get('semestre')
        creditos=request.POST.get('creditos')
        try:
        # Crear y guardar materia
            materia = Materia(nombre=nombre, semestre=semestre, creditos=creditos)
            materia.save()
            return render(request, self.template_name, {"mensaje": 'Materia registrada con exito'})
        except IntegrityError:
            return render(request, self.template_name, {"mensaje": 'Error al registrar la materia'})
   
class RegistraPeriodo(APIView):
    template_name = "periodo.html"
    def get(self,request):
        return render(request, self.template_name)
    def post(self,request):
        try:
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_format = fe.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin = request.POST.get('fecha_fin')
            fecha_forma = fe.strptime(fecha_fin, '%Y-%m-%d')
        # Crear y guardar materia
            periodo = Periodo(fecha_inicio=fecha_format, fecha_fin=fecha_forma)
            periodo.save()
            return render(request, self.template_name, {"mensaje": 'Periodo registrada con exito'})
        except IntegrityError:
            return render(request, self.template_name, {"mensaje": 'Error al registrar la periodo'})
   
class RegistraGrupo(APIView):
    template_name = "grupos.html"

    def get(self, request):
        # Obtén la lista de usuarios y periodos para mostrar en el formulario
        usuarios = User.objects.all()
        periodos = Periodo.objects.all()
        return render(request, self.template_name, {"usuarios": usuarios, "periodos": periodos})

    def post(self, request):
        try:
            nombre_grupo = request.POST.get('nombre_grupo')
            id = request.POST.get('id')
            id_periodo = request.POST.get('id_periodo')

            # Obten los objetos de usuario y periodo
            usuario = User.objects.get(id=id)
            periodo = Periodo.objects.get(id=id_periodo)

            # Crear y guardar grupo
            grupo = Grupo(nombre_grupo=nombre_grupo, usuario=id, periodo=periodo)
            grupo.save()

            return render(request, self.template_name, {"mensaje": 'Grupo registrado con éxito'})
        except IntegrityError:
            return render(request, self.template_name, {"mensaje": 'Error al registrar el grupo'})
#codigo reseteo contraseña
def generar_contrasena_temporal(length=10):
    caracteres=string.ascii_letters + string.digits
    contraseña_temporal=''.join(secrets.choice(caracteres)for i in range(length))
    return contraseña_temporal


#envio de correos
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
class google(APIView):
    template_name = "googlecharts.html"
    def get(self, request):
            return render(request, self.template_name) 

def rest(request):
        return render(request, 'rest.html')
def cuenta(request):
        return render(request, 'cuenta.html')
def grafica(request):
        return render(request, 'grafica.html')
def index2(request):
         return render(request, 'index2.html',{'form': AuthenticationForm})
def index3(request):
        return render(request, 'index3.html', {'form': AuthenticationForm})
def index4(request):
         return render(request, 'index4.html', {'form': AuthenticationForm})
def subir(request):
         return render(request, 'subir.html', {'form': AuthenticationForm})
        