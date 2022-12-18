from django.urls import path
from django.views.generic import TemplateView
from .views import *
urlpatterns = [
    path('inicio_autores/',TemplateView.as_view(template_name = 'libro/autor/listar_autor.html'),name='inicio_autores'),
    path('listado_autor/',ListadoAutor.as_view(), name = 'listar_autor'),
     path('crear_autor/',CrearAutor.as_view(), name = 'crear_autor'),
    path('editar_autor/<int:pk>/',ActualizarAutor.as_view(), name = 'editar_autor'),
     path('eliminar_autor/<int:pk>/',EliminarAutor.as_view(), name = 'eliminar_autor'),

    path('listado_libros/', ListadoLibros.as_view(), name = 'listado_libros'),
    path('crear_libro/',CrearLibro.as_view(), name = 'crear_libro'),
    path('editar_libro/<int:pk>/', ActualizarLibro.as_view(), name = 'editar_libro'),
    path('eliminar_libro/<int:pk>/', EliminarLibro.as_view(), name = 'eliminar_libro'),


    path('listado-libros-disponibles/',ListadoLibrosDisponibles.as_view(), name = 'listado_libros_disponibles'),
    path('detalle-libro/<int:pk>/',DetalleLibroDiponible.as_view(), name = 'detalle_libro'),
    path('reservar-libro/',RegistrarReserva.as_view(), name = 'reservar_libro'),
    path('listado-libros-reservados/',ListadoLibrosReservados.as_view(), name = 'listado_libros_reservados'),
    path('reservas/',Reservas.as_view(), name = 'reservas'),
    path('listado-reservas-vencidas/',ListadoReservasVencias.as_view(), name = 'listado_reservas_vencidas'),
    path('reservas-vencidas/',ReservasVencidas.as_view(), name = 'reservas_vencidas'),
    # path('detalle-libro/<int:pk>/',DetalleLibroDiponible.as_view(), name = 'detalle_libro'),
    # path('reservar-libro/',RegistrarReserva.as_view(), name = 'reservar_libro'),
]
