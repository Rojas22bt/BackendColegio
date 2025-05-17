from django.urls import path
from .controllers.controller_usuario import crear_usuario 

urlpatterns = [
    path('crearUsuario/', crear_usuario, name='crear_usuario')  # sin as_view()
]
