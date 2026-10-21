from django import forms
from .models import Pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            "numero_pedido",
            "cliente",
            "descripcion",
            "valor_total",
            "estado",
        ]

        widgets = {
            "numero_pedido": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ejemplo: PED-001",
            }),
            "cliente": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre del cliente",
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Descripción del pedido",
                "rows": 4,
            }),
            "valor_total": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0",
                "step": "0.01",
            }),
            "estado": forms.Select(attrs={
                "class": "form-select",
            }),
        }

    def clean_numero_pedido(self):
        numero = self.cleaned_data["numero_pedido"].strip()

        pedidos = Pedido.objects.filter(numero_pedido=numero)

        if self.instance.pk:
            pedidos = pedidos.exclude(pk=self.instance.pk)

        if pedidos.exists():
            raise forms.ValidationError(
                "Ya existe un pedido con ese número."
            )

        return numero

    def clean_valor_total(self):
        valor = self.cleaned_data["valor_total"]

        if valor < 0:
            raise forms.ValidationError(
                "El valor total no puede ser negativo."
            )

        return valor