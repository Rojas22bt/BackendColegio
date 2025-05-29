from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from BaseDatosColegio.models import (
    Dimension,Curso,Materia,Trimestre,
    MateriaAsignada,CursoParalelo,
    AlumnoCursoParalelo, HorarioMateria, DescripcionMateria,Profesor,
    TareaAsignada,Alumno,Actividad,Gestion,DetalleTrimestre,
    Libreta,DetalleDimension)
from Academia.serializers import MateriaAsignadaSerializer
from Periodo.serializers import TrimestreSerializers


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
    
    detalles = DetalleTrimestre.objects.filter(
    gestion__anio_escolar=gestion
    )

    trimestres = [detalle.trimestre for detalle in detalles]
    
    serializer = TrimestreSerializers(trimestres,many=True)
    
    for trimestre in trimestres:
        
        fecha_inicio = trimestre.fecha_inicio
        fecha_fin = trimestre.fecha_final        
        resultado = []
        
        for materia_asignada in obtener_materias:
            horarios = HorarioMateria.objects.filter(
                curso_paralelo_id=alumno_cursoparalelo.curso_paralelo_id,
                descripcion_materia__materia_id=materia_asignada.materia_id
            )
            if horarios.exists():
                horario_id = horarios.first().id
                horarios_data = [
                    {
                        "hora_inicial": h.horario.hora_inicial if h.horario else None,
                        "hora_final": h.horario.hora_final if h.horario else None
                    } for h in horarios
                ]
                notas_dimension = obtener_nota_materia(horario_id, fecha_inicio, fecha_fin, id)
                
            else:
                horarios_data = None  # o [] si prefieres lista vacía
                horario_id = None
                notas_dimension = []

            resultado.append({
            "materia_id": materia_asignada.materia_id,
            "trimetre": serializer.data,
            "curso_id": materia_asignada.curso_id,
            "horario_id": horario_id,
            "horarios": horarios_data,
            "notas_por_dimension": notas_dimension
            })
    
    return Response(resultado, status=status.HTTP_200_OK)

        
def obtener_nota_materia(horario_id, fecha_inicio, fecha_final, alumno_id):
    dimensiones = Dimension.objects.all()
    resultado = []

    for dimension in dimensiones:
        # Obtiene IDs de actividades vinculadas a la dimensión
        actividades_ids = DetalleDimension.objects.filter(
            dimension_id=dimension.id
        ).values_list('actividad_id', flat=True)

        # Recupera las actividades completas
        actividades = Actividad.objects.filter(id__in=actividades_ids)

        # Filtra tareas del alumno para esas actividades, en rango fechas y horario_materia
        tareas_de_dimension = TareaAsignada.objects.filter(
            fecha_inicio__gte=fecha_inicio,
            fecha_entrega__lte=fecha_final,
            alumno_id=alumno_id,
            horario_materia_id=horario_id,
            actividad_id__in=actividades_ids,
            estado=True  # Opcional: solo tareas activas
        )

        total_puntaje = sum(t.puntaje for t in tareas_de_dimension)
        cantidad = tareas_de_dimension.count()
        promedio = total_puntaje / cantidad if cantidad > 0 else None

        # Serializa las actividades que quieres mostrar
        actividades_data = [
            {
                "id": act.id,
                "nombre": act.nombre,
                # agrega más campos si quieres
            } for act in actividades
        ]

        resultado.append({
            "dimension_id": dimension.id,
            "dimension_descripcion": dimension.descripcion,
            "total_puntaje": total_puntaje,
            "cantidad_tareas": cantidad,
            "promedio": promedio,
            "actividades": actividades_data
        })

    return resultado


  
    