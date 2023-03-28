# Generated by Django 4.1.7 on 2023-03-20 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0048_alter_productos_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='tipoBeneficio',
            field=models.CharField(choices=[('Donación', 'Donación'), ('Prestamo', 'Prestamo')], default='Donación', max_length=25, verbose_name='Tipo de Beneficio'),
        ),
    ]