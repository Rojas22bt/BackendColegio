from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Usuario,Rol,Permiso
from Usuarios.serializers import UsuarioSerializer,PermisoDetalleSerializer
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def login_usuario(request):
    ci = request.data.get('ci')
    password = request.data.get('password')

    try:
        usuario = Usuario.objects.get(ci=ci)
        
        if not usuario.estado:
            return Response({'mensaje': 'Usuario no está activado'}, status=status.HTTP_403_FORBIDDEN)
        
        if not usuario.check_password(password):
            return Response({'mensaje': 'Contraseña incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(usuario)
        serializer = UsuarioSerializer(usuario)

        rol = usuario.rol
        permisos = Permiso.objects.filter(rol=rol)
        serializer2 = PermisoDetalleSerializer(permisos, many=True)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'usuario': serializer.data,
            'permisos': serializer2.data
        }, status=status.HTTP_200_OK)

    except Usuario.DoesNotExist:
        return Response({'mensaje': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

