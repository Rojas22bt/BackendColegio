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
    serializer = NotificacionSerializers(data=data)
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


@api_view(['PUT'])
def actualizar_notificacion_uni(request,id_notificacion):
    try:
        notificacion = Notificacion.objects.get(id=id_notificacion)
    except Notificacion.DoesNotExist:
        return Response({"mensaje": "Notificación no encontrada para este usuario"}, status=status.HTTP_404_NOT_FOUND)

    serializer = NotificacionSerializers(notificacion, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje": "Notificación actualizada correctamente", "data": serializer.data}, status=status.HTTP_200_OK)

    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def crear_notificacion_rol(request):
    id_rol = request.data.get("rol")
    if not id_rol:
        return Response({"error": "Falta el campo 'rol'"}, status=status.HTTP_400_BAD_REQUEST)

    usuarios = Usuario.objects.filter(rol=id_rol)
    if not usuarios.exists():
        return Response({"mensaje": "No hay usuarios con ese rol"}, status=status.HTTP_404_NOT_FOUND)

    errores = []
    exitosos = 0

    for usuario in usuarios:
        data = request.data.copy()
        data["usuario"] = usuario.id
        serializer = NotificacionSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            exitosos += 1
        else:
            errores.append({
                "usuario_id": usuario.id,
                "error": serializer.errors
            })

    return Response({
        "mensaje": f"Notificaciones enviadas a {exitosos} usuarios.",
        "fallos": errores
    }, status=status.HTTP_207_MULTI_STATUS if errores else status.HTTP_200_OK)
