from BaseDatosColegio.models import Dimension, Asistencia,Actividad,DetalleDimension, TareaAsignada
from rest_framework import serializers

class DimensionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = ['id','descripcion','puntaje']

class AsistenciaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = ['id','fecha','estado','alumno']
    
class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ['id','nombre','estado']

class DetalleDimensionSerializers(serializers.ModelSerializer):
    class Meta:
        model = DetalleDimension
        fields = ['actividad','dimension']
    
class TareaAsignadaSerializers(serializers.ModelSerializer):
    class Meta:
        model = TareaAsignada
        field = ['id','descripcion','puntaje','fecha_inicio','fecha_entrega','estado','actividad','alumno','horario_materia']
        