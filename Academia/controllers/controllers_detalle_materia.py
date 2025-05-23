from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import DescripcionMateria,Profesor,Materia,CursoParalelo,Horario,HorarioMateria,Curso,Paralelo,Usuario
from Academia.serializers import DescripcionMateriaSerializer,DescripcionHorarioSerializer,MateriaSerializer
from Usuarios.serializers import UsuarioSerializer

@api_view(['GET'])
def obtener_descripcion_completa(request):
    descripciones = DescripcionMateria.objects.all()
    resultado = []

    for descripcion in descripciones:
        horarios = HorarioMateria.objects.filter(descripcion_materia=descripcion)
        descripcion_serializada = DescripcionMateriaSerializer(descripcion).data
        horarios_serializados = DescripcionHorarioSerializer(horarios, many=True).data

        #agregarNombreProfesor
        profesor_id = descripcion_serializada["profesor"]
        profesor = Usuario.objects.get(id=profesor_id)
        obtenerProfesor = UsuarioSerializer(profesor).data
        descripcion_serializada["profesor_nombre"] = obtenerProfesor["nombre"]
        #agregamosNombreMateria
        materia_id = descripcion_serializada["materia"]
        materia = Materia.objects.get(id=materia_id)
        obtenerMateria = MateriaSerializer(materia).data
        descripcion_serializada["materia_nombre"] = obtenerMateria["nombre"]

        resultado.append({
            "descripcion": descripcion_serializada,
            "horarios": horarios_serializados,
            "id":descripcion_serializada["materia"] 
        })

    return Response(resultado, status=status.HTTP_200_OK)

        
@api_view(['POST'])
def crear_descripcion_completa(request):
    # 1. Crear la DescripcionMateria
    data1 = {
        "profesor": request.data.get("profesor"),
        "materia": request.data.get("materia")
    }
    serializer1 = DescripcionMateriaSerializer(data=data1)

    if serializer1.is_valid():
        descripcion_materia = serializer1.save()  # ya tienes la instancia guardada

        # 2. Obtener o crear el CursoParalelo
        curso_id = request.data.get("curso")
        paralelo_id = request.data.get("paralelo")
        try:
            curso = Curso.objects.get(id=curso_id)
            paralelo = Paralelo.objects.get(id=paralelo_id)
        except (Curso.DoesNotExist, Paralelo.DoesNotExist):
            return Response({"error": "Curso o Paralelo no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

        curso_paralelo, _ = CursoParalelo.objects.get_or_create(curso=curso, paralelo=paralelo)

        # 3. Crear el HorarioMateria
        data2 = {
            "curso_paralelo": curso_paralelo.id,
            "descripcion_materia": descripcion_materia.id,
            "horario": request.data.get("horario")
        }

        serializer2 = DescripcionHorarioSerializer(data=data2)
        if serializer2.is_valid():
            serializer2.save()
            return Response({
                "descripcion_materia": serializer1.data,
                "horario_materia": serializer2.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer2.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)
