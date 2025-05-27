from BaseDatosColegio.models import Dimension, Asistencia,Actividad,DetalleDimension
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