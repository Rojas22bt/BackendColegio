from django.urls import path
from .controllers.controllers_academia import obtener_cursos

urlpatterns = [
    path('obtener-cursos/',obtener_cursos)
]
