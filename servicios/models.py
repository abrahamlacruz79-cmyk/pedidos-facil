from django.db import models

class ServicioCliente(models.Model):
    nombre_servicio = models.CharField(max_length=150, verbose_name="Nombre del servicio")
    cliente = models.CharField(max_length=150, verbose_name="Cliente")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Descuento")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_servicio} - {self.cliente}"
