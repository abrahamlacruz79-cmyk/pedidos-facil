from django.db import models
from django.contrib.auth.models import User


class Pedido(models.Model):

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]

    numero_pedido = models.CharField(
        max_length=30,
        unique=True
    )
    cliente = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(max_length=500)
    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.numero_pedido