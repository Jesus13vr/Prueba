# Generated by Django 3.2.4 on 2024-01-10 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodo',
            name='fecha_fin',
            field=models.DateField(default='2024-01-01'),
        ),
        migrations.AlterField(
            model_name='periodo',
            name='fecha_inicio',
            field=models.DateField(default='2024-01-01'),
        ),
    ]
