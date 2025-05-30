from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Trimestre
from Periodo.serializers import TrimestreSerializers,DetalleTrimestreSerializer



@api_view(['POST'])
def crear_trimestre(request):
    serializer = TrimestreSerializers(data=request.data)
    if serializer.is_valid():
        trimestre = serializer.save()
        data = request.data.copy()
        data["trimestre"]= trimestre.id
        serializer2 = DetalleTrimestreSerializer(data=data)
        if serializer2.is_valid():
            serializer2.save()
            return Response({"mensaje":"registrado correctamente"},status=status.HTTP_201_CREATED)
        return Response({"erros":serializer2.errors},status=status.HTTP_400_BAD_REQUEST)
    return Response({"erros":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    

@api_view(['GET'])
def obtener_trimestres(request):
    trimestre = Trimestre.objects.all()
    serializer = TrimestreSerializers(trimestre,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['PUT'])
def actualizar_trimestre(request,id):
    try:
        trimestre = Trimestre.objects.get(id=id)
    except Trimestre.DoesNotExist:
        return Response({"mensaje": "Asistencia no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    serializer = TrimestreSerializers(trimestre,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje": "Trimestre actualizada correctamente", "data": serializer.data}, status=status.HTTP_200_OK)
    
    return Response({"mensaje": "Error de validación", "errores": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_trimestre(request,id):
    try:
        trimestre = Trimestre.objects.get(id=id)
        trimestre.delete()
        return Response({"mensaje":"eliminado correctamente"},status=status.HTTP_200_OK)
    except Trimestre.DoesNotExist:
        return Response({"mensaje": "Nivel no encontrado"}, status=status.HTTP_404_NOT_FOUND)   