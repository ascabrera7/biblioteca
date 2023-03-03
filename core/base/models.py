from django.db import models
from datetime import datetime
from core.base.choices import gender_choices
from django.forms import model_to_dict
from inventario.settings import MEDIA_URL, STATIC_URL
from core.base.choices import gender_choices


class Categoria(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    descripcion = models.CharField(max_length=150, null=True, blank=True, verbose_name='Descripción') 

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

class Productos(models.Model): 
    nombre = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=0)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = self.categoria.toJSON()
        item['imagen'] = self.get_imagen()
        item['pvp'] = format(self.pvp, '.2f')
        return item

    
    def get_imagen(self):
        if self.imagen:
            return  '{}{}'.format(STATIC_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')


    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


class Beneficiario(models.Model):
    nombres = models.CharField(max_length=150, verbose_name='Nombres')
    apellidos = models.CharField(max_length=150, verbose_name='Apellidos')
    cedula = models.CharField(max_length=10, unique=True, verbose_name='Cedula')
    cumpleaños = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    direccion = models.CharField(max_length=150, null=True, blank=True, verbose_name='Direccion')
    sexo = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')
    
    def __str__(self):
        return self.nombres
    
    def toJSON(self):
        item = model_to_dict(self)
        item['cumpleaños'] = self.cumpleaños.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Beneficiario'
        verbose_name_plural = 'Beneficiario'
        ordering = ['id']


class Suministro(models.Model):
    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)
    fecha_registro = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.beneficiario.nombres
    def toJSON(self):
        item = model_to_dict(self)
        item['beneficiario'] = self.beneficiario.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['total'] = format(self.total, '.2f')
        item['fecha_registro'] = self.fecha_registro.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detallesuministro_set.all()]
        return item
    
    class Meta:
        verbose_name = 'Suministro'
        verbose_name_plural = 'Suministros'
        ordering = ['id']


class DetalleSuministro(models.Model):
    suministro = models.ForeignKey(Suministro, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)


    def __str__(self):
        return self.producto.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['suministro'])
        item['producto'] = self.producto.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item
    class Meta:
        verbose_name = 'Detalle de Suministro'
        verbose_name_plural = 'Detalle de Suministros'
        ordering = ['id']

class Autor(models.Model):
    nombres = models.CharField(max_length = 45, blank = False, null = False)
    apellidos = models.CharField(max_length = 45, blank = False, null = False)
    nacionalidad = models.CharField(max_length = 50, blank = False, null = False)
    descripciones = models.TextField( blank = False, null = False)
    fecha_creacion = models.DateField('Fecha de creación', auto_now = True, auto_now_add = False)       

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['nombres']
    
    def toJSON(self):
        item = model_to_dict(self)
        return item
        
    def __str__(self):
        return self.nombres