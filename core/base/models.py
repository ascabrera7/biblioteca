from datetime import timedelta
from django.db import models
from datetime import datetime
from core.base.choices import gender_choices
from django.forms import model_to_dict
from core.user.models import User
from inventario.settings import MEDIA_URL, STATIC_URL
from core.base.choices import gender_choices
from django.db.models.signals import post_save,pre_save


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
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoría")
    imagen = models.ImageField(upload_to='productos/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    
    stock = models.PositiveIntegerField(default=1, verbose_name='Cantidad o Stock')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=0, verbose_name="Precio")
    estado = models.BooleanField(default = True, verbose_name = 'Donación(si) Préstamo(No)')


    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = '{} / {}'.format(self.nombre, self.categoria.nombre)
        item['categoria'] = self.categoria.toJSON()
        item['imagen'] = self.get_imagen()
        item['pvp'] = format(self.pvp, '.2f')
        return item

    
    def get_imagen(self):
        if self.imagen:
            return  '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')


    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


class Beneficiario(models.Model):
    nombres = models.CharField(max_length=150, verbose_name='Nombres')
    apellidos = models.CharField(max_length=150, verbose_name='Apellidos')
    class TipoDocumento(models.TextChoices):
        RC='Registro Civil', ('Registro Civil')
        TI='Tarjeta de Identidad', ('Tarjeta de Identidad')
        CC='Cédula de Ciudadanía', ('Cédula de Ciudadanía')
        CE='Cédula de Extrajería', ('Cédula de Extrajería')
        CR='Contraseña Registraduría', ('Contraseña Registraduria')
    tipoDocumento=models.CharField(max_length=25, choices=TipoDocumento.choices, default=TipoDocumento.RC, verbose_name="Tipo de Documento")
    documento = models.IntegerField( unique=True, verbose_name='Documento',null=True,blank=True,)
    cumpleaños = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    telefono=models.IntegerField( verbose_name="Teléfono", null=True,blank=True)
    class Tipo(models.TextChoices):
        LECTOR='Beneficiario', ('Beneficiario')
    tipo=models.CharField(max_length=25, choices=Tipo.choices, default=Tipo.LECTOR, verbose_name="Tipo")
    
    class Zona(models.TextChoices):
        URBANA='Urbana',('Urbana')
        RURAL='Rural',('Rural')
    zona=models.CharField(max_length=25, choices=Zona.choices, default=Zona.URBANA, verbose_name="Zona")
    direccion = models.CharField(max_length=150, null=True, blank=True, verbose_name='Direccion')
    barrio = models.CharField(max_length=150, verbose_name='Barrio',null=True,blank=True)
    class Gender(models.TextChoices):
        FEMENINO='Femenino',('Femenino')
        MASCULINO='Masculino',('Masculino')
    gender=models.CharField(max_length=25, choices=Gender.choices, default=Gender.FEMENINO, verbose_name="Genero")
    
    def __str__(self):
        return self.nombres
    
    def get_full_name(self):
        return '{} {} / {}'.format(self.nombres, self.apellidos, self.documento)

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
    
    def delete(self, using=None, keep_parents=False):
        for det in self.detallesuministro_set.all():
            det.producto.stock += det.cantidad
            det.producto.save()
        super(Suministro, self).delete()
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
    nombres = models.CharField('Nombres y Apellidos',max_length = 45, blank = False, null = False)
    nacionalidad = models.CharField(max_length = 50, blank = False, null = False)
    descripcion = models.TextField( blank = False, null = False, verbose_name="Descripción")
    fecha_creacion = models.DateField(default=datetime.now)
    estado = models.BooleanField(default = True, verbose_name = 'Estado')

    def __str__(self):  
        return self.nombres
    
    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_creacion'] = self.fecha_creacion.strftime('%Y-%m-%d')
        return item
    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['id']
    

class Eventos(models.Model):
    id = models.AutoField(primary_key = True)
    nombre =models.CharField(max_length = 50, blank = False, null = False)
    tipoEvento =models.CharField(max_length = 50, blank = False, null = False)
    fecha = models.DateTimeField(default=datetime.now, verbose_name='Fecha y Hora')
    ubicacion = models.CharField('Ubicación',max_length = 50,null=True, blank=True)
    descripcion = models.TextField('Descripción',null=True, blank=True)
    imagen = models.ImageField(upload_to='Eventos/',max_length=255, null=True, blank=True, verbose_name='Imagen')
    estado = models.BooleanField(default = True, verbose_name = 'Activo(Si) Inactivo(No)')


    def natural_key(self):
        return self.nombre
    
    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['imagen'] = self.get_imagen()
        return item
    
    def get_imagen(self):
        if self.imagen:
            return  '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    
