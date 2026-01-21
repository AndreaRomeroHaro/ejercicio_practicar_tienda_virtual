from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth import logout

class ProductoListView(LoginRequiredMixin,ListView):
    model=Producto
    context_object_name='productos'
    template_name='tienda/listado_productos.html'

class ProductoDetailView(DetailView):
    model=Producto
    context_object_name='producto'
    template_name='tienda/detalle_producto.html'

class ProductoCreateView(CreateView):
    model=Producto
    form_class=ProductoForm
    context_object_name='producto'
    template_name='tienda/crear_producto.html'
    success_url=reverse_lazy('listado_productos')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class ProductoUpdateView(UpdateView):
    model=Producto
    form_class=ProductoForm
    context_object_name='producto'
    template_name='tienda/editar_producto.html'
    success_url=reverse_lazy('listado_productos')

class ProductoDeleteView(DeleteView):
    model=Producto
    context_object_name='producto'
    template_name='tienda/eliminar_producto.html'
    success_url=reverse_lazy('listado_productos')

class CompraListView(LoginRequiredMixin,ListView):
    model=Compra
    context_object_name='compra'
    template_name='tienda/listado_compra.html'

    def get_queryset(self):
        producto=Producto.objects.filter(usuario=self.request.user)
        self.form=FiltroProductoForm(self.request.GET)
        if self.form.is_valid():
            nombre=self.form.cleaned_data('nombre')
            marca=self.form.cleaned_data('marca')
            modelo=self.form.cleaned_data('modelo')
            precio=self.form.cleaned_data('precio')
            vip=self.form.cleaned_data('vip')
            if nombre:
                producto=producto.filter(nombre=nombre)
            if marca:
                producto=producto.filter(marca=marca)
            if modelo:
                producto=producto.filter(modelo=modelo)
            if precio:
                producto=producto.filter(precio=precio)
            if vip:
                producto=producto.filter(vip=vip)
        return producto
    def get_context_data(self, **kwargs):
        contexto=super().get_context_data(**kwargs)
        contexto['formulario_filtro']=self.form
        return contexto
    
class CheckoutCompra(DetailView):
    model=Compra
    context_object_name='compra'
    template_name='tienda/checkout_compra.html'

def logout_view(request):
    logout(request)
    return render(request,'registration/logged_out.html')