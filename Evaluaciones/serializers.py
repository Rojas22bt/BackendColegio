from BaseDatosColegio.models import Dimension, Asistencia
from rest_framework import serializers

class DimensionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = ['id','descripcion','puntaje']

class AsistenciaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = ['id','fecha','estado','alumno']