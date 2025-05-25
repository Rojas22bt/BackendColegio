from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Notificacion, Usuario
from Periodo.serializers import NotificacionSerializers

@api_view(['POST'])
def crear_notificacion_uni(request,id):
    try:
        usuario = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        return Response({"mensaje":"usuario no encontrado"}, status=status.HTTP_400_BAD_REQUEST)
    data = request.data.copy()
    data["usuario"] = usuario.id
    serializer = NotificacionSerializers(data=data,many=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje":"notificacion creado"}, status=status.HTTP_201_CREATED)
    return Response({"error":serializer.errors},status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def obtener_notificacion_uni(request,id):
    try:
        usuario = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        return Response({"mensaje":"usuario no encontrado"}, status=status.HTTP_400_BAD_REQUEST)
    notificaciones = Notificacion.objects.filter(usuario=id)
    resultado= []
    for noti in notificaciones:
        serializer = NotificacionSerializers(noti).data
        resultado.append({
            "notificaciones":serializer
        }
        )
    return Response(resultado, status=status.HTTP_200_OK)
