from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Bitacora
from Usuarios.serializers import BitacoraSerializers

@api_view(['GET'])
def obtener_bitacora(request):
    bitacora = Bitacora.objects.all()
    serializer = BitacoraSerializers(bitacora,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
