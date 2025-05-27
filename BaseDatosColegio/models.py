from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


# --------- MÓDULO DE ROLES Y PRIVILEGIOS ---------
class Privilegio(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion


class Rol(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Permiso(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    privilegio = models.ForeignKey(Privilegio, on_delete=models.CASCADE)
    estado = models.BooleanField()

    class Meta:
        unique_together = ('rol', 'privilegio')

    def __str__(self):
        return f"{self.rol} - {self.privilegio}"


# -------------------- MANAGER --------------------
class UsuarioManager(BaseUserManager):
    def create_user(self, ci, password=None, **extra_fields):
        if not ci:
            raise ValueError("El CI es obligatorio")
        user = self.model(ci=ci, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, ci, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(ci, password, **extra_fields)


# ------------ MODULO USUARIO ------------------
class Usuario(AbstractBaseUser, PermissionsMixin):
    ci = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=100, null=False)
    fecha_nacimiento = models.DateField(default=timezone.now)
    sexo = models.CharField(max_length=1, null=False)
    estado = models.BooleanField(default=True)
    telefono = models.CharField(max_length=15,default='12345678')
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'ci'
    REQUIRED_FIELDS = ['nombre', 'fecha_nacimiento', 'sexo', 'rol_id']

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.ci} - {self.nombre}"


# ------------ SUBTIPOS DE USUARIO --------------
class Profesor(models.Model):
    profesor = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    especialidad = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"Profesor: {self.profesor.nombre}"


# ------------ MODULO BITÁCORA ------------------
class Bitacora(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    ip = models.CharField(max_length=15)
    accion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.ci} - {self.accion}"
    

#-------LE PERTENECE A ALUMNO----------
    

class Asistencia(models.Model):
    fecha = models.DateField()
    estado = models.BooleanField()
    alumno = models.ForeignKey('Alumno', on_delete=models.CASCADE)

    def __str__(self):
        return f"Asistencia de {self.alumno} - {self.fecha}"


class Licencia(models.Model):
    descripcion = models.CharField(max_length=50)
    fecha = models.DateField()
    imagen = models.CharField(max_length=200)
    alumno = models.ForeignKey('Alumno', on_delete=models.CASCADE)

    def __str__(self):
        return f"Licencia - {self.descripcion}"


class Participacion(models.Model):
    descripcion = models.CharField(max_length=30)
    fecha = models.DateField()
    alumno = models.ForeignKey('Alumno', on_delete=models.CASCADE)
    curso = models.IntegerField(null=True)
    materia = models.IntegerField(null=True)

    def __str__(self):
        return f"Participación de {self.alumno} - {self.fecha}"


class Dimension(models.Model):
    descripcion = models.CharField(max_length=15)
    puntaje = models.IntegerField()

    def __str__(self):
        return self.descripcion


class Nivel(models.Model):
    nombre = models.CharField(max_length=12)
    estado = models.BooleanField()

    def __str__(self):
        return self.nombre


class Curso(models.Model):
    nombre = models.CharField(max_length=5)
    estado = models.BooleanField()
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Paralelo(models.Model):
    descripcion = models.CharField(max_length=2)
    estado = models.BooleanField()

    def __str__(self):
        return self.descripcion


class CursoParalelo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    paralelo = models.ForeignKey(Paralelo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.curso} {self.paralelo}"
    
class Alumno(models.Model):
    alumno = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    matricula = models.CharField(max_length=20, null=False)


    def __str__(self):
        return f"Alumno: {self.alumno.nombre}"

class AlumnoCursoParalelo(models.Model):
    curso_paralelo = models.ForeignKey(CursoParalelo, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('curso_paralelo', 'alumno')

    def __str__(self):
        return f"{self.alumno} en {self.curso_paralelo}"

    
class Materia(models.Model):
    nombre = models.CharField(max_length=15)
    descripcion = models.CharField(max_length=30, blank=True, null=True)
    estado = models.BooleanField()

    def __str__(self):
        return self.nombre


class Horario(models.Model):
    hora_inicial = models.TimeField()
    hora_final = models.TimeField()
    estado = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.hora_inicial} - {self.hora_final}"


class DescripcionMateria(models.Model):
    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profesor} - {self.materia}"
class HorarioMateria(models.Model):
    curso_paralelo = models.ForeignKey('CursoParalelo', on_delete=models.CASCADE)
    descripcion_materia = models.ForeignKey(DescripcionMateria, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.descripcion_materia} - {self.horario}"


class Actividad(models.Model):
    nombre = models.CharField(max_length=30)
    estado = models.BooleanField()

    def __str__(self):
        return self.nombre


class DetalleDimension(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('actividad', 'dimension')

    def __str__(self):
        return f"{self.actividad} - {self.dimension}"

class TareaAsignada(models.Model):
    descripcion = models.CharField(max_length=150,null=True)
    puntaje = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_entrega = models.DateField()
    estado = models.BooleanField()
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    alumno = models.ForeignKey('Alumno', on_delete=models.CASCADE)
    horario_materia = models.ForeignKey(HorarioMateria, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f"Tarea de {self.alumno} - {self.actividad}"


class Trimestre(models.Model):
    nro = models.PositiveSmallIntegerField()
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    estado = models.BooleanField()

    def __str__(self):
        return f"Trimestre {self.nro}"


class Gestion(models.Model):
    anio_escolar = models.IntegerField()
    estado = models.BooleanField()

    def __str__(self):
        return str(self.anio_escolar)


class DetalleTrimestre(models.Model):
    gestion = models.ForeignKey(Gestion, on_delete=models.CASCADE)
    trimestre = models.ForeignKey(Trimestre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.gestion} - {self.trimestre}"


class Libreta(models.Model):
    descripcion = models.CharField(max_length=50)
    aprobado = models.BooleanField()
    alumno = models.ForeignKey('Alumno', on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    detalle_trimestre = models.ForeignKey(DetalleTrimestre, on_delete=models.CASCADE)

    def __str__(self):
        return f"Libreta de {self.alumno}"


class Mensualidad(models.Model):
    precio = models.IntegerField()
    cantidad = models.IntegerField()
    fecha = models.DateField()
    estado = models.BooleanField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    alumno = models.ForeignKey('Alumno', on_delete=models.CASCADE)

    def __str__(self):
        return f"Mensualidad de {self.alumno}"


class MateriaAsignada(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('curso', 'materia')

    def __str__(self):
        return f"{self.materia} - {self.curso}"


class Notificacion(models.Model):
    titulo = models.CharField(max_length=20)
    mensaje = models.CharField(max_length=500)
    fecha = models.DateField()
    estado = models.BooleanField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.titulo
