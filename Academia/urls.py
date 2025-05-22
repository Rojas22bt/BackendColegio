from django.urls import path
from .controllers.controllers_academia import (
    crear_curso,obtener_cursos,actualizar_curso,eliminar_curso,
    crear_nivel,obtener_niveles,actualizar_nivel,eliminar_nivel,
    crear_paralelo,obtener_paralelos,actualizar_paralelo,eliminar_paralelo,
    crear_materia,obtener_materias,actualizar_materia,eliminar_materia,
    crear_horario,obtener_horarios,actualizar_horario,eliminar_horario
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
    path('eliminar-nivel/<int:id>/',eliminar_nivel),
    
    path('crear-materia/',crear_materia),
    path('obtener-materias/',obtener_materias),
    path('actualizar-materia/<int:id>/',actualizar_materia),
    path('eliminar-materia/<int:id>/',eliminar_materia),
    
    path('crear-horario/',crear_horario),
    path('obtener-horarios/',obtener_horarios),
    path('actualizar-horario/<int:id>/',actualizar_horario),
    path('eliminar-horario/<int:id>/',eliminar_horario)
]
