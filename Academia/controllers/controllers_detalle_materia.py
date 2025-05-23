from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import DescripcionMateria,Profesor,Materia,CursoParalelo,Horario,HorarioMateria
from Academia.serializers import DescripcionMateriaSerializer

@api_view(['POST'])
def crear_descripcion_materia(request):
    serializer = DescripcionMateriaSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje":"registro exitoso","data":serializer.data},status=status.HTTP_200_OK)  
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)