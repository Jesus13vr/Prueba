import os
import django
from django.contrib.auth.hashers import make_password
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "APIPRUEBA.settings")
django.setup()
from api.models import *
datosRol = [
    {'Rol': 'Administrador'},
    {'Rol': 'Jefe de carrera'},
    {'Rol': 'Maestro'},
    {'Rol': 'Alumno'}
]
datosStatus = [
    {'Status': 'Activo'},
    {'Status': 'Baja'},
    {'Status': 'Egresado'},
    {'Status': 'Concluido'}
]
datosUsuarios = [
    {
        'is_superuser': True,
        'email': 'jesusvillanueva203@gmail.com',
        'username': 'pou',
        'password': '123',
        'fk_Rol': 1,
        'fk_Status': 1
    },
    {
        'first_name': 'Zita Concepción',
        'last_name': 'Alvarez Cruz',
        'email': 'zitaalvarez@teschi.edu.mx',
        'username': 'zita',
        'password': '123',
        'fk_Rol': 3,
        'fk_Status': 1
    },
    {
        'first_name': 'Jesus',
        'last_name': 'Romero Villanueva',
        'email': 'jesusvillanueva203@gmail.com',
        'username': 'yisus',
        'password': '123',
        'fk_Rol': 4,
        'fk_Status': 1
    }
]
datoPeriodo = {
    'Periodo': '0000-0',
    'fk_Status': 4
}

for datoRol in datosRol:
    createRol = Rol(**datoRol)
    createRol.save()
print("Roles insertados correctamente.")
for datoStatus in datosStatus:
    createStatus = Status(**datoStatus)
    createStatus.save()
print("Status insertados correctamente.")
for datoUsuarios in datosUsuarios:
    datoUsuarios['password'] = make_password(datoUsuarios['password'])
    fk_Rol = datoUsuarios.pop('fk_Rol')
    fk_Status = datoUsuarios.pop('fk_Status')
    rol = Rol.objects.get(id_Rol=fk_Rol)
    status = Status.objects.get(id_Status=fk_Status)
    createUsuario = CustomUser(fk_Rol=rol, fk_Status=status, **datoUsuarios)
    createUsuario.save()
print("Usuarios creados correctamente.")
fk_Status = datoPeriodo.pop('fk_Status')
status = Status.objects.get(id_Status=fk_Status)
createPeriodo = Periodo(fk_Status=status, **datoPeriodo)
createPeriodo.save()
print("Periodo creado correctamente.")