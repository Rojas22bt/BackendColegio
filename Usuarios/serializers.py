from BaseDatosColegio.models import Usuario,Rol,Privilegio,Permiso
from rest_framework import serializers

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


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # importante para seguridad

    class Meta:
        model = Usuario
        fields = ['id', 'ci', 'nombre', 'fecha_nacimiento', 'sexo', 'estado', 'rol', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

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