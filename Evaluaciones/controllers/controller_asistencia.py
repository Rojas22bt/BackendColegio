from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Asistencia, Gestion,Bitacora,Usuario
from django.db.models.functions import ExtractYear
from Evaluaciones.serializers import AsistenciaSerializers

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@api_view(['POST'])
def obtener_asistencia_de_alumnos(request):
    resultado = []

    fecha = request.data.get("fecha")
    alumnos = request.data.get("alumnos", [])

    for alumno in alumnos:
        alumno_id = alumno.get("id")

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
    serializer = AsistenciaSerializers(data=request.data)
    usuario_id = request.data.get("alumno")  # este es el ID del usuario
    
    if serializer.is_valid():
        serializer.save()
        
        # Obtener instancia del usuario
        try:
            usuario_instancia = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            usuario_instancia = None  # o manejar error de otra forma
        
        # Bitácora
        ip = get_client_ip(request)
        if usuario_instancia:
            Bitacora.objects.create(
                usuario=usuario_instancia,
                accion="Registro de asistencia",
                ip=ip
            )
        else:
            # Manejar caso usuario no encontrado o saltar bitácora
            pass
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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


@api_view(['GET'])
def obtener_asistencia_por_gestion(request, id):
    resultado = []

    gestiones = Gestion.objects.all()

    for gestion in gestiones:
        # Filtra asistencias cuyo año de la fecha coincide con gestion.anio_escolar
        asistencias = Asistencia.objects.filter(
            alumno_id=id,
            fecha__year=gestion.anio_escolar
        )

        resultado.append({
            "year": gestion.anio_escolar,
            "gestion": gestion.anio_escolar,
            "asistencia": asistencias.count(),
            "mensaje": "salio todo bien"
        })

    return Response(resultado, status=status.HTTP_200_OK)
