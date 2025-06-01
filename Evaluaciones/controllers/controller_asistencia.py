from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Asistencia
from Evaluaciones.serializers import AsistenciaSerializers

@api_view(['POST'])
def obtener_asistencia_de_alumnos(request):
    resultado = []
    
    for alumno in request.data:
        alumno_id = alumno.get("id")
        fecha = alumno.get("fecha")
        
        asistencias = Asistencia.objects.filter(
            alumno_id=alumno_id,
            fecha=fecha
        )

        if not asistencias.exists():
            resultado.append({
                "alumno_id": alumno_id,
                "fecha": fecha,
                "estado": "No hay registro"
            })
        else:
            for asistencia in asistencias:
                resultado.append({
                    "alumno_id": alumno_id,
                    "fecha": asistencia.fecha,
                    "estado": asistencia.estado
                })

    return Response(resultado, status=status.HTTP_200_OK)

@api_view(['POST'])
def crear_asistencia(request):
    serializer = AsistenciaSerializers(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    return Response({
        "mensaje": "Ocurrió algún problema al guardar la asistencia.",
        "errores": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def actualizar_asistencia(request,id):
    try:
        encontrado = Asistencia.objects.get(id=id)
    except Asistencia.DoesNotExist:
        return Response({"mensaje": "Asistencia no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = AsistenciaSerializers(encontrado,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje": "Asistencia actualizada correctamente", "data": serializer.data}, status=status.HTTP_200_OK)
    
    return Response({"mensaje": "Error de validación", "errores": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)