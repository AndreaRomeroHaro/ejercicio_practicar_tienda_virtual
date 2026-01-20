from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth import logout

class ProductoListView(LoginRequiredMixin,ListView):
    model=Producto
    context_object_name='productos'
    template_name='tienda/listados_productos.html'

class ProductoDetailView(DetailView):
    model=Producto
    context_object_name='producto'
    template_name='tienda/detalle_producto.html'

class ProductoCreateView(CreateView):
    model=Producto
    context_object_name='producto'
    template_name='tienda/crear_producto.html'

class ProductoUpdateView(UpdateView):
    model=Producto
    context_object_name='producto'
    template_name='tienda/editar_producto.html'

class ProductoDeleteView(DeleteView):
    model=Producto
    context_object_name='producto'
    template_name='tienda/eliminar_producto.html'

def logout_view(request):
    logout(request)
    return render(request,'registration/logged_out.html')