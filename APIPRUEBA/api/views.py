from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
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
        return render(request,self.template_name)
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
def signout(request):
    logout(request)
    return redirect('signin')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            login(request, user)
            return render(request, 'index.html')

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
    
    return redirect('signin')