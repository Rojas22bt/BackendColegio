from rest_framework import serializers
from BaseDatosColegio.models import Trimestre,Gestion ,DetalleTrimestre,Participacion,Notificacion,Licencia

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
    
class ParticipacionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Participacion
        fields =['id','descripcion','fecha','alumno','curso','materia']
        
class NotificacionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id','titulo','mensaje','fecha','estado','usuario']
    
class LicenciaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Licencia
        fields = ['id','descripcion','fecha','imagen','alumno']