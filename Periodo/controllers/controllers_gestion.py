from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Gestion,Trimestre,DetalleTrimestre
from Periodo.serializers import GestionSerializers,DetalleTrimestreSerializer


@api_view(['POST'])
def crear_gestion(request):
    trimestre = Trimestre.objects.all()
    serializer = GestionSerializers(data=request.data)
    
    if serializer.is_valid():
        gestion = serializer.save()  # guardamos la nueva Gestión

        for tri in trimestre:
            data = {
                "gestion": gestion.id,      # uso correcto del ID
                "trimestre": tri.id
            }
            serializer2 = DetalleTrimestreSerializer(data=data)
            if serializer2.is_valid():
                serializer2.save()
            else:
                return Response({
                    "mensaje": "Error al guardar DetalleTrimestre",
                    "errores": serializer2.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "mensaje": "Gestión y detalles creados correctamente",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response({
        "mensaje": "Error al guardar Gestión",
        "errores": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


