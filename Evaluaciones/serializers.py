from BaseDatosColegio.models import Dimension
from rest_framework import serializers

class DimensionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = ['id','descripcion','puntaje']
