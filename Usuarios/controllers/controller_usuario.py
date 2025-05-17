from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Usuario,Profesor,Alumno
from Usuarios.serializers import UsuarioSerializer

@api_view(['POST'])
def crear_usuario(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        usuario = serializer.save()
        
        rol_id =int(request.data.get('rol', 0))
        if rol_id == 1:
            Profesor.objects.create(profesor=usuario, especialidad=request.data.get('especialidad', ''))
        elif rol_id == 2:
            Alumno.objects.create(alumno=usuario, matricula=request.data.get('matricula', ''))

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)