from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import (
    Dimension,Curso,Materia,
    MateriaAsignada,CursoParalelo,
    AlumnoCursoParalelo, HorarioMateria, DescripcionMateria,Profesor,
    TareaAsignada,Alumno,Actividad,Gestion,DetalleTrimestre,
    Libreta,DetalleDimension)
from Academia.serializers import MateriaAsignadaSerializer


@api_view(['GET'])
def obtener_notas_del_alumno(request, id, gestion):
    try:
        alumno = Alumno.objects.get(alumno_id=id)
    except Alumno.DoesNotExist:
        return Response({"mensaje": "El alumno no existe"}, status=status.HTTP_404_NOT_FOUND)
    
    libretas = Libreta.objects.filter(
        alumno_id=id,
        detalle_trimestre__gestion__anio_escolar=gestion
    )
    
    if not libretas.exists():
         return Response({"mensaje": "El usuario no tiene libretas"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        alumno_cursoparalelo = AlumnoCursoParalelo.objects.get(
            alumno_id=id,
            gestion_id=gestion
        )
    except AlumnoCursoParalelo.DoesNotExist:
        return Response({"mensaje": "El alumno no está asignado a ningún curso paralelo en esta gestión"}, status=status.HTTP_404_NOT_FOUND)
    
    obtener_curso = CursoParalelo.objects.get(id=alumno_cursoparalelo.curso_paralelo_id)
    
    obtener_materias = MateriaAsignada.objects.filter(
        curso_id=obtener_curso.curso_id
    )
    
    resultado = []
    
    for materia_asignada in obtener_materias:
        horarios = HorarioMateria.objects.get(
            curso_paralelo_id=alumno_cursoparalelo.curso_paralelo_id,
            descripcion_materia__materia_id=materia_asignada.materia_id
        )
        if horarios.exists():
            horarios_data = [
            {
                "hora_inicial": h.horario.hora_inicial if h.horario else None,
                "hora_final": h.horario.hora_final if h.horario else None
            } for h in horarios
        ]
        else:
            horarios_data = None  # o [] si prefieres lista vacía

        resultado.append({
        "materia_id": materia_asignada.materia_id,
        "curso_id": materia_asignada.curso_id,
        "horarios": horarios_data
        })
    
    return Response(resultado, status=status.HTTP_200_OK)

        
    
    
    
    