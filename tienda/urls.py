from django.urls import path
from . import views
from .views import *

urlpatterns=[
    path('admin/productos/listado',ProductoListView.as_view(),name='listado_productos'),
    path('admin/productos/detalle/<int:pk>',ProductoDetailView.as_view(),name='detalle_producto'),
    path('admin/productos/nuevo',ProductoCreateView.as_view(),name='crear_producto'),
    path('admin/productos/edicion/<int:pk>',ProductoUpdateView.as_view(),name='editar_producto'),
    path('admin/productos/eliminar/<int:pk>',ProductoDeleteView.as_view(),name='eliminar_producto'),
    path('compra',CompraListView.as_view(),name='listado_compra'),
    path('checkout/<int:pk>',CheckoutCompra.as_view(),name='checkout_compra'),
    path('informes',Informe_tienda.as_view(),name='informe_tienda'),
    path('cerrar_sesion/',views.logout_view,name='logout_salir'),
]