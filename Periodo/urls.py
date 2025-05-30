from django.urls import path
from Periodo.controllers.controller_trimestre import crear_trimestre,obtener_trimestres,actualizar_trimestre,eliminar_trimestre
from Periodo.controllers.controllers_gestion import crear_gestion,obtener_gestiones_completas
from Periodo.controllers.controller_notificacion import crear_notificacion_uni,obtener_notificacion_uni,actualizar_notificacion_uni,crear_notificacion_rol
from Periodo.controllers.controller_participacion import crear_participacion,obtener_participaciones
urlpatterns = [
    path('crear-trimestre/',crear_trimestre),
    path('obtener-trimestres/',obtener_trimestres),
    path('actualizar-trimestre/<int:id>/',actualizar_trimestre),
    path('eliminar-trimestre/<int:id>/',eliminar_trimestre),
    path('crear-gestion/',crear_gestion),
    path('obtener-gestiones/',obtener_gestiones_completas),
    path('crear-notificacion-uni/<int:id>/',crear_notificacion_uni),
    path('obtener-notificacion-uni/<int:id>/',obtener_notificacion_uni),
    path('actualizar-notificacion-uni/<int:id_notificacion>/',actualizar_notificacion_uni),
    path('crear-notificacion-rol/',crear_notificacion_rol),
    path('crear-participacion/',crear_participacion),
    path('obtener-participacion/<int:alumno>/<int:materia>/',obtener_participaciones),
]