class Libro(models.Model):
    titulo = models.CharField(max_length = 45, blank = False, null = False)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    f_publicacion = models.DateField(default=datetime.now, verbose_name='Fecha de Publicación')
    genero = models.CharField(max_length = 45, blank = True, null = True)
    descripcion = models.TextField('Descripción',null=True, blank=True)
    cantidad = models.PositiveIntegerField('Cantidad o Stock',default = 1)
    imagen = models.ImageField(upload_to='libros/',max_length=255, null=True, blank=True, verbose_name='Imagen')
    estado = models.BooleanField(default = True, verbose_name = 'Estado')

    def natural_key(self):
        return self.titulo
    
    def __str__(self):
        return self.titulo
    
    def toJSON(self):
        item = model_to_dict(self)
        item['autor'] = self.autor.toJSON()
        item['f_publicacion'] = self.f_publicacion.strftime('%Y-%m-%d')
        item['imagen'] = self.get_imagen()
        return item
    
    def get_imagen(self):
        if self.imagen:
            return  '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')
    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['id']
    


class Lector(models.Model):
    nombres = models.CharField(max_length=150, verbose_name='Nombres')
    apellidos = models.CharField(max_length=150, verbose_name='Apellidos')
    class TipoDocumento(models.TextChoices):
        RC='Registro Civil', ('Registro Civil')
        TI='Tarjeta de Identidad', ('Tarjeta de Identidad')
        CC='Cédula de Ciudadanía', ('Cédula de Ciudadanía')
        CE='Cédula de Extrajería', ('Cédula de Extrajería')
        CR='Contraseña Registraduría', ('Contraseña Registraduria')
    tipoDocumento=models.CharField(max_length=25, choices=TipoDocumento.choices, default=TipoDocumento.RC, verbose_name="Tipo de Documento")
    documento = models.IntegerField( unique=True, verbose_name='Documento',null=True,blank=True,)
    cumpleaños = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    telefono=models.IntegerField( verbose_name="Teléfono", null=True,blank=True)
    class Zona(models.TextChoices):
        URBANA='Urbana',('Urbana')
        RURAL='Rural',('Rural')
    zona=models.CharField(max_length=25, choices=Zona.choices, default=Zona.URBANA, verbose_name="Zona")
    direccion = models.CharField(max_length=150, null=True, blank=True, verbose_name='Direccion')
    barrio = models.CharField(max_length=150, verbose_name='Barrio',null=True,blank=True)
    class Gender(models.TextChoices):
        FEMENINO='Femenino',('Femenino')
        MASCULINO='Masculino',('Masculino')
    gender=models.CharField(max_length=25, choices=Gender.choices, default=Gender.FEMENINO, verbose_name="Genero")
    
    def __str__(self):
        return self.nombres
    
    def get_full_name(self):
        return '{} {} / {}'.format(self.nombres, self.apellidos, self.documento)

    def toJSON(self):
        item = model_to_dict(self)
        item['cumpleaños'] = self.cumpleaños.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Lector'
        verbose_name_plural = 'Lectores'
        ordering = ['id']


    
class Reserva(models.Model):
    
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, null=True, blank=True)
    lector = models.ForeignKey(Lector, on_delete=models.CASCADE, null=True, blank=True)
    fecha9 = models.DateField(default=datetime.now, verbose_name='Fecha')
    fecha8 = models.DateField(default=datetime.now, verbose_name='Fecha')
    estado = models.BooleanField(default = True, verbose_name = ' Entregada(Si) Recibido(No)')


    def toJSON(self):
        item = model_to_dict(self)
        item['full_nombre'] = '{} / {}'.format(self.lector.nombres, self.lector.apellidos, self.lector.documento )
        item['libro'] = self.libro.toJSON()
        item['lector'] = self.lector.toJSON()
        item['fecha9'] = self.fecha9.strftime('%Y-%m-%d')
        item['fecha8'] = self.fecha8.strftime('%Y-%m-%d')
        
        return item
    

def reducir_cantidad_libro(sender,instance,**kwargs):
    libro = instance.libro
    if libro.cantidad > 0:
        libro.cantidad = libro.cantidad - 0
        libro.save()


post_save.connect(reducir_cantidad_libro,sender = Reserva)




