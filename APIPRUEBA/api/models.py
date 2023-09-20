from django.db import models

# Create your models here.
class usuario(models.Model):
    idUsu=models.CharField(max_length=20,primary_key=True, db_column='idCliente')
    nom=models.CharField(max_length=50,db_column='nombre')
    pas=models.CharField(max_length=50,db_column='password')
    class Meta:
        db_table='Usuario'