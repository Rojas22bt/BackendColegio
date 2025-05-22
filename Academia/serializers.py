from BaseDatosColegio.models import Curso,Paralelo,Nivel,Horario,Materia7
from rest_framework import serializers

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'