# Generated by Django 4.1.6 on 2023-03-15 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0030_remove_autor_apellidos_alter_autor_nombres'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='stock',
            field=models.IntegerField(default=0, verbose_name='Stock'),
        ),
    ]
