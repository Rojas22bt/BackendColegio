from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Alumno,Profesor,Materia,CursoParalelo,Horario,HorarioMateria,DescripcionMateria,Actividad,Dimension,DetalleDimension,TareaAsignada
from Evaluaciones.serializers import ActividadSerializer,DetalleDimensionSerializers


@api_view(['POST'])
def crear_actividad(request):
    id_dimension = request.data.get("dimension")
    try:
        dimension = Dimension.objects.get(id=id_dimension)
    except Dimension.DoesNotExist:
        return Response({"mensaje": "No existe la dimensión seleccionada"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ActividadSerializer(data=request.data)
    if serializer.is_valid():
        actividad = serializer.save()
        data = {
            "actividad": actividad.id,
            "dimension": dimension.id
        }

        serializer2 = DetalleDimensionSerializers(data=data)
        if serializer2.is_valid():
            serializer2.save()
            return Response({
                "mensaje": "Registrado correctamente",
                "data": ActividadSerializer(actividad).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "mensaje": "Error al registrar detalle de dimensión",
                "errores": serializer2.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "mensaje": "Ocurrió un problema al registrar la actividad",
        "errores": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
        