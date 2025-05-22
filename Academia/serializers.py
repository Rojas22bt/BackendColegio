from BaseDatosColegio.models import Curso,Paralelo,Nivel,Horario,Materia
from rest_framework import serializers

class NivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nivel
        fields = ['id','nombre','estado']

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['id','nombre','estado','nivel']

class ParaleloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paralelo
        fields = ['id','descripcion','estado']

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = ['id','hora_inicial','hora_final']

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = ['id','nombre','descripcion','estado']