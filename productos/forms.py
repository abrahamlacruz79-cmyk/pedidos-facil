from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombre",
            "descripcion",
            "precio",
            "cantidad_disponible",
        ]

        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre del producto",
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Descripción del producto",
                "rows": 4,
            }),
            "precio": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0",
                "step": "0.01",
            }),
            "cantidad_disponible": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0",
                "step": "1",
            }),
        }

    def clean_precio(self):
        precio = self.cleaned_data["precio"]

        if precio < 0:
            raise forms.ValidationError(
                "El precio no puede ser negativo."
            )

        return precio