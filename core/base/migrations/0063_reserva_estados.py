# Generated by Django 4.1.7 on 2023-04-08 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0062_remove_reserva_beneficiario_reserva_lector'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='estados',
            field=models.CharField(choices=[('Entregado', 'Entregado'), ('Recibido', 'Ricibido')], default='Entregado', max_length=25, verbose_name='Zona'),
        ),
    ]
