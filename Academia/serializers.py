from BaseDatosColegio.models import Curso,Paralelo,Nivel,Horario,Materia,CursoParalelo,MateriaAsignada,DescripcionMateria
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
        fields = ['id','hora_inicial','hora_final','estado']

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = ['id','nombre','descripcion','estado']
    
class CursoParaleloSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoParalelo
        fields = ['curso','paralelo']
    
class MateriaAsignadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MateriaAsignada
        fields = ['curso','materia']

class DescripcionMateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescripcionMateria
        fields = ['id','profesor','materia']