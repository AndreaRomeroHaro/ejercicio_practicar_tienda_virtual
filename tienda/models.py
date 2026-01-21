from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):

    class Meta:
        verbose_name="Usuario"
        verbose_name_plural="Usuarios"
    
    producto=models.ManyToManyField('Producto',through='Compra')
    vip=models.BooleanField(default=False)
    saldo=models.DecimalField(max_digits=12,decimal_places=2,blank=True,null=True)

    def __str__(self):
        return f"{self.username}"
    
class Marca(models.Model):

    class Meta:
        verbose_name="Marca"
        verbose_name_plural="Marcas"
    
    nombre=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return f"{self.nombre}"

class Producto(models.Model):

    class Meta:
        verbose_name="Producto"
        verbose_name_plural="Productos"

    nombre=models.CharField(max_length=100)
    marca=models.ForeignKey(Marca,on_delete=models.CASCADE)
    modelo=models.CharField(max_length=100,blank=True)
    unidades=models.FloatField()
    precio=models.DecimalField(max_digits=12,decimal_places=2,default=0.0)
    vip=models.BooleanField(default=False)
    foto = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.precio}€"
    
class Compra(models.Model):
    
    class IVA(models.IntegerChoices):
        GENERAL=21,'General (21%)'
        REDUCIDO=10,'Reducido(10%)'
        SUPERREDUCIDO=4,'Superreducido(4%)'

    class Meta:
        verbose_name="Compra"
        verbose_name_plural="Compras"
    
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    fecha=models.DateTimeField(auto_now=True)
    unidades=models.IntegerField()
    importe=models.DecimalField(max_digits=12,decimal_places=2,default=0.0)
    iva=models.IntegerField(choices=IVA.choices,default=IVA.GENERAL)

    def save(self,*args,**kwargs):
        base=self.producto.precio*self.unidades
        porcentaje=self.IVA/100
        resultado=base*(1+porcentaje)
        self.importe=resultado
        return super().save(*args,**kwargs)
    
    def __str__(self):
        return f"{self.producto.nombre} - Unidades: {self.unidades} - Importe: {self.importe}"