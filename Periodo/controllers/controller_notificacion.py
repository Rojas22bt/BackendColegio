from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Notificacion, Usuario
from Periodo.serializers import NotificacionSerializers
import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings

cred_path = getattr(settings, 'FIREBASE_CREDENTIALS', None)

if cred_path and not firebase_admin._apps:
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Error al inicializar Firebase: {e}")

def enviar_notificacion_firebase_por_tokens(titulo, mensaje, tokens):
    if not tokens:
        return {"enviados": 0, "mensaje": "No hay tokens para enviar"}

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=titulo,
            body=mensaje
        ),
        tokens=tokens
    )

    response = messaging.send_multicast(message)
    return {
        "enviados": response.success_count,
        "fallos": response.failure_count,
        "detalle": response.responses
    }


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
    
    


@api_view(['POST'])
def crear_notificacion_flexible(request):
    tipo = request.data.get("tipo")  # "todos" o "rol"
    id_rol = request.data.get("rol")  # Solo si tipo == "rol"
    titulo = request.data.get("titulo")
    mensaje = request.data.get("mensaje")

    if not titulo or not mensaje:
        return Response({"error": "Faltan campos 'titulo' o 'mensaje'"}, status=status.HTTP_400_BAD_REQUEST)

    errores = []
    enviados = 0
    firebase_tokens = []

    if tipo == "todos":
        usuarios = Usuario.objects.exclude(fcm_token__isnull=True)
        todos = Usuario.objects.all()

        # Guardar notificaciones para todos
        for usuario in todos:
            data = request.data.copy()
            data["usuario"] = usuario.id
            serializer = NotificacionSerializers(data=data)
            if serializer.is_valid():
                serializer.save()
                enviados += 1
            else:
                errores.append({"usuario_id": usuario.id, "error": serializer.errors})

        # Preparar tokens solo para los que tienen fcm_token
        firebase_tokens = [u.fcm_token for u in usuarios if u.fcm_token.strip() != ""]

        firebase_res = enviar_notificacion_firebase_por_tokens(titulo, mensaje, firebase_tokens)

        return Response({
            "mensaje": f"Notificación enviada a todos.",
            "notificaciones_guardadas": enviados,
            "errores_guardado": errores,
            "firebase_enviados": firebase_res["enviados"],
            "firebase_fallos": firebase_res["fallos"]
        })

    elif tipo == "rol":
        if not id_rol:
            return Response({"error": "Falta el campo 'rol'"}, status=status.HTTP_400_BAD_REQUEST)

        usuarios = Usuario.objects.filter(rol_id=id_rol)
        if not usuarios.exists():
            return Response({"mensaje": "No hay usuarios con ese rol"}, status=status.HTTP_404_NOT_FOUND)

        firebase_tokens = []
        enviar_firebase = int(id_rol) == 2  # Solo si es rol Alumno

        for usuario in usuarios:
            data = request.data.copy()
            data["usuario"] = usuario.id
            serializer = NotificacionSerializers(data=data)
            if serializer.is_valid():
                serializer.save()
                enviados += 1

                if enviar_firebase and usuario.fcm_token:
                    firebase_tokens.append(usuario.fcm_token)
            else:
                errores.append({"usuario_id": usuario.id, "error": serializer.errors})

        firebase_res = {"enviados": 0, "fallos": 0}
        if enviar_firebase:
            firebase_res = enviar_notificacion_firebase_por_tokens(titulo, mensaje, firebase_tokens)

        return Response({
            "mensaje": f"Notificación enviada a usuarios del rol {id_rol}.",
            "notificaciones_guardadas": enviados,
            "errores_guardado": errores,
            "firebase_enviados": firebase_res["enviados"],
            "firebase_fallos": firebase_res["fallos"]
        })

    else:
        return Response({"error": "El campo 'tipo' debe ser 'todos' o 'rol'"}, status=status.HTTP_400_BAD_REQUEST)

