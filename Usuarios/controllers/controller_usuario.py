from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Usuario,Profesor,Alumno
from Usuarios.serializers import UsuarioSerializer

@api_view(['POST'])
def crear_usuario(request):
    data = request.data.copy()  # Copia modificable del request

    password = data.get('password')
    rol_id = int(data.get('rol', 0))

    # Solo si no se proporciona contraseña
    if not password:
        if rol_id == 2:  # Profesor
            data['password'] = data.get('ci', '')
        elif rol_id == 5:  # Alumno
            data['password'] = data.get('matricula', '')

    serializer = UsuarioSerializer(data=data)
    if serializer.is_valid():
        usuario = serializer.save()

        if rol_id == 2:
            Profesor.objects.create(profesor=usuario, especialidad=data.get('especialidad', ''))
        elif rol_id == 5:
            Alumno.objects.create(alumno=usuario, matricula=data.get('matricula', ''))

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def obtener_usuarios(request):
    usuarios = Usuario.objects.all()
    serializer = UsuarioSerializer(usuarios,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def actualizar_usuario(request, id):
    try:
        usuario = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        return Response({"mensaje": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UsuarioSerializer(usuario, data=request.data)
    if serializer.is_valid():
        usuario_actualizado = serializer.save()

        rol_id = int(request.data.get('rol', 0))
        if rol_id == 5:
            alumno, _ = Alumno.objects.get_or_create(alumno=usuario_actualizado)
            alumno.matricula = request.data.get('matricula', alumno.matricula)
            alumno.save()
        elif rol_id == 2:
            profesor, _ = Profesor.objects.get_or_create(profesor=usuario_actualizado)
            profesor.especialidad = request.data.get('especialidad', profesor.especialidad)
            profesor.save()

        return Response({
            "mensaje": "Usuario actualizado correctamente",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    return Response({
        "mensaje": "Error al actualizar el usuario",
        "errores": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def eliminar_usuario(request, id):
    try:
        usuario = Usuario.objects.get(id=id)
        usuario.delete()
        return Response({"mensaje": "Usuario eliminado correctamente"}, status=status.HTTP_200_OK)
    except Usuario.DoesNotExist:
        return Response({"mensaje": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

# CREAR POR CANTIDAD SOLO PARA INGRESAR DATOS
@api_view(['POST'])
def bulk_create_usuarios(request):
    usuarios = request.data.get('usuarios', [])
    resultados = []
    errores = []

    for i, user_data in enumerate(usuarios):
        data = user_data.copy()

        rol_id = int(data.get('rol', 0))
        password = data.get('password')

        # Si no hay password, usar la CI o matrícula según el rol
        if not password:
            if rol_id == 2:
                data['password'] = data.get('ci', '')
            elif rol_id == 5:
                data['password'] = data.get('matricula', '')

        serializer = UsuarioSerializer(data=data)
        if serializer.is_valid():
            usuario = serializer.save()
            if rol_id == 2:
                Profesor.objects.create(profesor=usuario, especialidad=data.get('especialidad', ''))
            elif rol_id == 5:
                Alumno.objects.create(alumno=usuario, matricula=data.get('matricula', ''))
            resultados.append(serializer.data)
        else:
            errores.append({'index': i, 'errors': serializer.errors})

    if errores:
        return Response({'creados': resultados, 'errores': errores}, status=status.HTTP_207_MULTI_STATUS)

    return Response({'creados': resultados}, status=status.HTTP_201_CREATED)

