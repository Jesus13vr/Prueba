from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#base de datos 
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

class Seguimiento(models.Model):
    idSeguimiento = models.AutoField(primary_key=True)
    parcial = models.CharField(max_length=45)

    class Meta:
        db_table = 'Seguimiento'

class Docente(models.Model):
    idDocente = models.AutoField(primary_key=True)
    Rol_id_Rol = models.ForeignKey(Rol, on_delete=models.DO_NOTHING)
    usuario= models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        db_table = 'Docente'