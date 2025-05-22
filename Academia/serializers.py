from BaseDatosColegio.models import Curso,Paralelo,Nivel,Horario,Materia7
from rest_framework import serializers

class NivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nivel
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'