import json

from time import time
from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View,TemplateView,ListView,UpdateView,CreateView,DeleteView,DetailView
from django.urls import reverse_lazy
#from apps.usuario.mixins import LoginYSuperStaffMixin, ValidarPermisosMixin,LoginMixin
# from apps.usuario.models import Usuario
from .models import Autor ,Libro,Reserva
from .forms import AutorForm,LibroForm
from django.contrib.auth import get_user_model

user = get_user_model()


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class ListadoAutor(ListView):
    model = Autor
    #template_name = 'libro/autor/listar_autor.html'
    context_object_name = 'autores'
    
    

    def get_queryset(self):
        return  self.model.objects.filter(estado = True)

    def get(self,request,*args, **kwargs):
        #preguntamos si la peticion es ajax
        if is_ajax(request): #is_ajax esta en desuso en la version 4 de django osea no funciona
            # lista_autores = [] #creamos una lista vacia para meter cada uno de los registros que se obtengan de la consulta 
            # for autores in self.get_queryset():
            #     data_autores = {}
            #     data_autores['id'] = autores.id
            #     data_autores['nombre'] = autores.nombre
            #     data_autores['apellidos']= autores.apellidos
            #     data_autores['nacionalidad']= autores.nacionalidad
            #     data_autores['descripcion'] = autores.descripcion
            #     lista_autores.append(data_autores)
            #     #en este caso lista autores es una lista y no va a funcionar devemos comvertirla a json
            # data = json.dumps(lista_autores)
            # listo ahora como retorno este json necesitamos un httpresponse y definir igual que se retorna como una aplicacion json
            # return HttpResponse(data,'application/json')

            #Ctodo eso que hicimos pedomes hacerlo con serialize
            #primero espezificamos a que archivo combertir y luego que datos en este caso todos los que el estado sea true
            data = serializers.serialize('json', self.get_queryset())
            return HttpResponse(data,'application/json')
        else:
            return redirect('libro:inicio_autores')

class ActualizarAutor(UpdateView):
    model = Autor
    form_class = AutorForm
    template_name = 'libro/autor/autor.html'
    # permission_required = ('libro.view_autor', 'libro.add_autor',
    #                        'libro.delete_autor', 'libro.change_autor')
    
    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            #cuando usamos pk podemos optener la instancia actual que estamos utilizando con la funcion interna get_object osea django lo hace por nosotros namas la llamamos
            #osea instance es para saber cual debemos editar si el que tiene el id 3 o 6 por ejemplo 
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} actualizado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido actualizar!'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('libro:inicio_autor')

    


class CrearAutor(CreateView):
    model = Autor
    form_class = AutorForm
    template_name = 'libro/autor/crear_autor.html'
    # permission_required = ('libro.view_autor', 'libro.add_autor',
    #                        'libro.delete_autor', 'libro.change_autor')

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            form = self.form_class(request.POST)
            if form.is_valid():
                nuevo_autor = Autor(
                    nombre=form.cleaned_data.get('nombre'),
                    apellidos=form.cleaned_data.get('apellidos'),
                    nacionalidad=form.cleaned_data.get('nacionalidad'),
                    descripcion=form.cleaned_data.get('descripcion')
                )
                nuevo_autor.save()
                #aqui solo ponemos una variable con un mensaje model.__name__ es el nombre del modelo osea seria Autor registrado correctamente
                mensaje = f'{self.model.__name__} registrado correctamente!'
                #tombien un mensaje error y en este caso no hay error 
                error = 'No hay error!'
                #jsonresponse con este enviamos los mensajes y error por si queremos usarlos 
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                #y enviamos el codigo 201 pa decir que se a creado y es valido el formulario
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar!'
                #como estamos usando el form de django este trae ventajas y es que este ya trae errores predeterminados y solo es cuestion de mandarlos 
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                #y enviamos el codigo 400 que es la peticion no es valida y esto es culpa del cliente mas no del servidor
                response.status_code = 400
                return response
        else:
            return redirect('libro:inicio_autores')


class EliminarAutor(DeleteView):
    model = Autor
    template_name = 'libro/autor/eliminar_autor.html'
    # permission_required = ('libro.view_autor', 'libro.add_autor',
    #                        'libro.delete_autor', 'libro.change_autor')

    def delete(self,request,pk,*args,**kwargs):
        if is_ajax(request):
            autor = self.get_object()#optenemos el usuario actual
            autor.estado = False
            autor.save()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        return redirect('libro:listar_autor')


class ListadoLibros(View):
    model = Libro
    template_name = 'libro/libro/listar_libro.html'
    
    def get_queryset(self):
        return self.model.objects.filter(estado = True)

    def get_context_data(self, **kwargs):
        con = {}
        con['libros']= self.get_queryset()
        #podemos quitar este porque ahora usamos un modal 
        #con['form'] = LibroForm #envamos el formulario
        return con
        
    def get(self,request,*args, **kwargs):
        return render(request,self.template_name,self.get_context_data())

  #podemos quitar esta funcion ya que usamos un modal 
    # def post(self,request,*args, **kwargs):
    #     form = LibroForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('libro:listado_libros')


class CrearLibro(CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libro/libro/crear_libro.html'
    success_url = reverse_lazy('libro:listado_libros')

class ActualizarLibro(UpdateView):
    model = Libro
    template_name = 'libro/libro/libro.html'
    form_class = LibroForm
    success_url = reverse_lazy('libro:listado_libros')

    def get_context_data(self, **kwargs): 
        con = super().get_context_data(**kwargs) #aque redifinimos el contexto con todos los contextos que trae pordefecto por ejempol el form o el object
        con['libros']= Libro.objects.filter(estado = True)
        return con 


class EliminarLibro(DeleteView):
    model = Libro
   
    def post(self,request,pk,*args, **kwargs):
        object = Libro.objects.get(id=pk)
        object.estado = False
        object.save()
        return redirect('libro:listado_libros')



class ListadoLibrosDisponibles(ListView):
    model = Libro
    paginate_by = 1
    template_name = 'libro/libros_disponibles.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(estado = True,cantidad__gte = 1)#gte es para mostrar los libros que tengan una cantidad minima de una gte es mayor o igual que 
        return queryset


class DetalleLibroDiponible(DetailView):
    model = Libro
    template_name = 'libro/detalle_libro_disponible.html'
     #esto es por si se sabe la ruta de un libro que ya no tiene stock lo redirecione
    def get(self,request,*agrs,**kwargs):
        if self.get_object().cantidad > 0:
            return render(request,self.template_name,{'object':self.get_object()})
        return redirect('libro:listado_libros_disponibles')


class RegistrarReserva(CreateView):
    model = Reserva
    success_url = reverse_lazy('libro:listado_libros_disponibles')

    def post(self,request,*args,**kwargs):
        if is_ajax(request):
            libro = Libro.objects.filter(id = request.POST.get('libro')).first() #recojemos el libro que pasamos por ajax en el template 
            usuario = user.objects.filter(id = request.POST.get('usuario')).first()
            if libro and usuario: #si existe el libro y el usuario
                if libro.cantidad > 0:
                    #hacemos un un previo para guardar en el modelo y hacer una reserva
                    nueva_reserva = self.model(  #self.model.objects.create() igugal podemos hacerlo asi y ya no ponemos el .save despues es lo mismo
                        libro = libro,
                        usuario = usuario
                    )
                    nueva_reserva.save()#guardamos el privio
                    mensaje = f'{self.model.__name__} registrada correctamente!'
                    error = 'No hay error!'
                    response = JsonResponse({'mensaje': mensaje, 'error': error,'url':self.success_url}) #colocamos url para que despues de reservar nos redireccione
                    response.status_code = 201
                    return response
        return redirect('libro:listado_libros_disponibles')

class ListadoLibrosReservados(ListView):
    model = Reserva
    template_name = 'libro/libros_reservados.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(estado = True,usuario = self.request.user)
        return queryset

class Reservas(ListView):
    model = Reserva

    def get_queryset(self):
        return self.model.objects.filter(estado = True,usuario = self.request.user)

    def get(self, request, *args, **kwargs):
        if is_ajax(request):
            return HttpResponse(serializers.serialize('json', self.get_queryset(),use_natural_foreign_keys = True), 'application/json')
        else:
            return redirect('libro:listado_libros_reservados')

class ListadoReservasVencias(TemplateView):
    template_name = 'libro/reservas_vencidas.html'

class ReservasVencidas(ListView):
    model = Reserva

    def get_queryset(self):
        return self.model.objects.filter(estado = False,usuario = self.request.user)

    def get(self, request, *args, **kwargs):
        if is_ajax(request):
            return HttpResponse(serializers.serialize('json', self.get_queryset(),use_natural_foreign_keys = True), 'application/json')
        else:
            return redirect('libro:listado_reservas_vencidas')

