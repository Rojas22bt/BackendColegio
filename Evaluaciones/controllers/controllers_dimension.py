from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Dimension
from Evaluaciones.serializers import DimensionSerializers

@api_view(['POST'])
def crear_dimension(request):
    serializer = DimensionSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"mensaje": "Registro exitoso", "data": serializer.data},
            status=status.HTTP_201_CREATED  
        )
    return Response(
        {"mensaje": "Error de validación", "errores": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST  
    )


@api_view(['GET'])
def obtener_dimensiones(request):
    dimensiones = Dimension.objects.all()
    serializer = DimensionSerializers(dimensiones, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def actualizar_dimension(request, id):
    try:
        dimension = Dimension.objects.get(id=id)
    except Dimension.DoesNotExist:
        return Response({"mensaje": "Dimensión no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = DimensionSerializers(dimension, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje": "Dimensión actualizada correctamente", "data": serializer.data}, status=status.HTTP_200_OK)
    
    return Response({"mensaje": "Error de validación", "errores": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def eliminar_dimension(request, id):
    try:
        dimension = Dimension.objects.get(id=id)
        dimension.delete()
        return Response({"mensaje": "Dimensión eliminada correctamente"}, status=status.HTTP_200_OK)
    except Dimension.DoesNotExist:
        return Response({"mensaje": "Dimensión no encontrada"}, status=status.HTTP_404_NOT_FOUND)
