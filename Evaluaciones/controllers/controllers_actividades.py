from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from collections import OrderedDict
from datetime import datetime
from BaseDatosColegio.models import Alumno,Profesor,Materia,CursoParalelo,Horario,HorarioMateria,DescripcionMateria,Actividad,Dimension,DetalleDimension,TareaAsignada
from Evaluaciones.serializers import ActividadSerializer,DetalleDimensionSerializers,TareaAsignadaSerializers,DimensionSerializers
from Usuarios.serializers import AlumnoSerializer

@api_view(['PUT'])
def actualizar_tareas(request):
    updates = []
    for item in request.data:
        try:
            tarea = TareaAsignada.objects.get(id=item['id'])
            tarea.puntaje = item.get('puntaje', tarea.puntaje)
            updates.append(tarea)
        except TareaAsignada.DoesNotExist:
            return Response({'error': f"Tarea con ID {item['id']} no existe."}, status=404)

    TareaAsignada.objects.bulk_update(updates, ['puntaje'])
    return Response({"mensaje": "notas actualizadas"}, status=200)



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

@api_view(['POST'])
def crear_tareas(request):
    id_paralelo = request.data.get("id_cursoparalelo")
    gestion = request.data.get("gestion")

    if not id_paralelo or not gestion:
        return Response(
            {"error": "Faltan parámetros 'id_cursoparalelo' o 'gestion'."},
            status=status.HTTP_400_BAD_REQUEST
        )

    alumnos = Alumno.objects.filter(
        alumnocursoparalelo__curso_paralelo_id=id_paralelo,
        libreta__detalle_trimestre__gestion=gestion
    ).distinct()

    if not alumnos.exists():
        return Response(
            {"mensaje": "No se encontraron alumnos para esa gestión y curso-paralelo."},
            status=status.HTTP_404_NOT_FOUND
        )

    data_base = request.data.copy()
    tareas_creadas = []
    errores = []

    for alumno in alumnos:
        data = data_base.copy()
        data["alumno"] = alumno.alumno_id

        serializer = TareaAsignadaSerializers(data=data)
        if serializer.is_valid():
            tarea = serializer.save()
            tareas_creadas.append({
                "alumno": alumno.alumno_id,
                "tarea_id": tarea.id
            })
        else:
            errores.append({
                "alumno": alumno.alumno_id,
                "errores": serializer.errors
            })

    if tareas_creadas:
        return Response({
            "mensaje": "Tareas asignadas correctamente.",
            "total_asignadas": len(tareas_creadas),
            "tareas": tareas_creadas,
            "errores": errores
        }, status=status.HTTP_201_CREATED if not errores else status.HTTP_207_MULTI_STATUS)
    else:
        return Response({
            "mensaje": "No se pudo asignar ninguna tarea.",
            "errores": errores
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def obtener_tareas(request):
    id_paralelo = request.query_params.get("id_cursoparalelo")
    gestion = request.query_params.get("gestion")

    if not id_paralelo or not gestion:
        return Response({"error": "Faltan parámetros id_cursoparalelo o gestion"},
                        status=status.HTTP_400_BAD_REQUEST)

    alumnos = Alumno.objects.filter(
        alumnocursoparalelo__curso_paralelo_id=id_paralelo,
        libreta__detalle_trimestre__gestion=gestion
    ).distinct()

    serializer = AlumnoSerializer(alumnos, many=True)  # Asumiendo que ya existe
    return Response({
        "cantidad_alumnos": alumnos.count(),
        "alumnos": serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def obtener_actividades(request):
    actividades = Actividad.objects.all()
    serializer = ActividadSerializer(actividades,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
        

@api_view(['GET'])
def obtener_tareas_asignadas(request):
    id_paralelo = request.query_params.get("id_cursoparalelo")
    gestion = request.query_params.get("gestion")
    id_horario = request.query_params.get("horario_materia")
    fecha_inicio = request.query_params.get("fecha_inicio")
    fecha_fin = request.query_params.get("fecha_fin")

    if not id_paralelo or not gestion or not id_horario:
        return Response({
            "error": "Faltan parámetros: id_cursoparalelo, gestion o horario_materia"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d") if fecha_inicio else None
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d") if fecha_fin else None
    except ValueError:
        return Response({
            "error": "Las fechas deben tener el formato YYYY-MM-DD"
        }, status=status.HTTP_400_BAD_REQUEST)

    # Obtener alumnos según paralelo y gestión
    alumnos = Alumno.objects.filter(
        alumnocursoparalelo__curso_paralelo_id=id_paralelo,
        alumnocursoparalelo__gestion_id=gestion
    ).distinct()


    if not alumnos.exists():
        return Response({
            "mensaje": "No se encontraron alumnos para esa gestión, curso-paralelo y horario."
        }, status=status.HTTP_404_NOT_FOUND)

    resultado = []
    for alumno in alumnos:
        tareas_qs = TareaAsignada.objects.filter(
            alumno=alumno,
            horario_materia_id=id_horario
        )

        # ✅ Aplicar filtros por fecha si se especificaron
        if fecha_inicio_dt and fecha_fin_dt:
            tareas_qs = tareas_qs.filter(fecha_entrega__range=(fecha_inicio_dt, fecha_fin_dt))
        elif fecha_inicio_dt:
            tareas_qs = tareas_qs.filter(fecha_entrega__gte=fecha_inicio_dt)
        elif fecha_fin_dt:
            tareas_qs = tareas_qs.filter(fecha_entrega__lte=fecha_fin_dt)

        tareas_serializer = TareaAsignadaSerializers(tareas_qs, many=True)
        resultado.append({
            "alumno_id": alumno.alumno_id,
            "nombre": alumno.alumno.nombre,
            "tareas": tareas_serializer.data
        })

    return Response(resultado, status=status.HTTP_200_OK)

@api_view(['GET'])
def obtener_dimensiones_actividades_tareas(request):
    id_paralelo = request.query_params.get("id_cursoparalelo")
    gestion = request.query_params.get("gestion")
    id_horario = request.query_params.get("horario_materia")
    fecha_inicio = request.query_params.get("fecha_inicio")
    fecha_fin = request.query_params.get("fecha_fin")

    if not id_paralelo or not gestion or not id_horario:
        return Response({
            "error": "Faltan parámetros: id_cursoparalelo, gestion o horario_materia"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d") if fecha_inicio else None
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d") if fecha_fin else None
    except ValueError:
        return Response({
            "error": "Las fechas deben tener el formato YYYY-MM-DD"
        }, status=status.HTTP_400_BAD_REQUEST)

    resultado = []
    dimensiones = Dimension.objects.all()

    for dimension in dimensiones:
        actividades = Actividad.objects.filter(
            id__in=DetalleDimension.objects.filter(dimension=dimension).values_list('actividad_id', flat=True)
        )

        actividades_data = []
        for actividad in actividades:
            tareas_qs = TareaAsignada.objects.filter(
                actividad=actividad,
                horario_materia_id=id_horario,
                alumno__alumnocursoparalelo__curso_paralelo_id=id_paralelo,
                alumno__alumnocursoparalelo__gestion_id=gestion
            ).distinct()

            # ✅ Aplicar filtro por fechas si se proporcionaron
            if fecha_inicio_dt and fecha_fin_dt:
                tareas_qs = tareas_qs.filter(fecha_entrega__range=(fecha_inicio_dt, fecha_fin_dt))
            elif fecha_inicio_dt:
                tareas_qs = tareas_qs.filter(fecha_entrega__gte=fecha_inicio_dt)
            elif fecha_fin_dt:
                tareas_qs = tareas_qs.filter(fecha_entrega__lte=fecha_fin_dt)

            tareas_unicas = OrderedDict()
            for tarea in tareas_qs:
                if tarea.descripcion not in tareas_unicas:
                    tareas_unicas[tarea.descripcion] = tarea

            tareas_serializadas = TareaAsignadaSerializers(tareas_unicas.values(), many=True).data

            actividades_data.append({
                "id": actividad.id,
                "nombre": actividad.nombre,
                "estado": actividad.estado,
                "tareas": tareas_serializadas
            })

        resultado.append({
            "dimension": {
                "id": dimension.id,
                "descripcion": dimension.descripcion,
                "puntaje": dimension.puntaje
            },
            "actividades": actividades_data
        })

    return Response(resultado, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def obtener_dimensiones_actividades_tareas(request):
#     id_paralelo = request.query_params.get("id_cursoparalelo")
#     gestion = request.query_params.get("gestion")
#     id_horario = request.query_params.get("horario_materia")

#     if not id_paralelo or not gestion or not id_horario:
#         return Response({
#             "error": "Faltan parámetros: id_cursoparalelo, gestion o horario_materia"
#         }, status=status.HTTP_400_BAD_REQUEST)

#     resultado = []

#     dimensiones = Dimension.objects.all()
#     for dimension in dimensiones:
#         actividades = Actividad.objects.filter(
#             id__in=DetalleDimension.objects.filter(dimension=dimension).values_list('actividad_id', flat=True)
#         )

#         actividades_data = []
#         for actividad in actividades:
#             tareas = TareaAsignada.objects.filter(
#                 actividad=actividad,
#                 horario_materia_id=id_horario,
#                 alumno__alumnocursoparalelo__curso_paralelo_id=id_paralelo,
#                 alumno__libreta__detalle_trimestre__gestion=gestion
#             ).distinct()

#             # ✅ Filtrar una tarea por cada descripción única
#             tareas_unicas = OrderedDict()
#             for tarea in tareas:
#                 if tarea.descripcion not in tareas_unicas:
#                     tareas_unicas[tarea.descripcion] = tarea

#             tareas_serializadas = TareaAsignadaSerializers(tareas_unicas.values(), many=True).data

#             actividades_data.append({
#                 "id": actividad.id,
#                 "nombre": actividad.nombre,
#                 "estado": actividad.estado,
#                 "tareas": tareas_serializadas
#             })

#         resultado.append({
#             "dimension": {
#                 "id": dimension.id,
#                 "descripcion": dimension.descripcion,
#                 "puntaje": dimension.puntaje
#             },
#             "actividades": actividades_data
#         })

#     return Response(resultado, status=status.HTTP_200_OK)


# @api_view(['GET'])
# def obtener_tareas_y_actividades_por_horario(request):
#     id_paralelo = request.query_params.get("id_cursoparalelo")
#     gestion = request.query_params.get("gestion")
#     id_horario = request.query_params.get("horario_materia")

#     if not id_paralelo or not gestion or not id_horario:
#         return Response({
#             "error": "Faltan parámetros: id_cursoparalelo, gestion o horario_materia"
#         }, status=status.HTTP_400_BAD_REQUEST)

#     alumnos = Alumno.objects.filter(
#         alumnocursoparalelo__curso_paralelo_id=id_paralelo,
#         libreta__detalle_trimestre__gestion=gestion
#     ).distinct()

#     if not alumnos.exists():
#         return Response({
#             "mensaje": "No se encontraron alumnos para esa gestión, curso-paralelo y horario."
#         }, status=status.HTTP_404_NOT_FOUND)

#     resultado = []

#     for alumno in alumnos:
#         tareas = TareaAsignada.objects.filter(
#             alumno=alumno,
#             horario_materia_id=id_horario
#         ).select_related('actividad')

#         tareas_info = []
#         for tarea in tareas:
#             # Obtener dimensiones relacionadas a la actividad
#             detalles = DetalleDimension.objects.filter(actividad=tarea.actividad)
#             dimensiones = DimensionSerializers([detalle.dimension for detalle in detalles], many=True).data

#             tarea_data = {
#                 "id": tarea.id,
#                 "descripcion": tarea.descripcion,
#                 "puntaje": tarea.puntaje,
#                 "fecha_inicio": tarea.fecha_inicio,
#                 "fecha_entrega": tarea.fecha_entrega,
#                 "estado": tarea.estado,
#                 "actividad": {
#                     "id": tarea.actividad.id,
#                     "nombre": tarea.actividad.nombre,
#                     "estado": tarea.actividad.estado,
#                     "dimensiones": dimensiones
#                 }
#             }
#             tareas_info.append(tarea_data)

#         resultado.append({
#             "alumno_id": alumno.alumno_id,
#             "nombre": alumno.alumno.nombre,
#             "tareas": tareas_info
#         })

#     return Response(resultado, status=status.HTTP_200_OK)
