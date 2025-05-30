from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Libreta , DetalleTrimestre, Alumno,CursoParalelo
from Academia.serializers import LibretaSerializers,AlumnoParaleloSerializers


@api_view(['POST'])
def crear_libreta(request):
    gestion = request.data.get("gestion")
    id_curso = request.data.get("curso")
    id_paralelo = request.data.get("paralelo")
    id_alumno = request.data.get("alumno")
    anio_escolar = request.data.get("anio_escolar")

    # Validar curso-paralelo
    try:
        curso_paralelo = CursoParalelo.objects.get(curso_id=id_curso, paralelo_id=id_paralelo)
    except CursoParalelo.DoesNotExist:
        return Response({"mensaje": "No se encontró el curso-paralelo especificado."},
                        status=status.HTTP_404_NOT_FOUND)

    # Obtener trimestres
    detalle_trimestres = DetalleTrimestre.objects.filter(gestion=gestion)
    if not detalle_trimestres.exists():
        return Response({"mensaje": "No se encontraron trimestres para la gestión."},
                        status=status.HTTP_404_NOT_FOUND)

    respuestas = []
    errores = []

    for detalle in detalle_trimestres:
        data = request.data.copy()
        data["detalle_trimestre"] = detalle.id
        data["aprobado"] = True

        serializer = LibretaSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            respuestas.append({
                "datos": serializer.data,
                "id_detalle_trimestre": detalle.id,
                "trimestre_id": detalle.trimestre_id,
                "id_gestion": detalle.gestion_id
            })
        else:
            errores.append({
                "detalle_id": detalle.id,
                "errors": serializer.errors
            })

    # Solo registrar alumno-curso si hay al menos una libreta creada
    if respuestas:
        data_alumno = {
            "alumno": id_alumno,
            "curso_paralelo": curso_paralelo.id,
            "gestion_id":anio_escolar
        }
        serializer3 = AlumnoParaleloSerializers(data=data_alumno)
        if serializer3.is_valid():
            serializer3.save()
        else:
            errores.append({"alumno_curso": serializer3.errors})

        return Response({
            "mensaje": "Se registraron algunas libretas.",
            "registradas": respuestas,
            "errores": errores
        }, status=status.HTTP_207_MULTI_STATUS if errores else status.HTTP_201_CREATED)
    else:
        return Response({
            "mensaje": "Ninguna libreta fue registrada.",
            "errores": errores
        }, status=status.HTTP_400_BAD_REQUEST)
