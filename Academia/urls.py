from django.urls import path
from .controllers.controllers_academia import (
    crear_curso,obtener_cursos,
    crear_nivel
)

urlpatterns = [
    path('crear-curso/',crear_curso),
    path('obtener-cursos/',obtener_cursos),
    
    path('crear-nivel/',crear_nivel)
]
