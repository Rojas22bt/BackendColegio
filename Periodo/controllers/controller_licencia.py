from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Licencia
from Periodo.serializers import LicenciaSerializers

@api_view(['POST'])
def crear_licencia(request):
    serializer = LicenciaSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje":"Licencia Enviada"},status=status.HTTP_200_OK)
    return Response({"mensaje":"ocurrio algun error", "error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

api_view(['POST'])
def obtner_licencias(requets):
    fecha = requets.data.get("fecha")
    licencias = Licencia.objects.filter(fecha=fecha)
    seriaizer = LicenciaSerializers(licencias,many=True)
    return Response(seriaizer.data,status=status.HTTP_200_OK)
    
