from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Alumno,Profesor,Materia,CursoParalelo,Horario,HorarioMateria,DescripcionMateria,Actividad,Dimension,DetalleDimension,TareaAsignada
from Evaluaciones.serializers import ActividadSerializer,DetalleDimensionSerializers,TareaAsignadaSerializers
from Usuarios.serializers import AlumnoSerializer


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
        