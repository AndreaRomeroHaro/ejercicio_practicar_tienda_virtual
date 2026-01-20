from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):

    class Meta:
        verbose_name="Usuario"
        verbose_name_plural="Usuarios"
    
    producto=models.ManyToManyField('Producto',through='Producto')
    vip=models.BooleanField(default=False)
    saldo=models.DecimalField(blank=True,null=True)

    def __str__(self):
        return f"{self.username}"
    
class Marca(models.Model):

    class Meta:
        verbose_name="Marca"
        verbose_name_plural="Marcas"
    
    nombre=models.CharField(max_length=100,unique=True)

class Producto(models.Model):

    class Meta:
        verbose_name="Producto"
        verbose_name_plural="Productos"

    nombre=models.CharField(max_length=100)
    marca=models.ForeignKey(Marca,on_delete=models.CASCADE)
    modelo=models.CharField(blank=True)
    unidades=models.FloatField()
    precio=models.DecimalField(default=0.0)
    vip=models.BooleanField(default=False)
    foto = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.precio}€"
    
class Compra(models.Model):
    
    class IVA(models.IntegerChoices):
        GENERAL='21%',0,21
        REDUCIDO='10%',0.10
        SUPERREDUCIDO='4%',0.04

    class Meta:
        verbose_name="Compra"
        verbose_name_plural="Compras"
        unique_together=('producto','usuario')
    
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    fecha=models.DateTimeField(auto_now=True)
    unidades=models.IntegerField()
    importe=models.DecimalField(default=0.0)
    iva=models.CharField(max_length=2,choices=IVA.choices(default=IVA.GENERAL))

    def __str__(self):
        return f"{self.producto.nombre} - Unidades: {self.unidades} - Importe: {self.unidades}"