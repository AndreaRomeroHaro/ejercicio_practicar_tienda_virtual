from django.urls import path
from . import views
from .views import *

urlpatterns=[
    path('tienda/admin/productos/listado',ProductoListView.as_view(),name='listado_productos'),
    path('tienda/admin/productos/detalle/<int:pk>',ProductoDetailView.as_view(),name='detalle_producto'),
    path('tienda/admin/productos/nuevo',ProductoCreateView.as_view(),name='crear_producto'),
    path('tienda/admin/productos/edicion/<int:pk>',ProductoUpdateView.as_view(),name='editar_producto'),
    path('tienda/admin/productos/eliminar/<int:pk>',ProductoDeleteView.as_view(),name='eliminar_producto'),
    path('tienda/compra',CompraListView.as_view(),name='listado_compra'),
    path('tienda/checkout',CheckoutCompra.as_view(),name='checkout_compra'),
    path('cerrar_sesion/',views.logout_view,name='logout_salir'),
]