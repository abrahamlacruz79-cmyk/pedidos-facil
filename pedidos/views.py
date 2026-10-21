from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Pedido
from .forms import PedidoForm


@login_required
def listar_pedidos(request):
    busqueda = request.GET.get("buscar", "").strip()

    pedidos = Pedido.objects.select_related(
        "usuario"
    ).order_by("-fecha_registro")

    if busqueda:
        pedidos = pedidos.filter(
            Q(numero_pedido__icontains=busqueda)
            | Q(cliente__icontains=busqueda)
            | Q(descripcion__icontains=busqueda)
            | Q(estado__icontains=busqueda)
        )

    return render(
        request,
        "pedidos/lista.html",
        {
            "pedidos": pedidos,
            "busqueda": busqueda,
        },
    )


@login_required
def crear_pedido(request):
    if request.method == "POST":
        form = PedidoForm(request.POST)

        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            pedido.save()

            messages.success(
                request,
                "Pedido registrado correctamente.",
            )
            return redirect("listar_pedidos")
    else:
        form = PedidoForm()

    return render(
        request,
        "pedidos/formulario.html",
        {
            "form": form,
            "titulo": "Registrar pedido",
        },
    )


@login_required
def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == "POST":
        form = PedidoForm(request.POST, instance=pedido)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Pedido actualizado correctamente.",
            )
            return redirect("listar_pedidos")
    else:
        form = PedidoForm(instance=pedido)

    return render(
        request,
        "pedidos/formulario.html",
        {
            "form": form,
            "titulo": "Editar pedido",
        },
    )


@login_required
def eliminar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == "POST":
        pedido.delete()
        messages.success(
            request,
            "Pedido eliminado correctamente.",
        )
        return redirect("listar_pedidos")

    return render(
        request,
        "pedidos/confirmar_eliminacion.html",
        {"pedido": pedido},
    )
