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
    trimestre_nro = serializers.SerializerMethodField()
    trimestre_info = TrimestreSerializers(source='trimestre', read_only=True)

    class Meta:
        model = DetalleTrimestre
        fields = ['id', 'gestion', 'trimestre', 'trimestre_nro', 'trimestre_info']

    def get_trimestre_nro(self, obj):
        return obj.trimestre.nro if obj.trimestre else None


    
class ParticipacionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Participacion
        fields =['id','descripcion','fecha','alumno','curso','materia']
        
class NotificacionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id','titulo','mensaje','fecha','estado','usuario']
    
class LicenciaSerializers(serializers.ModelSerializer):
    nombre_usuario = serializers.SerializerMethodField()
    ci_usuario = serializers.SerializerMethodField()

    class Meta:
        model = Licencia
        fields = ['id', 'descripcion', 'fecha', 'imagen', 'alumno', 'nombre_usuario', 'ci_usuario']
        
    def get_nombre_usuario(self, obj):
        try:
            return obj.alumno.alumno.nombre
        except AttributeError:
            return None

    def get_ci_usuario(self, obj):
        try:
            return obj.alumno.alumno.ci
        except AttributeError:
            return None


    
    