from django.urls import path
from .controllers.controller_usuario import crear_usuario 

from .controllers.controller_permiso import (
    crear_rol,actualizar_rol,eliminar_rol,obtener_roles,obtener_roles_activos,
    crear_privilegio,actualizar_privilegio,obtener_privilegio,eliminar_privilegio,
    actualizar_estado_permiso
)

urlpatterns = [
    path('crearUsuario/', crear_usuario, name='crear_usuario'),
    
    #------URL PARA ROL-----
    path('crearRol/', crear_rol, name='crear_rol'),
    path('obtenerRoles/', obtener_roles),
    path('obtenerRolesActivos/', obtener_roles_activos),
    path('actualizarRol/<int:id>/', actualizar_rol),
    path('eliminarRol/<int:id>/', eliminar_rol),
    
    #-----URL PARA PRIVILEGIO-----
    path('crearPrivilegio/', crear_privilegio),
    path('obtenerPrivilegio/', obtener_privilegio),
    path('actualizarPrivilegio/<int:id>/', actualizar_privilegio),
    path('eliminarPrivilegio/<int:id>/', eliminar_privilegio),
    
    #----URL PARA ACTUALIZAR PERMISOS POR ROL----
    path('actualizarEstadoPermiso/',actualizar_estado_permiso)
]
