# Generated by Django 3.2.4 on 2023-10-19 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encuestadesatisfaccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marcatemporal', models.TextField(db_column='Marca temporal')),
                ('correo', models.TextField(db_column='Dirección de correo electrónico')),
                ('p1', models.TextField(db_column='El sistema de administración de calificaciones es fácil de usar y comprender')),
                ('p2', models.TextField(db_column='La información proporcionada por el sistema es útil y oportuna para la toma de decisiones')),
                ('p3', models.TextField(db_column='La generación de informes estadísticos es eficiente y útil')),
                ('p4', models.TextField(db_column='Qué tan útil es la retroalimentación proporcionada por los maestros junto con las calificaciones')),
                ('p5', models.TextField(db_column='En qué medida crees que el sistema ha reducido el tiempo necesario para generar informes estadísticos')),
                ('p6', models.TextField(db_column='Cuál de las siguientes funcionalidades consideras más importante en el sistema')),
                ('p7', models.TextField(db_column='Qué tan satisfecho/a estás con la capacitación recibida para utilizar el sistema')),
                ('p8', models.TextField(db_column='El sistema ha mejorado la transparencia y la comunicación con los estudiantes')),
                ('p9', models.TextField(db_column='Qué tan confiable consideras que es la información proporcionada por el sistema de calificaciones')),
                ('p10', models.TextField(db_column='Cuál es tu grado de satisfacción general con el proyecto de administración')),
            ],
            options={
                'db_table': 'Encuestadesatisfaccion',
            },
        ),
    ]