from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,View
from django.contrib.auth import logout
from django.db.models import Sum

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
    context_object_name='productos'
    template_name='compra/listado_compra.html'

    def get_queryset(self):
        productos=Producto.objects.all()
        self.form=FiltroProductoForm(self.request.GET)
        if self.form.is_valid():
            nombre=self.form.cleaned_data.get('nombre')
            marca=self.form.cleaned_data.get('marca')
            modelo=self.form.cleaned_data.get('modelo')
            precio=self.form.cleaned_data.get('precio')
            vip=self.form.cleaned_data.get('vip')
            if nombre:
                productos=productos.filter(nombre__icontains=nombre)
            if marca:
                productos=productos.filter(marca__nombre__icontains=marca)
            if modelo:
                productos=productos.filter(modelo=modelo)
            if precio:
                productos=productos.filter(precio__lte=precio)
            if vip:
                productos=productos.filter(vip=True)
        return productos
    
    def get_context_data(self, **kwargs):
        contexto=super().get_context_data(**kwargs)
        contexto['formulario_filtro']=self.form
        return contexto
    
class CheckoutCompra(LoginRequiredMixin,View):

    def get(self,request,pk):
        producto=get_object_or_404(Producto,pk=pk)
        tipo_iva=Compra.IVA.choices
        contexto={'producto':producto,'tipos_iva':tipo_iva}
        return render(request,'compra/checkout_compra.html',contexto)
    
    def post(self,request,pk):
        producto=get_object_or_404(Producto,pk=pk)
        try:
            unidades=int(request.POST.get('unidades'))
            iva=int(request.POST.get('iva'))
            compra=Compra(usuario=request.user,producto=producto,unidades=unidades,iva=iva)
            compra.full_clean()
            compra.save()
            return redirect('listado_productos')
        except ValidationError as e:
            messages.error(request,e.messages[0])
            return redirect('checkout_compra',pk=pk)
        
class Informe_tienda(LoginRequiredMixin,View):

    def get(self,request):
        #productos por marca
        marcas=Marca.objects.all()
        marca_seleccionada=request.GET.get('marca_id')
        productos=[]
        marca_actual=None
        if marca_seleccionada:
            productos=Producto.objects.filter(marca_id=marca_seleccionada)
            marca_actual=Marca.objects.get(id=marca_seleccionada)
        
        #diez productos más vendidos
        top_productos=Producto.objects.annotate(total_vendida=Sum('ventas__unidades')).order_by('-total_vendida')[:10]
        
        #compras de un usuario
        compras=Compra.objects.filter(usuario=self.request.user)

        #diez mejores clientes
        top_clientes=Usuario.objects.annotate(total_gastado=Sum('compra__importe')).order_by('-total_gastado')[:10]
        
        contexto={'marcas':marcas,'productos':productos,'marca_actual':marca_actual,'top_productos':top_productos,'compras':compras,'top_clientes':top_clientes}
        return render(request,'informe/informe_tienda.html',contexto)


def logout_view(request):
    logout(request)
    return render(request,'registration/logged_out.html')