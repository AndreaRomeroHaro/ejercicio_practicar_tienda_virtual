from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,View
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
    model=Producto
    form=FiltroProductoForm
    context_object_name='productos'
    template_name='compra/listado_compra.html'

    def get_context_data(self, **kwargs):
        contexto=super().get_context_data(**kwargs)
        contexto['formulario_filtro']=self.form
        return contexto
    
class CheckoutCompra(LoginRequiredMixin,View):

    def get(self,request,pk):
        producto=get_object_or_404(Producto,pk=pk)
        return render(request,'compra/checkout_compra.html',{producto:'producto'})
    
    def post(self,request,pk):
        producto=get_object_or_404(Producto,pk=pk)
        unidades_compradas=request.POST.get('unidades')
        iva_elegido=request.POST.get('iva')
        Compra.objects.create(usuario=request.user,producto=producto,unidades=unidades_compradas,iva=iva_elegido)
        producto.unidades=-unidades_compradas
        producto.save()
        messages.success(request, f"Has comprado {unidades_compradas} unidades de {producto.nombre}")
        return redirect('listado_productos')

def logout_view(request):
    logout(request)
    return render(request,'registration/logged_out.html')