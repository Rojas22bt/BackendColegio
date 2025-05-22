from django.urls import path
from .controllers.controllers_academia import (
    crear_curso,obtener_cursos,actualizar_curso,eliminar_curso,
    crear_nivel,obtener_niveles,actualizar_nivel,eliminar_nivel,
    crear_paralelo,obtener_paralelos,actualizar_paralelo,eliminar_paralelo
)

urlpatterns = [
    path('crear-curso/',crear_curso),
    path('obtener-cursos/',obtener_cursos),
    path('actualizar-curso/<int:id>/',actualizar_curso),
    path('eliminar-curso/<int:id>/',eliminar_curso),
    
    path('crear-paralelo/',crear_paralelo),
    path('obtener-paralelos/',obtener_paralelos),
    path('actualizar-paralelo/<int:id>/',actualizar_paralelo),
    path('eliminar-paralelo/<int:id>/',eliminar_paralelo),
    
    path('crear-nivel/',crear_nivel),
    path('obtener-niveles/',obtener_niveles),
    path('actualizar-nivel/<int:id>/',actualizar_nivel),
    path('eliminar-nivel/<int:id>/',eliminar_nivel)
]
