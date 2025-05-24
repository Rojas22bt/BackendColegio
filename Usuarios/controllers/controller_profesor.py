from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Usuario,Profesor,Alumno,DescripcionMateria,HorarioMateria
from Academia.serializers import DescripcionHorarioSerializer,DescripcionMateriaSerializer

@api_view(['GET'])
def obtener_materia_horario_profesor(request, id):
    descripcion_materias = DescripcionMateria.objects.filter(profesor=id)
    resultado = []
    for detalle in descripcion_materias:
        horarios = HorarioMateria.objects.get(descripcion_materia=detalle)
        serializer = DescripcionHorarioSerializer(horarios).data
        serializer2 = DescripcionMateriaSerializer(detalle).data
        resultado.append({
            "descripcion":serializer2,
            "horarios":serializer
        })

    return Response(resultado, status=status.HTTP_200_OK)