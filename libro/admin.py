from django.contrib import admin
from .models import Autor,Libro,Reserva
from .forms import ReservaForm

class ReservaAdmin(admin.ModelAdmin):
    form = ReservaForm
    list_display = ('libro','usuario','fecha_creacion','fecha_vencimiento','estado')

admin.site.register(Autor)
admin.site.register(Libro)
admin.site.register(Reserva,ReservaAdmin)