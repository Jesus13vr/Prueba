from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.
#base de datos 
# models.py

class Rol(models.Model):
    id_Rol = models.AutoField(primary_key=True,db_column='Id_Rol')
    Rol = models.CharField(unique=True,max_length=20,default='Rol',db_column='Rol')
    class Meta:
        db_table='Rol'

class Status(models.Model):
    id_Status = models.AutoField(primary_key=True,db_column='id_Status')
    Status = models.CharField(unique=True,max_length=15,default='Status',db_column='Status')
    class Meta:
        db_table='Status'
        
class CustomUser(AbstractUser):
    fk_Rol = models.ForeignKey(Rol,null=False,on_delete=models.PROTECT,db_column='fk_Rol')
    fk_Status = models.ForeignKey(Status,null=False,on_delete=models.PROTECT,db_column='fk_Status')
    def __str__(self):
        return self.username

class Materia(models.Model):
    id_Materia = models.AutoField(primary_key=True,db_column='id_Materia')
    Materia = models.CharField(max_length=45,default='Materia',db_column='Materia')
    Clave = models.CharField(unique=True,max_length=10,default='Clave',db_column='Clave')
    No_creditos = models.IntegerField(default=1,db_column='No_creditos')
    class Meta:
        db_table='Materia'

class Grupo(models.Model):
    id_Grupo = models.AutoField(primary_key=True,db_column='id_Grupo')
    Grupo = models.CharField(unique=True,max_length=10,default='Grupo',db_column='Grupo')
    class Meta:
        db_table='Grupo'

class Periodo(models.Model):
    id_Periodo = models.AutoField(primary_key=True,db_column='id_Periodo')
    Periodo = models.CharField(unique=True,max_length=10,default='Periodo',db_column='Periodo')
    fk_Status = models.ForeignKey(Status,null=False,on_delete=models.PROTECT,db_column='fk_Status')
    class Meta:
        db_table='Periodo'
        
class Asignacion(models.Model):
    id_Asignacion = models.AutoField(primary_key=True,db_column='id_Asignacion')
    fk_Alumno = models.ForeignKey(CustomUser,on_delete=models.PROTECT,related_name='asignacion_alumno',db_column='fk_Alumno')
    fk_Materia = models.ForeignKey(Materia, on_delete=models.PROTECT,db_column='fk_Materia')
    fk_Grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT,db_column='fk_Grupo')
    fk_Periodo = models.ForeignKey(Periodo, on_delete=models.PROTECT,db_column='fk_Periodo')
    fk_Docente = models.ForeignKey(CustomUser, on_delete=models.PROTECT,related_name='asignacion_docente',db_column='fk_Docente')
    class Meta:
        db_table='Asignacion'
        
class Calificacion(models.Model):
    id_Calificacion = models.AutoField(primary_key=True,db_column='id_Calificacion')
    fk_Asignacion = models.ForeignKey(Asignacion, on_delete=models.PROTECT,db_column='fk_Asignacion')
    Parcial_1 = models.FloatField(default=0.0,db_column='Parcial_1')
    Parcial_2 = models.FloatField(default=0.0,db_column='Parcial_2')
    Parcial_3 = models.FloatField(default=0.0,db_column='Parcial_3')
    class Meta:
        db_table='Calificacion'
