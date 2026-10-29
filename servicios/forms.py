from django import forms
from .models import ServicioCliente

class ServicioClienteForm(forms.ModelForm):
    class Meta:
        model = ServicioCliente
        fields = ['nombre_servicio', 'cliente', 'precio', 'descuento']
        widgets = {
            'nombre_servicio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Mantenimiento Web'}),
            'cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan Pérez'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
        }