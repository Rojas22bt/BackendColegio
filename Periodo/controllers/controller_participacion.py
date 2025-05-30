from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Participacion
from Periodo.serializers import ParticipacionSerializers

@api_view(['POST'])
def crear_participacion(request):
    serializer = ParticipacionSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje":"todo okey", "data":serializer.data},status=status.HTTP_201_CREATED)
    return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def obtener_participaciones(request,alumno,materia):
    participacion = Participacion.objects.filter(
        alumno = alumno,
        materia = materia
    )
    serializer = ParticipacionSerializers(participacion,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)