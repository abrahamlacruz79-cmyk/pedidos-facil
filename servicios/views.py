from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ServicioCliente
from .forms import ServicioClienteForm


def listar_servicios(request):
    servicios = ServicioCliente.objects.all().order_by('-id')
    return render(request, 'servicios/listar.html', {'servicios': servicios})


def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Servicio registrado con éxito.")
            return redirect('listar_servicios')
    else:
        form = ServicioClienteForm()
    
    return render(request, 'servicios/formulario.html', {
        'form': form,
        'titulo': 'Registrar Servicio'
    })


def editar_servicio(request, pk):
    servicio = get_object_or_404(ServicioCliente, pk=pk)
    if request.method == 'POST':
        form = ServicioClienteForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, "Servicio actualizado correctamente.")
            return redirect('listar_servicios')
    else:
        form = ServicioClienteForm(instance=servicio)

    return render(request, 'servicios/formulario.html', {
        'form': form,
        'titulo': 'Editar Servicio'
    })


def eliminar_servicio(request, pk):
    servicio = get_object_or_404(ServicioCliente, pk=pk)
    if request.method == 'POST':
        servicio.delete()
        messages.success(request, "Servicio eliminado correctamente.")
        return redirect('listar_servicios')
    
    return render(request, 'servicios/confirmar_eliminar.html', {'servicio': servicio})



def descuento_servicio(request, pk):
    servicio = get_object_or_404(ServicioCliente, pk=pk)
    if request.method == 'post':
        descuento = request.POST.get('descuento')
        if descuento:
            try:
                descuento = float(descuento)
                if 0 <= descuento <= 100:
                    servicio.precio -= servicio.precio * (descuento / 100)
                    servicio.save()
                    messages.success(request, f"Descuento del {descuento}% aplicado correctamente.")
                else:
                    messages.error(request, "El descuento debe estar entre 0 y 100.")
            except ValueError:
                messages.error(request, "Por favor, ingrese un valor numérico válido para el descuento.")
        else:
            messages.error(request, "Por favor, ingrese un valor para el descuento.")
