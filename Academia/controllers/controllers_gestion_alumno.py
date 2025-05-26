from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Libreta , DetalleTrimestre, Alumno
from Academia.serializers import LibretaSerializers


@api_view(['POST'])
def crear_libreta(request):
    gestion = request.data.get("gestion")

    detalle_trimestres = DetalleTrimestre.objects.filter(gestion=gestion)
    if not detalle_trimestres.exists():
        return Response({"mensaje": "No se encontraron trimestres para la gestión."},
                        status=status.HTTP_404_NOT_FOUND)

    respuestas = []
    errores = []

    for detalle in detalle_trimestres:
        data = request.data.copy()
        data["detalle_trimestre"] = detalle.id
        data["aprobado"] = True

        serializer = LibretaSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            respuestas.append({
                    "datos":serializer.data,
                    "id_detalle_trimestre": detalle.id,
                    "trimestre_id": detalle.trimestre,
                    "id_gestion": detalle.gestion
                })
        else:
            errores.append({"detalle_id": detalle.id, "errors": serializer.errors})

    if respuestas:
        return Response({
            "mensaje": "Se registraron algunas libretas.",
            "registradas": respuestas,
            "errores": errores
        }, status=status.HTTP_207_MULTI_STATUS if errores else status.HTTP_201_CREATED)
    else:
        return Response({
            "mensaje": "Ninguna libreta fue registrada.",
            "errores": errores
        }, status=status.HTTP_400_BAD_REQUEST)