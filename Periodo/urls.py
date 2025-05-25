from django.urls import path
from Periodo.controllers.controller_trimestre import crear_trimestre,obtener_trimestres,actualizar_trimestre,eliminar_trimestre
from Periodo.controllers.controllers_gestion import crear_gestion
from Periodo.controllers.controller_notificacion import crear_notificacion_uni,obtener_notificacion_uni
urlpatterns = [
    path('crear-trimestre/',crear_trimestre),
    path('obtener-trimestres/',obtener_trimestres),
    path('actualizar-trimestre/<int:id>/',actualizar_trimestre),
    path('eliminar-trimestre/<int:id>/',eliminar_trimestre),
    path('crear-gestion/',crear_gestion),
    path('crear-notificacion-uni/<int:id>/',crear_notificacion_uni),
    path('obtener-notificacion-uni/<int:id>/',obtener_notificacion_uni),
]
