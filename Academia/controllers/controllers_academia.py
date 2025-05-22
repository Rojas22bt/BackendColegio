from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from BaseDatosColegio.models import Curso
from Academia.serializers import CursoSerializer

@api_view(['get'])
def obtener_cursos(request):
    curso = Curso.objects.all()
    serializer = CursoSerializer(curso, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
