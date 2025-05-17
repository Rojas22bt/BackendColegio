from django.urls import path
from .controllers.controller_usuario import crear_usuario 

urlpatterns = [
    path('/crearUsuario', crear_usuario.as_view(),name='crear_usuario')
]
