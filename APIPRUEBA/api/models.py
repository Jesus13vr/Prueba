from django.db import models

# Create your models here.
class usuario(models.Model):
    idUsu=models.CharField(max_length=20,primary_key=True, db_column='idCliente')
    nom=models.CharField(max_length=50,db_column='nombre')
    pas=models.CharField(max_length=50,db_column='password')
    class Meta:
        db_table='Usuario'
class Encuestadesatisfaccion(models.Model):
    marcatemporal=models.TextField(db_column='Marca temporal')
    correo=models.TextField(db_column='Dirección de correo electrónico')
    p1=models.TextField(db_column='El sistema de administración de calificaciones es fácil de usar y comprender')
    p2=models.TextField(db_column='La información proporcionada por el sistema es útil y oportuna para la toma de decisiones')
    p3=models.TextField(db_column='La generación de informes estadísticos es eficiente y útil')
    p4=models.TextField(db_column='Qué tan útil es la retroalimentación proporcionada por los maestros junto con las calificaciones')
    p5=models.TextField(db_column='En qué medida crees que el sistema ha reducido el tiempo necesario para generar informes estadísticos')
    p6=models.TextField(db_column='Cuál de las siguientes funcionalidades consideras más importante en el sistema')
    p7=models.TextField(db_column='Qué tan satisfecho/a estás con la capacitación recibida para utilizar el sistema')
    p8=models.TextField(db_column='El sistema ha mejorado la transparencia y la comunicación con los estudiantes')
    p9=models.TextField(db_column='Qué tan confiable consideras que es la información proporcionada por el sistema de calificaciones')
    p10=models.TextField(db_column='Cuál es tu grado de satisfacción general con el proyecto de administración')
    class Meta:
        db_table = 'Encuestadesatisfaccion'