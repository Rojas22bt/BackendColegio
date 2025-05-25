from rest_framework import serializers
from BaseDatosColegio.models import Trimestre,Gestion ,DetalleTrimestre

class TrimestreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Trimestre
        fields = ['id','nro','fecha_inicio','fecha_final','estado']
        
class GestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Gestion
        fields = ['id','anio_escolar','estado']
    
class DetalleTrimestreSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleTrimestre
        fields = ['id','gestion','trimestre']