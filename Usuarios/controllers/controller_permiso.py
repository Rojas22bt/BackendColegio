from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Permiso,Privilegio,Rol
from Usuarios.serializers import RolSerializers

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
    
@api_view(['DELETE'])
def eliminar_rol(request,id):
    try:
        rol = Rol.objects.get(id=id)
        rol.delete()
        return Response(
            {"mensaje": "Rol elimina"},
            status=status.HTTP_200_OK
        )
    except Rol.DoesNotExist:
      return Response({"mensaje": "Rol no encontrado"}, status=status.HTTP_404_NOT_FOUND)   

@api_view(['GET'])
def obtener_roles(request):
    roles = Rol.objects.all()
    serializers = RolSerializers(roles, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def obtener_roles_activos(request):
    roles = Rol.objects.filter(estado=True)
    serializer = RolSerializers(roles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)