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
