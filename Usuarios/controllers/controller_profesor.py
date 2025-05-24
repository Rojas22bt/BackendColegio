from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Usuario,Profesor,Alumno,DescripcionMateria,HorarioMateria
from Academia.serializers import DescripcionHorarioSerializer,DescripcionMateriaSerializer

@api_view(['GET'])
def obtener_materia_horario_profesor(request,id):
    try:
        descripcion_materia = DescripcionMateria.objects.get(profesor = id)
        serializer = DescripcionHorarioSerializer(descripcion_materia).data
        return Response(serializer, status=status.HTTP_200_OK)
    
    except DescripcionMateria.DoesNotExist:
        return Response({"mensaje":"Profesor no encontrado"}, status=status.HTTP_404_NOT_FOUND)
