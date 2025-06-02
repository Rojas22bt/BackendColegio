from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Notificacion, Usuario
from Periodo.serializers import NotificacionSerializers
import firebase_admin
from firebase_admin import credentials, messaging
import os
import json
import tempfile

if not firebase_admin._apps:
    try:
        firebase_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
        if firebase_json:
            # ✅ Guardamos el contenido JSON temporalmente en un archivo
            with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as temp_json:
                temp_json.write(firebase_json)
                temp_json.flush()
                cred = credentials.Certificate(temp_json.name)
                firebase_admin.initialize_app(cred)
        else:
            print("⚠️ No se encontró la variable FIREBASE_CREDENTIALS_JSON")
    except Exception as e:
        print(f"🔥 Error al inicializar Firebase: {e}")

def enviar_notificacion_firebase(titulo, mensaje, token):
    if not token or not isinstance(token, str):
        return {"enviado": False, "motivo": "Token inválido o vacío"}

    message = messaging.Message(
        notification=messaging.Notification(
            title=titulo,
            body=mensaje
        ),
        token=token
    )

    try:
        response = messaging.send(message)
        return {
            "enviado": True,
            "firebase_response": response
        }
    except Exception as e:
        return {"enviado": False, "motivo": f"Error al enviar: {e}"}


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def crear_notificacion_uni(request, id):
    try:
        usuario = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        return Response({"mensaje": "Usuario no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data.copy()
    data["usuario"] = usuario.id

    serializer = NotificacionSerializers(data=data)
    if serializer.is_valid():
        serializer.save()

        titulo = data.get("titulo", "Notificación")
        mensaje = data.get("mensaje", "")
        firebase_resultado = {"enviado": False, "motivo": ""}

        if usuario.fcm_token and usuario.fcm_token.strip():
            try:
                res = enviar_notificacion_firebase(titulo, mensaje, usuario.fcm_token)
                firebase_resultado = {
                    "enviado": res.get("enviado", False),
                    "motivo": res.get("motivo", "OK" if res.get("enviado") else "Sin motivo")
                }
            except Exception as e:
                firebase_resultado = {
                    "enviado": False,
                    "motivo": f"Error al enviar: {str(e)}"
                }
        else:
            firebase_resultado["motivo"] = "Usuario sin token FCM"


        return Response({
            "mensaje": "Notificación creada",
            "firebase": firebase_resultado
        }, status=status.HTTP_201_CREATED)

    return Response({
        "error": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


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

        firebase_res = enviar_notificacion_firebase(titulo, mensaje, firebase_tokens)

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
            firebase_res = enviar_notificacion_firebase(titulo, mensaje, firebase_tokens)

        return Response({
            "mensaje": f"Notificación enviada a usuarios del rol {id_rol}.",
            "notificaciones_guardadas": enviados,
            "errores_guardado": errores,
            "firebase_enviados": firebase_res["enviados"],
            "firebase_fallos": firebase_res["fallos"]
        })

    else:
        return Response({"error": "El campo 'tipo' debe ser 'todos' o 'rol'"}, status=status.HTTP_400_BAD_REQUEST)

