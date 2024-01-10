from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.
#base de datos 
# models.py

class Rol(models.Model):
    id_Rol = models.AutoField(primary_key=True)
    Descripción = models.CharField(max_length=45)

    class Meta:
        db_table = 'Rol'

class Jefa(models.Model):
    id_Jefa = models.AutoField(primary_key=True)
    Rol_id_Rol = models.ForeignKey(Rol, on_delete=models.DO_NOTHING)
    usuario= models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table = 'Jefa'

class Alumno(models.Model):
    idAlumno = models.AutoField(primary_key=True)
    Rol_id_Rol = models.ForeignKey(Rol, on_delete=models.DO_NOTHING)
    usuario= models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        db_table = 'Alumno'

class Materia(models.Model):
    idMateria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    semestre = models.CharField(max_length=45)
    creditos = models.IntegerField()

    class Meta:
        db_table = 'Materia'
class Periodo(models.Model):
    idPeriodo = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField(default='2024-01-01', null=False)
    fecha_fin = models.DateField(default='2024-01-02', null=False)
    class Meta:
        db_table = 'Periodo'
class Seguimiento(models.Model):
    idSeguimiento = models.AutoField(primary_key=True)
    parcial = models.CharField(max_length=45)
    Periodo_idPeriodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    class Meta:
        db_table = 'Seguimiento'

class Docente(models.Model):
    idDocente = models.AutoField(primary_key=True)
    Rol_id_Rol = models.ForeignKey(Rol, on_delete=models.DO_NOTHING)
    usuario= models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        db_table = 'Docente'

