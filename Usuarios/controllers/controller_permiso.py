from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Permiso,Privilegio,Rol
from Usuarios.serializers import RolSerializers,PrivilegioSerializers,PermisoDetalleSerializer


#------CRUD DE PRIVILEGIO----------

#CREAR NUEVO PRIVILEGIO
@api_view(['POST'])
def crear_privilegio(request):
    serializer = PrivilegioSerializers(data=request.data)
    if serializer.is_valid():
        privilegio = serializer.save()
        roles = Rol.objects.all()
        permisos_creados = []
        for rol in roles:
            permiso, creado = Permiso.objects.get_or_create(
                rol=rol,
                privilegio=privilegio,
                defaults={'estado': True}  
            )
            if creado:
                permisos_creados.append(PermisoDetalleSerializer(permiso).data)

        return Response({
            "mensaje": "Privilegio creado correctamente",
            "privilegio": PrivilegioSerializers(privilegio).data,
            "permisos_creados": permisos_creados
        }, status=status.HTTP_201_CREATED)

    return Response({
        "mensaje": "Error al crear el privilegio",
        "errores": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

#ACTUALIZER PRIVILEGIO
@api_view(['PUT'])
def actualizar_privilegio(request,id):
    try:
        privilegio = Privilegio.objects.get(id=id)
    except Privilegio.DoesNotExist:
        return Response(
            {"mensaje": "Privilegio no encontrado"},
            status=status.HTTP_404_NOT_FOUND
            )
    serializer = PrivilegioSerializers(privilegio, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "mensaje": "Privilegio actualizado correctamente",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    return Response({
        "mensaje": "Error al actualizar el Privilegio",
        "errores": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

#ELIMINAR PRIVILEGIO POR ID
@api_view(['DELETE'])
def eliminar_privilegio(request,id):
    try:
        privilegio = Privilegio.objects.get(id=id)
        privilegio.delete()
        return Response(
            {"mensaje": "Privilegio eliminado"},
            status=status.HTTP_200_OK
        )
    except Privilegio.DoesNotExist:
      return Response(
            {"mensaje": "Privilegio no encontrado"}, 
            status=status.HTTP_404_NOT_FOUND
        )
      
#OBTENER PRIVILEGIOS
@api_view(['GET'])
def obtener_privilegio(request):
    privilegios = Privilegio.objects.all()
    serializer = PrivilegioSerializers(privilegios,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#ACTUALIZER EL ESTADO DE ESE PERMISO DE CADA ROL POR PRIVILEGIO
@api_view(['PUT'])
def actualizar_estado_permiso(request):
    rol_id = request.data.get('rol')
    privilegio_id = request.data.get('privilegio')
    nuevo_estado = request.data.get('estado')

    if rol_id is None or privilegio_id is None or nuevo_estado is None:
        return Response({
            "mensaje": "Se requieren los campos 'rol', 'privilegio' y 'estado'"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        permiso = Permiso.objects.get(rol_id=rol_id, privilegio_id=privilegio_id)
    except Permiso.DoesNotExist:
        return Response({
            "mensaje": "Permiso no encontrado con ese rol y privilegio"
        }, status=status.HTTP_404_NOT_FOUND)

    permiso.estado = nuevo_estado
    permiso.save()

    return Response({
        "mensaje": "Permiso actualizado correctamente",
        "data": PermisoDetalleSerializer(permiso).data
    }, status=status.HTTP_200_OK)


#------CRUD DE ROL--------------------

#CREAR UN NUEVO ROL
@api_view(['POST']) 
def crear_rol(request):
    serializer = RolSerializers(data=request.data)
    if serializer.is_valid():
        rol = serializer.save()
        return Response({
            "mensaje": "Rol creado correctamente",
            "data": RolSerializers(rol).data
        }, status=status.HTTP_201_CREATED)

    return Response({
            "mensaje": "Error al crear el rol",
            "errores": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
#ACTUALIZAR ROL CON EL METODO PUT
@api_view(['PUT'])
def actualizar_rol(request,id):
    try:
        rol = Rol.objects.get(id=id)
    except Rol.DoesNotExist:
        return Response(
            {"mensaje": "Rol no encontrado"},
            status=status.HTTP_404_NOT_FOUND
            )
    serializer = RolSerializers(rol, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "mensaje": "Rol actualizado correctamente",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    return Response({
        "mensaje": "Error al actualizar el rol",
        "errores": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

#ELIMINAR ROL POR ID    
@api_view(['DELETE'])
def eliminar_rol(request,id):
    try:
        rol = Rol.objects.get(id=id)
        rol.delete()
        return Response(
            {"mensaje": "Rol eliminado"},
            status=status.HTTP_200_OK
        )
    except Rol.DoesNotExist:
      return Response({"mensaje": "Rol no encontrado"}, status=status.HTTP_404_NOT_FOUND)   

#OBTENER TODOS LOS ROLES DE LA TABLA
@api_view(['GET'])
def obtener_roles(request):
    roles = Rol.objects.all()
    serializers = RolSerializers(roles, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

#OBTENER TODOS LOS ROLES ACTIVOS DE LA TABLA (NO FUNCIONA PORQUE NO EXISTE ESTADO EN LA TABLA)
@api_view(['GET'])
def obtener_roles_activos(request):
    roles = Rol.objects.filter(estado=True)
    serializer = RolSerializers(roles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)