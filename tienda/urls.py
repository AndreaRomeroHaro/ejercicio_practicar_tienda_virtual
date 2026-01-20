from django.urls import path
from . import views
from .views import *

urlpatterns=[
    path('tienda/admin/producto',ProductoListView.as_view(),name='listado_productos'),
    path('detalle/',ProductoDetailView.as_view(),name='detalle_producto'),
    path('crear/',ProductoCreateView.as_view(),name='crear_producto'),
    path('editar/',ProductoUpdateView.as_view(),name='editar_producto'),
    path('eliminar/',ProductoDeleteView.as_view(),name='eliminar_producto'),
    path('cerrar_sesion/',views.logout_view,name='logout_salir'),
]