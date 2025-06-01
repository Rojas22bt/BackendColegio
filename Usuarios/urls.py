from django.urls import path
from .controllers.controller_usuario import crear_usuario,obtener_usuarios,actualizar_usuario,bulk_create_usuarios

from .controllers.controller_permiso import (
    crear_rol,actualizar_rol,eliminar_rol,obtener_roles,obtener_roles_activos,
    crear_privilegio,actualizar_privilegio,obtener_privilegio,eliminar_privilegio,
    actualizar_estado_permiso,obtener_permiso_agrupados_por_rol
)

from .controllers.controller_auth import login_usuario

from .controllers.controller_profesor import obtener_materia_horario_profesor

from .controllers.controllers_alumno import obtener_alumnos

urlpatterns = [
    
    #-----URL LOGIN-----
    path('login/', login_usuario),
    
    
    #------URL PARA USUARIO--------
    path('crearUsuario/', crear_usuario, name='crear_usuario'),
    path('obtenerUsuario/',obtener_usuarios),
    path('actualizarUsuario/<int:id>/',actualizar_usuario),
    
    #-----CREAR USUARIO POR CANTIDAD-----
    path('crear-cantidad-usuario/', bulk_create_usuarios),
    
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
    path('actualizarEstadoPermiso/',actualizar_estado_permiso),
    path('obtenerRolesAgrupados/',obtener_permiso_agrupados_por_rol),
    path('obtenerMateriaProfesor/',obtener_materia_horario_profesor),
    
    path('obtener-alumnos/<int:gestion>/<int:id_paralelo>/',obtener_alumnos),
]
