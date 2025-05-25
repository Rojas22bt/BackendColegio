from django.urls import path
from Periodo.controllers.controller_trimestre import crear_trimestre,obtener_trimestres,actualizar_trimestre,eliminar_trimestre

urlpatterns = [
    path('crear-trimestre/',crear_trimestre),
    path('obtener-trimestres/',obtener_trimestres),
    path('actualizar-trimestre/<int:id>/',actualizar_trimestre),
    path('eliminar-trimestre/<int:id>/',eliminar_trimestre),
]
