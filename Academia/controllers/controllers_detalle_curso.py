from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import CursoParalelo,MateriaAsignada
from Academia.serializers import MateriaAsignadaSerializer,CursoParaleloSerializer

#CRUD DE DETALLE CURSO MATERIA
@api_view(['POST'])
def crear_detalle_curso_materia(request):
    serializer = MateriaAsignadaSerializer(data=request.data)
    if serializer.is_valid():
        detalle_curso = serializer.save()
        return Response({
            "mensaje": "Detalle curso creado correctamente",
            "data": MateriaAsignadaSerializer(detalle_curso).data
        }, status=status.HTTP_201_CREATED)
    return Response({
            "mensaje": "Error al crear el detalle curso",
            "errores": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def obtener_detalle_curso_materia(request):
    detalle_curso = MateriaAsignada.objects.all()
    serializer = MateriaAsignadaSerializer(detalle_curso, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def actualizar_detalle_curso_materia(request,id):
    try:
        detalle_curso = MateriaAsignada.objects.get(id=id)
    except MateriaAsignada.DoesNotExist:
        return Response(
            {"mensaje": "Detalle curso no encontrado"},
            status=status.HTTP_404_NOT_FOUND
            )
    serializer = MateriaAsignadaSerializer(detalle_curso, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "mensaje": "Detalle curso actualizado correctamente",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    return Response({
        "mensaje": "Error al actualizar el detalle curso",
        "errores": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_detalle_curso_materia(request,id):
    try:
        detalle_curso = MateriaAsignada.objects.get(id=id)
        detalle_curso.delete()
        return Response(
            {"mensaje": "Detalle curso eliminado"},
            status=status.HTTP_200_OK
        )
    except MateriaAsignada.DoesNotExist:
      return Response({"mensaje": "Detalle curso no encontrado"}, status=status.HTTP_404_NOT_FOUND)   

#CRUD DE DETALLE CURSO PARALELO
@api_view(['POST'])
def crear_detalle_curso_paralelo(request):
    serializer = CursoParaleloSerializer(data=request.data)
    if serializer.is_valid():
        detalle_curso = serializer.save()
        return Response({
            "mensaje": "Detalle curso creado correctamente",
            "data": CursoParaleloSerializer(detalle_curso).data
        }, status=status.HTTP_201_CREATED)
    return Response({
            "mensaje": "Error al crear el detalle curso",
            "errores": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def obtener_detalle_curso_paralelo(request):
    detalle_curso = CursoParalelo.objects.all()
    serializer = CursoParaleloSerializer(detalle_curso, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def actualizar_detalle_curso_paralelo(request,id):
    try:
        detalle_curso = CursoParalelo.objects.get(id=id)
    except CursoParalelo.DoesNotExist:
        return Response(
            {"mensaje": "Detalle curso no encontrado"},
            status=status.HTTP_404_NOT_FOUND
            )
    serializer = CursoParaleloSerializer(detalle_curso, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "mensaje": "Detalle curso actualizado correctamente",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    return Response({
        "mensaje": "Error al actualizar el detalle curso",
        "errores": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_detalle_curso_paralelo(request,id):
    try:
        detalle_curso = CursoParalelo.objects.get(id=id)
        detalle_curso.delete()
        return Response(
            {"mensaje": "Detalle curso eliminado"},
            status=status.HTTP_200_OK
        )
    except CursoParalelo.DoesNotExist:
      return Response({"mensaje": "Detalle curso no encontrado"}, status=status.HTTP_404_NOT_FOUND)   