from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Curso
from Academia.serializers import CursoSerializer,NivelSerializer


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
    

@api_view(['POST'])
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
    
    

@api_view(['GET'])
def obtener_cursos(request):
    curso = Curso.objects.all()
    serializer = CursoSerializer(curso, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
