from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Usuario,Profesor,Alumno
from Usuarios.serializers import UsuarioSerializer,AlumnoSerializer


@api_view(['GET'])
def obtener_alumnos(request,gestion,id_paralelo):
    alumnos = Usuario.objects.filter(
        alumno__alumnocursoparalelo__curso_paralelo_id=id_paralelo,
        alumno__alumnocursoparalelo__gestion_id=gestion
    )
    serializer = UsuarioSerializer(alumnos,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    