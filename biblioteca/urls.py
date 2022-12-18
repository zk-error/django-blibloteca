from django.conf import settings 
from django.conf.urls.static import static 
from django.contrib import admin
from django.urls import path,include
from usuario.views import Inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")), #para el registro inicio y cierre de secion de usuarios 
    path('libro/',include(('libro.urls','libro'))),
    path('',Inicio.as_view(), name = 'index'),
]+ static(
settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
) 
