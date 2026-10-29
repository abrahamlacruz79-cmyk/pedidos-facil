from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Pedido
from .forms import PedidoForm


@login_required  # Requiere que el usuario esté autenticado para acceder
def listar_pedidos(request):
    """
    Vista para listar y buscar pedidos.
    Soporta filtrado básico a través de parámetros de consulta GET.
    """
    # Obtiene el término de búsqueda ingresado en la URL (?buscar=texto)
    busqueda = request.GET.get("buscar", "").strip()

    # Consulta inicial: optimiza la lectura trayendo los datos del usuario relacionado (foreign key)
    # y ordena los registros del más reciente al más antiguo.
    pedidos = Pedido.objects.select_related(
        "usuario"
    ).order_by("-fecha_registro")

    # Si se proporcionó un parámetro de búsqueda, aplica el filtro OR en múltiples campos
    if busqueda:
        pedidos = pedidos.filter(
            Q(numero_pedido__icontains=busqueda)
            | Q(cliente__icontains=busqueda)
            | Q(descripcion__icontains=busqueda)
            | Q(estado__icontains=busqueda)
        )

    # Renderiza la plantilla enviando la lista de pedidos y el texto buscado
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
    """
    Vista para registrar un nuevo pedido en el sistema.
    Asigna automáticamente el usuario logueado como creador del pedido.
    """
    # Procesamiento del formulario cuando el usuario envía los datos (POST)
    if request.method == "POST":
        form = PedidoForm(request.POST)

        if form.is_valid():
            # Crea la instancia en memoria sin guardarla en la base de datos aún
            pedido = form.save(commit=False)
            # Asigna el usuario en sesión activa
            pedido.usuario = request.user
            # Guarda definitivamente en la base de datos
            pedido.save()

            # Notificación de éxito para la interfaz
            messages.success(
                request,
                "Pedido registrado correctamente.",
            )
            return redirect("listar_pedidos")
    else:
        # Carga inicial del formulario vacío para peticiones GET
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
    """
    Vista para actualizar un pedido existente identificado por su Primary Key (pk).
    """
    # Busca el pedido por ID o retorna un error HTTP 404 Not Found si no existe
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == "POST":
        # Pasa los nuevos datos y vincula la instancia existente para actualizarla
        form = PedidoForm(request.POST, instance=pedido)

        if form.is_valid():
            form.save()  # Actualiza el registro en la base de datos
            messages.success(
                request,
                "Pedido actualizado correctamente.",
            )
            return redirect("listar_pedidos")
    else:
        # Carga el formulario precompletado con los datos del pedido actual
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
    """
    Vista para la eliminación de un pedido.
    Implementa confirmación previa antes de eliminar.
    """
    pedido = get_object_or_404(Pedido, pk=pk)

    # Solo elimina cuando el usuario confirma mediante una petición POST
    if request.method == "POST":
        pedido.delete()
        messages.success(
            request,
            "Pedido eliminado correctamente.",
        )
        return redirect("listar_pedidos")

    # Muestra la pantalla de confirmación si la petición es GET
    return render(
        request,
        "pedidos/confirmar_eliminacion.html",
        {"pedido": pedido},
    )
