from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import CursoParalelo,MateriaAsignada
from Academia.serializers import MateriaAsignadaSerializer,CursoParaleloSerializer

#CRUD DE DETALLE CURSO MATERIA
@api_view(['POST'])
def crear_detalle_curso_materia(request):
    curso_id = request.data.get('curso')
    materias = request.data.get('materias', [])

    if not curso_id or not materias:
        return Response({"mensaje": "Faltan datos: 'curso' y 'materias'"}, status=status.HTTP_400_BAD_REQUEST)

    creados = []
    errores = []

    for materia_id in materias:
        serializer = MateriaAsignadaSerializer(data={
            "curso": curso_id,
            "materia": materia_id
        })
        if serializer.is_valid():
            detalle = serializer.save()
            creados.append(MateriaAsignadaSerializer(detalle).data)
        else:
            errores.append({f"materia_id {materia_id}": serializer.errors})

    if errores:
        return Response({
            "mensaje": "Algunas asignaciones no se pudieron crear",
            "creados": creados,
            "errores": errores
        }, status=status.HTTP_207_MULTI_STATUS)

    return Response({
        "mensaje": "Todas las asignaciones creadas correctamente",
        "data": creados
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def obtener_detalle_curso_materia(request):
    detalle_curso = MateriaAsignada.objects.all()
    serializer = MateriaAsignadaSerializer(detalle_curso, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def actualizar_detalle_curso_materia(request):
    materia_id = request.data.get('materia')
    curso_id = request.data.get('curso')

    if not materia_id or not curso_id:
        return Response({"mensaje": "Se requieren 'materia' y 'curso'"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        detalle_curso = MateriaAsignada.objects.get(materia_id=materia_id, curso_id=curso_id)
    except MateriaAsignada.DoesNotExist:
        return Response({"mensaje": "Detalle curso no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = MateriaAsignadaSerializer(detalle_curso, data=request.data, partial=True)
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
def eliminar_detalle_curso_materia(request):
    materia_id = request.data.get('materia')
    curso_id = request.data.get('curso')

    if not materia_id or not curso_id:
        return Response({"mensaje": "Se requieren 'materia' y 'curso'"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        detalle_curso = MateriaAsignada.objects.get(materia_id=materia_id, curso_id=curso_id)
        detalle_curso.delete()
        return Response({"mensaje": "Detalle curso eliminado"}, status=status.HTTP_200_OK)
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