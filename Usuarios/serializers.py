from BaseDatosColegio.models import Usuario,Rol,Privilegio,Permiso,Alumno,Profesor,Bitacora
from rest_framework import serializers

#BITACORA
class BitacoraSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bitacora
        fields = [ 'id','usuario','fecha','hora','ip','accion']

#PARA LO QUE TENGA QUE VER CON PERMISOS

class PrivilegioSerializers(serializers.ModelSerializer):
    class Meta:
        model = Privilegio
        fields = ['id','descripcion']

class RolSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id','nombre']

class PermisoDetalleSerializer(serializers.ModelSerializer):
    rol = RolSerializers(read_only=True)
    privilegio = PrivilegioSerializers(read_only=True)

    class Meta:
        model = Permiso
        fields = ['id', 'rol', 'privilegio', 'estado']

#PARA LO QUE TENGA QUE VER CON USUARIO
class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ['alumno','matricula','curso_paralelo']
        
class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ['profesor','especialidad']

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    alumno = serializers.SerializerMethodField()
    profesor = serializers.SerializerMethodField()
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'ci', 'nombre', 'fecha_nacimiento', 'sexo','telefono',
            'estado', 'rol', 'rol_nombre', 'password', 'alumno', 'profesor'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_alumno(self, obj):
        try:
            alumno = Alumno.objects.get(alumno=obj)
            return AlumnoSerializer(alumno).data
        except Alumno.DoesNotExist:
            return None

    def get_profesor(self, obj):
        try:
            profesor = Profesor.objects.get(profesor=obj)
            return ProfesorSerializer(profesor).data
        except Profesor.DoesNotExist:
            return None

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        usuario = Usuario(**validated_data)
        if password:
            usuario.set_password(password)
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance