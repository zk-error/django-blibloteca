import json

from time import time
from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View,TemplateView,ListView,UpdateView,CreateView,DeleteView,DetailView
from django.urls import reverse_lazy
# from apps.usuario.mixins import LoginYSuperStaffMixin, ValidarPermisosMixin,LoginMixin
# from apps.usuario.models import Usuario
from .models import Autor ,Libro#Reserva
from .forms import AutorForm,LibroForm


class ListadoAutor(ListView):
    model = Autor
    template_name = 'libro/autor/listar_autor.html'
    context_object_name = 'autores'
    queryset = Autor.objects.filter(estado = True)

class ActualizarAutor(UpdateView):
    model = Autor
    template_name = 'libro/autor/crear_autor.html'
    form_class = AutorForm
    success_url = reverse_lazy('libro:listar_autor')


class CrearAutor(CreateView):
    model = Autor
    template_name = 'libro/autor/crear_autor.html'
    form_class = AutorForm
    success_url = reverse_lazy('libro:listar_autor')

class EliminarAutor(DeleteView):
    model = Autor
    # success_url = reverse_lazy('libro:listar_autor')
    def post(self,request,pk,*args, **kwargs):
        object = Autor.objects.get(id=pk)
        object.estado = False
        object.save()
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
