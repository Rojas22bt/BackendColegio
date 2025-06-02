from rest_framework.decorators import api_view
from rest_framework.response import Response
from BaseDatosColegio.models import Usuario, Profesor, Alumno, TareaAsignada, Bitacora, CursoParalelo, AlumnoCursoParalelo
from django.db.models import Avg, Count, Q
from datetime import date

@api_view(['GET'])
def dashboard_stats(request):
    try:
        # Conteos básicos
        total_usuarios = Usuario.objects.count()
        total_mujeres = Usuario.objects.filter(sexo='F').count()
        total_hombres = Usuario.objects.filter(sexo='M').count()
        total_profesores = Profesor.objects.count()
        total_alumnos = Alumno.objects.count()

        # Usuarios por rol (agrupado)
        usuarios_por_rol = Usuario.objects.values('rol__nombre').annotate(count=Count('id'))

        # Tareas asignadas
        total_tareas = TareaAsignada.objects.count()
        total_tareas_activas = TareaAsignada.objects.filter(estado=True).count()
        promedio_puntaje_tareas = TareaAsignada.objects.filter(estado=True).aggregate(avg=Avg('puntaje'))['avg'] or 0

        # Promedio tareas por alumno
        tareas_por_alumno = TareaAsignada.objects.values('alumno').annotate(promedio=Avg('puntaje'))
        promedio_general_alumnos = 0
        if tareas_por_alumno:
            promedio_general_alumnos = sum([t['promedio'] for t in tareas_por_alumno]) / len(tareas_por_alumno)

        # Alumnos por curso paralelo
        alumnos_por_cursoparalelo = AlumnoCursoParalelo.objects.values(
            'curso_paralelo__curso__nombre', 'curso_paralelo__paralelo__descripcion'
        ).annotate(count=Count('alumno')).order_by('curso_paralelo__curso__nombre')

        # Alumnos con tareas aprobadas (puntaje >= 60)
        alumnos_tareas_aprobadas = TareaAsignada.objects.filter(puntaje__gte=60).values('alumno').distinct().count()

        # Profesores con y sin especialidad
        profesores_con_esp = Profesor.objects.exclude(especialidad__exact='').count()
        profesores_sin_esp = total_profesores - profesores_con_esp

        # Usuarios activos e inactivos
        usuarios_activos = Usuario.objects.filter(estado=True).count()
        usuarios_inactivos = total_usuarios - usuarios_activos

        # Rango de edad
        hoy = date.today()
        edad_menor_18 = Usuario.objects.filter(fecha_nacimiento__gt=date(hoy.year - 18, hoy.month, hoy.day)).count()
        edad_18_25 = Usuario.objects.filter(fecha_nacimiento__lte=date(hoy.year - 18, hoy.month, hoy.day),
                                             fecha_nacimiento__gt=date(hoy.year - 25, hoy.month, hoy.day)).count()
        edad_mas_25 = total_usuarios - edad_menor_18 - edad_18_25

        # Últimas 5 acciones en bitácora
        ultimas_acciones = Bitacora.objects.order_by('-fecha', '-hora')[:5].values(
            'usuario__nombre', 'fecha', 'hora', 'ip', 'accion'
        )

        data = {
            'total_usuarios': total_usuarios,
            'total_mujeres': total_mujeres,
            'total_hombres': total_hombres,
            'total_profesores': total_profesores,
            'total_alumnos': total_alumnos,
            'usuarios_por_rol': list(usuarios_por_rol),
            'total_tareas': total_tareas,
            'total_tareas_activas': total_tareas_activas,
            'promedio_puntaje_tareas': round(promedio_puntaje_tareas, 2),
            'promedio_general_alumnos': round(promedio_general_alumnos, 2),
            'alumnos_por_cursoparalelo': list(alumnos_por_cursoparalelo),
            'alumnos_tareas_aprobadas': alumnos_tareas_aprobadas,
            'profesores_con_especialidad': profesores_con_esp,
            'profesores_sin_especialidad': profesores_sin_esp,
            'usuarios_activos': usuarios_activos,
            'usuarios_inactivos': usuarios_inactivos,
            'usuarios_por_rango_edad': {
                '<18': edad_menor_18,
                '18-25': edad_18_25,
                '>25': edad_mas_25,
            },
            'ultimas_acciones_bitacora': list(ultimas_acciones),
        }
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
