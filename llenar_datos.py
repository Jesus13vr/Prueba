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
        "first_name": "Juan Carlos",
        "last_name": "García López",
        "email": "juancarlos@teschi.edu.mx",
        "username": "juancarlos",
        "password": "123",
        "fk_Rol": 3,
        "fk_Status": 1
    },
    {
        "first_name": "María Fernanda",
        "last_name": "Rodríguez Pérez",
        "email": "mariafernanda@teschi.edu.mx",
        "username": "mariafernanda",
        "password": "123",
        "fk_Rol": 3,
        "fk_Status": 1
    },
    {
        "first_name": "Alejandro",
        "last_name": "Martínez Ruiz",
        "email": "alejandro@teschi.edu.mx",
        "username": "alejandro",
        "password": "123",
        "fk_Rol": 3,
        "fk_Status": 1
    },
    {
        "first_name": "Ana Sofía",
        "last_name": "Hernández García",
        "email": "anasofia@teschi.edu.mx",
        "username": "anasofia",
        "password": "123",
        "fk_Rol": 3,
        "fk_Status": 1
    },
    {
        "first_name": "Luis Alberto",
        "last_name": "Pérez López",
        "email": "luisalberto@teschi.edu.mx",
        "username": "luisalberto",
        "password": "123",
        "fk_Rol": 3,
        "fk_Status": 1
    },
    {
        'first_name': 'Jesus',
        'last_name': 'Romero Villanueva',
        'email': 'jesusvillanueva203@gmail.com',
        'username': 'yisus',
        'password': '123',
        'fk_Rol': 4,
        'fk_Status': 1
    },
    {
        "first_name": "Pedro",
        "last_name": "López Rodríguez",
        "email": "pedrolopez@teschi.edu.mx",
        "username": "pedrolopez",
        "password": "123",
        "fk_Rol": 4,
        "fk_Status": 1
    },
    {
        "first_name": "Marcela",
        "last_name": "García Pérez",
        "email": "marcela@teschi.edu.mx",
        "username": "marcela",
        "password": "123",
        "fk_Rol": 4,
        "fk_Status": 1
    },
    {
        "first_name": "Ricardo",
        "last_name": "Martínez González",
        "email": "ricardo@teschi.edu.mx",
        "username": "ricardo",
        "password": "123",
        "fk_Rol": 4,
        "fk_Status": 1
    },
    {
        "first_name": "Laura",
        "last_name": "Hernández Martín",
        "email": "laura@teschi.edu.mx",
        "username": "laura",
        "password": "123",
        "fk_Rol": 4,
        "fk_Status": 1
    },
    {
        "first_name": "Fernando",
        "last_name": "Sánchez García",
        "email": "fernando@teschi.edu.mx",
        "username": "fernando",
        "password": "123",
        "fk_Rol": 4,
        "fk_Status": 1
    },
    {
        "first_name": "Gabriela",
        "last_name": "Pérez Martínez",
        "email": "gabriela@teschi.edu.mx",
        "username": "gabriela",
        "password": "123",
        "fk_Rol": 4,
        "fk_Status": 1
    },
    {
        "first_name": "Jorge",
        "last_name": "López Martínez",
        "email": "jorge@teschi.edu.mx",
        "username": "jorge",
        "password": "123",
        "fk_Rol": 4,
        "fk_Status": 1
    },
    {
        "first_name": "Ana",
        "last_name": "Martín Pérez",
        "email": "ana@teschi.edu.mx",
        "username": "ana",
        "password": "123",
        "fk_Rol": 4,
        "fk_Status": 1
    },
    {
        "first_name": "Pablo",
        "last_name": "González Martínez",
        "email": "pablo@teschi.edu.mx",
        "username": "pablo",
        "password": "123",
        "fk_Rol": 4,
        "fk_Status": 1
    },
    {
        "first_name": "Carolina",
        "last_name": "Sánchez Pérez",
        "email": "carolina@teschi.edu.mx",
        "username": "carolina",
        "password": "123",
        "fk_Rol": 4,
        "fk_Status": 1
    },
    {
        "first_name": "Miguel",
        "last_name": "Gómez Pérez",
        "email": "miguel@teschi.edu.mx",
        "username": "miguel",
        "password": "123",
        "fk_Rol": 4,
        "fk_Status": 1
    },
    {
        "first_name": "Valeria",
        "last_name": "Martínez López",
        "email": "valeria@teschi.edu.mx",
        "username": "valeria",
        "password": "123",
        "fk_Rol": 4,
        "fk_Status": 1
    },
    {
        "first_name": "Héctor",
        "last_name": "González Rodríguez",
        "email": "hector@teschi.edu.mx",
        "username": "hector",
        "password": "123",
        "fk_Rol": 4,
        "fk_Status": 1
    },
    {
        "first_name": "Daniela",
        "last_name": "Pérez López",
        "email": "daniela@teschi.edu.mx",
        "username": "daniela",
        "password": "123",
        "fk_Rol": 4,
        "fk_Status": 1
    },
    {
        "first_name": "Oscar",
        "last_name": "Sánchez Martínez",
        "email": "oscar@teschi.edu.mx",
        "username": "oscar",
        "password": "123",
        "fk_Rol": 4,
        "fk_Status": 1
    }
]
datoPeriodo = {
    'Periodo': '0000-0',
    'fk_Status': 4
}
datosMateria = [
    {
        'Materia': 'Teoría General de la Administración',
        'Clave': 'TEOAD',
        'No_creditos': 4
    },
    {
        'Materia': 'Informática para la Administración',
        'Clave': 'INAD',
        'No_creditos': 5
    },
    {
        'Materia': 'Taller de Ética',
        'Clave': 'TALLET',
        'No_creditos': 4
    },
    {
        'Materia': 'Función Administrativa I',
        'Clave': 'FUADI',
        'No_creditos': 5
    },
    {
        'Materia': 'Estadística para la Administración I',
        'Clave': 'ESADI',
        'No_creditos': 5
    },
    {
        'Materia': 'Derecho Laboral y Seguridad Social',
        'Clave': 'DERLS',
        'No_creditos': 5
    },
    {
        'Materia': 'Función Administrativa II',
        'Clave': 'FUADII',
        'No_creditos': 5
    },
    {
        'Materia': 'Estadística para la Administración II',
        'Clave': 'ESADII',
        'No_creditos': 5
    },
    {
        'Materia': 'Derecho Empresarial',
        'Clave': 'DEREMP',
        'No_creditos': 5
    },
]
datosGrupo = [
    {
        'Grupo': '1LA11'
    },
    {
        'Grupo': '2LA11'
    },
    {
        'Grupo': '3LA11'
    },
]

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
for datoMateria in datosMateria:
    createMateria = Materia(**datoMateria)
    createMateria.save()
print("Materias insertadas correctamente.")
for datoGrupo in datosGrupo:
    createGrupo = Grupo(**datoGrupo)
    createGrupo.save()
print("Grupos insertados correctamente.")