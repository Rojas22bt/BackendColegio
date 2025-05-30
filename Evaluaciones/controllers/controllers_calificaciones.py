from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import (
    Dimension, Curso, Materia,TareaAsignada,
    MateriaAsignada, CursoParalelo,
    AlumnoCursoParalelo, HorarioMateria,
    DetalleTrimestre, Libreta)
from Periodo.serializers import TrimestreSerializers


@api_view(['GET'])
def obtener_notas_del_alumno(request, id, gestion):
    try:
        alumno = AlumnoCursoParalelo.objects.get(alumno_id=id, gestion_id=gestion)
    except AlumnoCursoParalelo.DoesNotExist:
        return Response({"mensaje": "El alumno no está asignado a ningún curso paralelo en esta gestión"}, status=status.HTTP_404_NOT_FOUND)
    
    # Verificar libretas
    if not Libreta.objects.filter(alumno_id=id, detalle_trimestre__gestion__anio_escolar=gestion).exists():
        return Response({"mensaje": "El alumno no tiene libretas en esta gestión"}, status=status.HTTP_404_NOT_FOUND)

    curso_paralelo = CursoParalelo.objects.get(id=alumno.curso_paralelo_id)
    materias_asignadas = MateriaAsignada.objects.filter(curso_id=curso_paralelo.curso_id)

    detalles = DetalleTrimestre.objects.filter(gestion__anio_escolar=gestion)
    trimestres = [detalle.trimestre for detalle in detalles]
    trimestre_serializer = TrimestreSerializers(trimestres, many=True)

    resultado = []

    for trimestre in trimestre_serializer.data:
        fecha_inicio = trimestre.get("fecha_inicio")
        fecha_fin = trimestre.get("fecha_final")

        for materia_asignada in materias_asignadas:
            horarios = HorarioMateria.objects.filter(
                curso_paralelo_id=alumno.curso_paralelo_id,
                descripcion_materia__materia_id=materia_asignada.materia_id
            )
            if horarios.exists():
                horario_id = horarios.first().id
            else:
                horario_id = None

            # Obtener dimensiones con promedio para esa materia, horario y rango de fechas
            dimensiones_promedios = obtener_promedios_por_dimension(horario_id, fecha_inicio, fecha_fin, id)

            resultado.append({
                "materia_id": materia_asignada.materia.id,
                "nombre_materia": materia_asignada.materia.nombre,
                "trimestre": {
                    "id": trimestre.get("id"),
                    "nro": trimestre.get("nro"),
                    "fecha_inicio": fecha_inicio,
                    "fecha_final": fecha_fin
                },
                "dimensiones": dimensiones_promedios
            })

    return Response(resultado, status=status.HTTP_200_OK)


def obtener_promedios_por_dimension(horario_id, fecha_inicio, fecha_final, alumno_id):
    dimensiones = Dimension.objects.all()
    resultado = []

    for dimension in dimensiones:
        # IDs actividades vinculadas a la dimensión
        actividades_ids = dimension.detalledimension_set.values_list('actividad_id', flat=True)

        # Filtrar tareas que estén dentro del rango y vinculadas a actividades y horario
        tareas = TareaAsignada.objects.filter(
            fecha_inicio__gte=fecha_inicio,
            fecha_entrega__lte=fecha_final,
            alumno_id=alumno_id,
            horario_materia_id=horario_id,
            actividad_id__in=actividades_ids,
            estado=True
        )

        total_puntaje = sum(t.puntaje for t in tareas)
        cantidad = tareas.count()
        nota_mayor = cantidad * 100
        promedio = (total_puntaje * dimension.puntaje) / nota_mayor if cantidad > 0 else None

        resultado.append({
            "dimension_id": dimension.id,
            "descripcion": dimension.descripcion,
            "promedio": promedio
        })

    return resultado




# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.db.models import Q
# from BaseDatosColegio.models import (
#     Dimension,Curso,Materia,Trimestre,
#     MateriaAsignada,CursoParalelo,
#     AlumnoCursoParalelo, HorarioMateria, DescripcionMateria,Profesor,
#     TareaAsignada,Alumno,Actividad,Gestion,DetalleTrimestre,
#     Libreta,DetalleDimension)
# from Academia.serializers import MateriaAsignadaSerializer
# from Periodo.serializers import TrimestreSerializers


# @api_view(['GET'])
# def obtener_notas_del_alumno(request, id, gestion):
#     try:
#         alumno = Alumno.objects.get(alumno_id=id)
#     except Alumno.DoesNotExist:
#         return Response({"mensaje": "El alumno no existe"}, status=status.HTTP_404_NOT_FOUND)
    
