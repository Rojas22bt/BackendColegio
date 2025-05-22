from django.urls import path
from .controllers.controllers_academia import (
    crear_curso,obtener_cursos,
    crear_nivel,obtener_niveles,actualizar_nivel,eliminar_nivel
)

urlpatterns = [
    path('crear-curso/',crear_curso),
    path('obtener-cursos/',obtener_cursos),
    
    path('crear-nivel/',crear_nivel),
    path('obtener-niveles/',obtener_niveles),
    path('actualizar-nivel/<int:id>/',actualizar_nivel),
    path('eliminar-nivel/<int:id>/',eliminar_nivel)
]
