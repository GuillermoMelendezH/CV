from django import forms
from django.forms import inlineformset_factory
from .models import Perfil, ExperienciaLaboral, Educacion


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["imagen", "nombre", "ine", "correo", "contacto"]
        widgets = {
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "ine": forms.TextInput(attrs={"class": "form-control"}),
            "correo": forms.EmailInput(attrs={"class": "form-control"}),
            "contacto": forms.TextInput(attrs={"class": "form-control"}),
        }


class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        fields = ["empresa", "puesto", "fecha_ingreso", "fecha_salida"]
        widgets = {
            "empresa": forms.TextInput(attrs={"class": "form-control"}),
            "puesto": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_ingreso": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fecha_salida": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


class EducacionForm(forms.ModelForm):
    class Meta:
        model = Educacion
        fields = ["titulo", "institucion", "fecha_ingreso", "fecha_salida"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "institucion": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_ingreso": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fecha_salida": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


# Formsets con opción de borrar registros
ExperienciaFormSet = inlineformset_factory(
    Perfil,
    ExperienciaLaboral,
    form=ExperienciaLaboralForm,
    extra=3,
    max_num=3,
    can_delete=True
)

EducacionFormSet = inlineformset_factory(
    Perfil,
    Educacion,
    form=EducacionForm,
    extra=3,
    max_num=3,
    can_delete=True
)

