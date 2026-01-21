from django import forms
from .models import *

class ProductoForm(forms.ModelForm):
    class Meta:
        model=Producto
        fields=['nombre','marca','modelo','unidades','precio','vip','foto']

class FiltroProductoForm(forms.Form):
    nombre=forms.CharField(required=False)
    marca=forms.CharField(required=False)
    modelo=forms.CharField(required=False)
    precio=forms.DecimalField(required=False)
    vip=forms.BooleanField(required=False)
