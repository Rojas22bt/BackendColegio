from django.urls import path
from .controllers.controllers_dimension import crear_dimension,obtener_dimensiones,actualizar_dimension,eliminar_dimension


urlpatterns = [
    path('crear-dimension/', crear_dimension),
    path('obtener-dimensiones/', obtener_dimensiones),
    path('actualizar-dimension/<int:id>/', actualizar_dimension),
    path('eliminar-dimension/<int:id>/', eliminar_dimension),
]