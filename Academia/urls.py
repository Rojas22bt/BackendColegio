from django.urls import path
from .controllers.controllers_academia import (
    crear_curso,obtener_cursos,actualizar_curso,eliminar_curso,
    crear_nivel,obtener_niveles,actualizar_nivel,eliminar_nivel,
    crear_paralelo,obtener_paralelos,actualizar_paralelo,eliminar_paralelo,
    crear_materia,obtener_materias,actualizar_materia,eliminar_materia,
    crear_horario,obtener_horarios,actualizar_horario,eliminar_horario
)

from .controllers.controllers_detalle_curso import (
    crear_detalle_curso_materia,obtener_detalle_curso_materia,
    actualizar_detalle_curso_materia,eliminar_detalle_curso_materia,
    crear_detalle_curso_paralelo,obtener_detalle_curso_paralelo,
    actualizar_detalle_curso_paralelo,eliminar_detalle_curso_paralelo,
    obtener_cursos_con_paralelos_y_materias
)

from .controllers.controllers_detalle_materia import ( crear_descripcion_completa )

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
    path('eliminar-horario/<int:id>/',eliminar_horario),
    
    path('crear-detalle-curso-materia/',crear_detalle_curso_materia),
    path('obtener-detalle-curso-materia/',obtener_detalle_curso_materia),
    path('actualizar-detalle-curso-materia/',actualizar_detalle_curso_materia),
    path('eliminar-detalle-curso-materia/',eliminar_detalle_curso_materia),
    
    path('crear-detalle-curso-paralelo/',crear_detalle_curso_paralelo),
    path('obtener-detalle-curso-paralelo/',obtener_detalle_curso_paralelo),
    path('actualizar-detalle-curso-paralelo/<int:id>/',actualizar_detalle_curso_paralelo),
    path('eliminar-paralelo/',eliminar_detalle_curso_paralelo),
    path('obtener/',obtener_cursos_con_paralelos_y_materias),
    
    path('crear-detalle-materia/',crear_descripcion_completa),
    
]
