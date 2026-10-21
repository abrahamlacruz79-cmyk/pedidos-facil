from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Producto
from .forms import ProductoForm


@login_required
def listar_productos(request):
    busqueda = request.GET.get("buscar", "").strip()

    productos = Producto.objects.all().order_by("-fecha_registro")

    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda)
            | Q(descripcion__icontains=busqueda)
        )

    return render(
        request,
        "productos/lista.html",
        {
            "productos": productos,
            "busqueda": busqueda,
        },
    )


@login_required
def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Producto registrado correctamente.",
            )
            return redirect("listar_productos")
    else:
        form = ProductoForm()

    return render(
        request,
        "productos/formulario.html",
        {
            "form": form,
            "titulo": "Registrar producto",
        },
    )


@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Producto actualizado correctamente.",
            )
            return redirect("listar_productos")
    else:
        form = ProductoForm(instance=producto)

    return render(
        request,
        "productos/formulario.html",
        {
            "form": form,
            "titulo": "Editar producto",
        },
    )


@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        producto.delete()
        messages.success(
            request,
            "Producto eliminado correctamente.",
        )
        return redirect("listar_productos")

    return render(
        request,
        "productos/confirmar_eliminacion.html",
        {"producto": producto},
    )
