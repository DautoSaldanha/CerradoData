from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ImagemProjetoFormSet, MembroForm, ParticipacaoFormSet, ProjetoForm
from .models import Membro, Projeto


def home(request):
    projetos_destaque = Projeto.objects.filter(
        publicado=True, destaque=True
    ).prefetch_related("imagens")
    return render(request, "clientes/home.html", {"projetos": projetos_destaque})


def projetos(request):
    projetos_publicados = Projeto.objects.filter(
        publicado=True
    ).prefetch_related("imagens")
    return render(request, "clientes/projetos.html", {"projetos": projetos_publicados})


def projeto_detalhe(request, slug):
    projeto = get_object_or_404(
        Projeto.objects.filter(publicado=True).prefetch_related(
            "imagens", "participacoes__membro"
        ),
        slug=slug,
    )
    return render(request, "clientes/projeto_detalhe.html", {"projeto": projeto})


def usuario_autorizado(user):
    return user.is_authenticated and user.is_staff


def gestao_required(view_func):
    return login_required(
        user_passes_test(usuario_autorizado, login_url="gestao_login")(view_func)
    )


def gestao_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("gestao_dashboard")

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username", "").strip(),
            password=request.POST.get("password", ""),
        )
        if user is not None and user.is_staff:
            login(request, user)
            return redirect(request.GET.get("next") or "gestao_dashboard")
        messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "gestao/login.html")


def gestao_logout(request):
    logout(request)
    return redirect("gestao_login")


@gestao_required
def gestao_dashboard(request):
    return render(
        request,
        "gestao/dashboard.html",
        {"projetos": Projeto.objects.all(), "membros": Membro.objects.all()},
    )


@gestao_required
def gestao_projeto_form(request, pk=None):
    projeto = get_object_or_404(Projeto, pk=pk) if pk else None
    form = ProjetoForm(request.POST or None, request.FILES or None, instance=projeto)
    participacoes = ParticipacaoFormSet(request.POST or None, instance=projeto)
    imagens = ImagemProjetoFormSet(
        request.POST or None, request.FILES or None, instance=projeto
    )

    if (
        request.method == "POST"
        and form.is_valid()
        and participacoes.is_valid()
        and imagens.is_valid()
    ):
        with transaction.atomic():
            projeto = form.save()
            participacoes.instance = projeto
            imagens.instance = projeto
            participacoes.save()
            imagens.save()
        messages.success(request, "Projeto salvo com sucesso.")
        return redirect("gestao_dashboard")

    return render(
        request,
        "gestao/projeto_form.html",
        {"form": form, "participacoes": participacoes, "imagens": imagens, "projeto": projeto},
    )


@gestao_required
def gestao_projeto_remover(request, pk):
    if request.method == "POST":
        get_object_or_404(Projeto, pk=pk).delete()
        messages.success(request, "Projeto removido com sucesso.")
    return redirect("gestao_dashboard")


@gestao_required
def gestao_membro_form(request, pk=None):
    membro = get_object_or_404(Membro, pk=pk) if pk else None
    form = MembroForm(request.POST or None, request.FILES or None, instance=membro)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Membro salvo com sucesso.")
        return redirect("gestao_dashboard")
    return render(request, "gestao/membro_form.html", {"form": form, "membro": membro})


@gestao_required
def gestao_membro_remover(request, pk):
    if request.method == "POST":
        try:
            get_object_or_404(Membro, pk=pk).delete()
        except ProtectedError:
            messages.error(
                request,
                "Este membro participa de projetos. Remova as participações antes de excluí-lo.",
            )
        else:
            messages.success(request, "Membro removido com sucesso.")
    return redirect("gestao_dashboard")
