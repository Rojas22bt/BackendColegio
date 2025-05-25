from BaseDatosColegio.models import Curso,Paralelo,Nivel,Horario,Materia,CursoParalelo,MateriaAsignada,DescripcionMateria,HorarioMateria
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
        fields = ['id','curso','paralelo']
    
class MateriaAsignadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MateriaAsignada
        fields = ['curso','materia']

class DescripcionMateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescripcionMateria
        fields = ['id','profesor','materia']
        
class DescripcionHorarioSerializer(serializers.ModelSerializer):
    nombre_curso = serializers.SerializerMethodField()
    descripcion_paralelo = serializers.SerializerMethodField()
    hora_inicial = serializers.SerializerMethodField()
    hora_final = serializers.SerializerMethodField()

    class Meta:
        model = HorarioMateria
        fields = [
            'id', 'curso_paralelo', 'descripcion_materia', 'horario',
            'nombre_curso', 'descripcion_paralelo', 'hora_inicial', 'hora_final'
        ]

    def get_nombre_curso(self, obj):
        return obj.curso_paralelo.curso.nombre if obj.curso_paralelo and obj.curso_paralelo.curso else None

    def get_descripcion_paralelo(self, obj):
        return obj.curso_paralelo.paralelo.descripcion if obj.curso_paralelo and obj.curso_paralelo.paralelo else None

    def get_hora_inicial(self, obj):
        return obj.horario.hora_inicial if obj.horario else None

    def get_hora_final(self, obj):
        return obj.horario.hora_final if obj.horario else None
