from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Gestion,Trimestre,DetalleTrimestre
from Periodo.serializers import GestionSerializers,DetalleTrimestreSerializer


@api_view(['POST'])
def crear_gestion(request):
    serializer = GestionSerializers(data=request.data)
    if serializer.is_valid():
        serializer.saver()
        return Response({"data":serializer.data},status=status.HTTP_200_OK)
    return Response({"erros":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


