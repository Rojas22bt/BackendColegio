from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Gestion,Trimestre,DetalleTrimestre
from Periodo.serializers import GestionSerializers,DetalleTrimestreSerializer

@api_view(['POST'])
def crear_gestion(request):
    anio_escolar = request.data.get("anio_escolar")

    # Verificar si ya existe una gestión con ese año
    gestion_existente = Gestion.objects.filter(anio_escolar=anio_escolar).first()
    if gestion_existente:
        return Response({"error": "Ya existe este año"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = GestionSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def obtener_gestiones(request):
    gestiones = Gestion.objects.all()
    serializer = GestionSerializers(gestiones,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

