from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Curso,Nivel,Paralelo
from Academia.serializers import CursoSerializer,NivelSerializer,ParaleloSerializer

#CRUD DE NIVEL

@api_view(['POST'])
def crear_nivel(request):
    serializer= NivelSerializer(data=request.data)
    if serializer.is_valid():
        nivel = serializer.save()
        return Response({
            "mensaje": "Nivel creado correctamente",
            "data": NivelSerializer(nivel).data
        }, status=status.HTTP_201_CREATED)

    return Response({
            "mensaje": "Error al crear el nivel",
            "errores": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def obtener_niveles(request):
    nivel = Nivel.objects.all()
    serializer = NivelSerializer(nivel,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['PUT'])
def actualizar_nivel(request,id):
    try:
        nivel = Nivel.objects.get(id=id)
    except Nivel.DoesNotExist:
        return Response(
            {"mensaje": "Nivel no encontrado"},
            status=status.HTTP_404_NOT_FOUND
            )
    serializer = NivelSerializer(nivel, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "mensaje": "Nivel actualizado correctamente",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    return Response({
        "mensaje": "Error al actualizar el nivel",
        "errores": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
    
  
@api_view(['DELETE'])
def eliminar_nivel(request,id):
    try:
        nivel = Nivel.objects.get(id=id)
        nivel.delete()
        return Response(
            {"mensaje": "Nivel eliminado"},
            status=status.HTTP_200_OK
        )
    except Nivel.DoesNotExist:
      return Response({"mensaje": "Nivel no encontrado"}, status=status.HTTP_404_NOT_FOUND)   

@api_view(['POST'])


#CRUD DE CURSO
def crear_curso(request):
    serializer = CursoSerializer(data=request.data)
    if serializer.is_valid():
        curso = serializer.save()
        return Response({
            "mensaje": "Curso creado correctamente",
            "data": CursoSerializer(curso).data
        }, status=status.HTTP_201_CREATED)

    return Response({
            "mensaje": "Error al crear el curso",
            "errores": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def actualizar_curso(request,id):
    try:
        curso = Curso.objects.get(id=id)
    except Curso.DoesNotExist:
        return Response(
            {"mensaje": "Curso no encontrado"},
            status=status.HTTP_404_NOT_FOUND
            )
    serializer = CursoSerializer(curso, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "mensaje": "Curso actualizado correctamente",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    return Response({
        "mensaje": "Error al actualizar el curso",
        "errores": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_curso(request,id):
    try:
        curso = Curso.objects.get(id=id)
        curso.delete()
        return Response(
            {"mensaje": "Curso eliminado"},
            status=status.HTTP_200_OK
        )
    except Curso.DoesNotExist:
      return Response({"mensaje": "Curso no encontrado"}, status=status.HTTP_404_NOT_FOUND)   

@api_view(['GET'])
def obtener_cursos(request):
    curso = Curso.objects.all()
    serializer = CursoSerializer(curso, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#CRUD PARALELO
@api_view(['POST'])
def crear_paralelo(request):
    serializer = ParaleloSerializer(data=request.data)
    if serializer.is_valid():
        paralelo = serializer.save()
        return Response({
            "mensaje": "Paralelo creado correctamente",
            "data": ParaleloSerializer(paralelo).data
        }, status=status.HTTP_201_CREATED)

    return Response({
            "mensaje": "Error al crear el paralelo",
            "errores": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
def actualizar_paralelo(request,id):
    try:
        paralelo = Paralelo.objects.get(id=id)
    except Paralelo.DoesNotExist:
        return Response(
            {"mensaje": "Paralelo no encontrado"},
            status=status.HTTP_404_NOT_FOUND
            )
    serializer = ParaleloSerializer(paralelo, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "mensaje": "Paralelo actualizado correctamente",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    return Response({
        "mensaje": "Error al actualizar el paralelo",
        "errores": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
def eliminar_paralelo(request,id):
    try:
        paralelo = Paralelo.objects.get(id=id)
        paralelo.delete()
        return Response(
            {"mensaje": "Paralelo eliminado"},
            status=status.HTTP_200_OK
        )
    except Paralelo.DoesNotExist:
      return Response({"mensaje": "Paralelo no encontrado"}, status=status.HTTP_404_NOT_FOUND)   
@api_view(['GET'])
def obtener_paralelos(request):
    paralelo = Paralelo.objects.all()
    serializer = ParaleloSerializer(paralelo, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
