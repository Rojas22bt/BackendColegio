from django.urls import path
from .controllers.controller_usuario import crear_usuario 
from .controllers.controller_permiso import crear_rol,actualizar_rol,eliminar_rol,obtener_roles,obtener_roles_activos

urlpatterns = [
    path('crearUsuario/', crear_usuario, name='crear_usuario'),
    
    #------URL PARA ROL-----
    path('crearRol/', crear_rol, name='crear_rol'),
    path('obtenerRoles/', obtener_roles),
    path('obtenerRolesActivos/', obtener_roles_activos),
    path('actualizarRol/<int:id>/', actualizar_rol),
    path('eliminarRol/<int:id>/', eliminar_rol),
]
