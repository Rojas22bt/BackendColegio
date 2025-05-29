from django.urls import path
from .controllers.controllers_dimension import crear_dimension,obtener_dimensiones,actualizar_dimension,eliminar_dimension
from .controllers.controller_asistencia import crear_asistencia,actualizar_asistencia
from .controllers.controllers_actividades import (
    crear_actividad,
    obtener_tareas,
    crear_tareas,
    obtener_actividades,
    obtener_tareas_asignadas,
    obtener_dimensiones_actividades_tareas,
    actualizar_tareas,

    ) 
from .controllers.controllers_calificaciones import obtener_notas_del_alumno
urlpatterns = [
    path('crear-dimension/', crear_dimension),
    path('obtener-dimensiones/', obtener_dimensiones),
    path('actualizar-dimension/<int:id>/', actualizar_dimension),
    path('eliminar-dimension/<int:id>/', eliminar_dimension),
    
    path('crear-asistencia/', crear_asistencia),
    path('actualizar-asistencia/<int:id>/', actualizar_asistencia),
    
    path('crear-nueva-actividad/', crear_actividad),
    path('crear-nueva-tarea/', crear_tareas),
    path('obtener-tarea/', obtener_tareas),
    path('obtener-actividades/', obtener_actividades),
    path('obtener-actividades-curso/', obtener_tareas_asignadas),
    path('obtener-actividades-curso2/', obtener_dimensiones_actividades_tareas),
    path('actualizar-tareas/', actualizar_tareas),
    
    path('obtener-notas/<int:id>/<int:gestion>/', obtener_notas_del_alumno),
       
]