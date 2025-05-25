from django.urls import path
from .controllers.controllers_dimension import crear_dimension,obtener_dimensiones,actualizar_dimension,eliminar_dimension
from .controllers.controller_asistencia import crear_asistencia,actualizar_asistencia

urlpatterns = [
    path('crear-dimension/', crear_dimension),
    path('obtener-dimensiones/', obtener_dimensiones),
    path('actualizar-dimension/<int:id>/', actualizar_dimension),
    path('eliminar-dimension/<int:id>/', eliminar_dimension),
    
    path('crear-asistencia/', crear_asistencia),
    path('actualizar-asistencia/<int:id>/', actualizar_asistencia),
]