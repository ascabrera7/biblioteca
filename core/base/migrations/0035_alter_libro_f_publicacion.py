# Generated by Django 4.1.6 on 2023-03-17 15:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0034_autor_fecha_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='f_publicacion',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Fecha de Publicacion'),
        ),
    ]