#     libretas = Libreta.objects.filter(
#         alumno_id=id,
#         detalle_trimestre__gestion__anio_escolar=gestion
#     )
    
#     if not libretas.exists():
#          return Response({"mensaje": "El usuario no tiene libretas"}, status=status.HTTP_404_NOT_FOUND)
    
#     try:
#         alumno_cursoparalelo = AlumnoCursoParalelo.objects.get(
#             alumno_id=id,
#             gestion_id=gestion
#         )
#     except AlumnoCursoParalelo.DoesNotExist:
#         return Response({"mensaje": "El alumno no está asignado a ningún curso paralelo en esta gestión"}, status=status.HTTP_404_NOT_FOUND)
    
#     obtener_curso = CursoParalelo.objects.get(id=alumno_cursoparalelo.curso_paralelo_id)
    
#     obtener_materias = MateriaAsignada.objects.filter(
#         curso_id=obtener_curso.curso_id
#     )
    
#     detalles = DetalleTrimestre.objects.filter(
#     gestion__anio_escolar=gestion
#     )

#     trimestres = [detalle.trimestre for detalle in detalles]
    
#     serializer = TrimestreSerializers(trimestres,many=True)
    
#     resultado = []

#     for trimestre in serializer.data:
#         fecha_inicio = trimestre.get("fecha_inicio")
#         fecha_fin = trimestre.get("fecha_final")        
        
#         for materia_asignada in obtener_materias:
#             horarios = HorarioMateria.objects.filter(
#                 curso_paralelo_id=alumno_cursoparalelo.curso_paralelo_id,
#                 descripcion_materia__materia_id=materia_asignada.materia_id
#             )
#             if horarios.exists():
#                 horario_id = horarios.first().id
#                 horarios_data = [
#                     {
#                         "hora_inicial": h.horario.hora_inicial if h.horario else None,
#                         "hora_final": h.horario.hora_final if h.horario else None
#                     } for h in horarios
#                 ]
#                 notas_dimension = obtener_nota_materia(horario_id, fecha_inicio, fecha_fin, id)
                
#             else:
#                 horarios_data = None
#                 horario_id = None
#                 notas_dimension = []

#             resultado.append({
#                 "materia_id": materia_asignada.materia_id,
#                 "trimetre": trimestre,
#                 "curso_id": materia_asignada.curso_id,
#                 "horario_id": horario_id,
#                 "horarios": horarios_data,
#                 "notas_por_dimension": notas_dimension
#             })

#     return Response(resultado, status=status.HTTP_200_OK)

        
# def obtener_nota_materia(horario_id, fecha_inicio, fecha_final, alumno_id):
#     dimensiones = Dimension.objects.all()
#     resultado = []

#     for dimension in dimensiones:
#         # IDs de actividades de la dimensión
#         actividades_ids = DetalleDimension.objects.filter(
#             dimension_id=dimension.id
#         ).values_list('actividad_id', flat=True)

#         # Obtén todas las actividades relacionadas
#         actividades = Actividad.objects.filter(id__in=actividades_ids)

#         # Filtra tareas de alumno para estas actividades, rango fechas y horario
#         tareas = TareaAsignada.objects.filter(
#         fecha_inicio__gte=fecha_inicio,
#         fecha_entrega__lte=fecha_final,
#         alumno_id=alumno_id,
#         horario_materia_id=horario_id,
#         actividad_id__in=actividades_ids,
#         estado=True
#         )


#         total_puntaje = sum(t.puntaje for t in tareas)
#         cantidad = tareas.count()
#         notaMayor = cantidad * 100
#         promedio = (total_puntaje* dimension.puntaje) /notaMayor if cantidad > 0 else None

#         # Para cada actividad, filtrar sus tareas específicas
#         actividades_data = []
#         for act in actividades:
#             tareas_actividad = tareas.filter(actividad_id=act.id)
#             tareas_data = [
#                 {
#                     "id": t.id,
#                     "descripcion": t.descripcion,
#                     "puntaje": t.puntaje,
#                     "fecha_inicio": t.fecha_inicio,
#                     "fecha_entrega": t.fecha_entrega,
#                     "estado": t.estado,
#                 } for t in tareas_actividad
#             ]
#             actividades_data.append({
#                 "id": act.id,
#                 "nombre": act.nombre,
#                 "tareas": tareas_data
#             })

#         resultado.append({
#             "dimension_id": dimension.id,
#             "dimension_descripcion": dimension.descripcion,
#             "total_puntaje": total_puntaje,
#             "cantidad_tareas": cantidad,
#             "promedio": promedio,
#             "actividades": actividades_data,
#             "fecha_final": fecha_final,
#             "fecha_inicio": fecha_inicio
#         })

#     return resultado

  
    