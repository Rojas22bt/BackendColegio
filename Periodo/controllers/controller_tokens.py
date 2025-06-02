from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Usuario

@api_view(['POST'])
def guardar_token(request):
    ci = request.data.get("ci")
    token = request.data.get("fcm_token")

    try:
        usuario = Usuario.objects.get(ci=ci)
        usuario.fcm_token = token
        usuario.save()
        return Response({"mensaje": "Token guardado correctamente."}, status=status.HTTP_200_OK)
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
