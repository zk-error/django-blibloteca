from django.shortcuts import render

from django.views.generic import CreateView, ListView, UpdateView, DeleteView,TemplateView

class Inicio(TemplateView):
  template_name = 'index.html'


