# recepcion/urls.py
from django.urls import path
from .views import crear_cv

urlpatterns = [
    path('', crear_cv, name='crear_cv'),
    
]