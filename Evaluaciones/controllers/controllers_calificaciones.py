from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import (
    Dimension,Curso,Materia,
    MateriaAsignada,CursoParalelo,
    AlumnoCursoParalelo, HorarioMateria, DescripcionMateria,Profesor,
    TareaAsignada,Alumno,Actividad,Gestion,DetalleTrimestre,
    Libreta,DetalleDimension)
from Evaluaciones.serializers import DimensionSerializers


@api_view(['GET'])
def obtener_notas_del_alumno(request,id,gestion):
    try:
        alumno = Alumno.objects.get(id=id)
    except Alumno.DoesNotExist:
        return Response({"mensaje": "El usuario no existe"}, status=status.HTTP_404_NOT_FOUND)
    
    obtener_libretas = Libreta.objects.filter(
        alumno_id = id,
        detalle_trimestre__gestion = gestion
    )
    
    if not obtener_libretas.exists():
         return Response({"mensaje": "El usuario no tiene llibretas"}, status=status.HTTP_404_NOT_FOUND)
    
    obtener_alumnocursoparalelo = AlumnoCursoParalelo.objects.get()
    
    
    
    