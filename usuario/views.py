
from django.views.generic import CreateView, ListView, UpdateView, DeleteView,TemplateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from libro.models import Libro,Reserva
# from .forms import CustomUserCreationForm

class Inicio(TemplateView):
  template_name = 'index.html'

  def get(self,request,*args, **kwargs):
    # #query es para ver comos se ve el codigo sql
    # print(Reserva.objects.select_related('libro').all().query)
    # reservas = Reserva.objects.all()
    # for reserva in reservas:
    #   print(reserva.usuario.username)
    #   print(reserva.libro.titulo)
    #   print(reserva.libro.fecha_publicacion)
    return render(request,self.template_name)



