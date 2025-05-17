from django.urls import path
from .controllers.controller_usuario import crear_usuario 
from .controllers.controller_permiso import crear_rol

urlpatterns = [
    path('crearUsuario/', crear_usuario, name='crear_usuario'),
    path('crearRol/', crear_rol, name='crear_rol')
]
