# Generated by Django 3.2.4 on 2024-01-08 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20231122_1524'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rol',
            old_name='Descripción',
            new_name='Descripcion',
        ),
    ]
