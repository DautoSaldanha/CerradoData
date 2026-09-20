from django import forms
from django.forms import inlineformset_factory

from .models import ImagemProjeto, Membro, Participacao, Projeto


class GestaoFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "management-form__input")


class ProjetoForm(GestaoFormMixin, forms.ModelForm):
    class Meta:
        model = Projeto
        fields = [
            "titulo", "slug", "categoria", "resumo", "descricao",
            "cliente", "ano", "imagem_capa", "url_projeto",
            "tecnologias", "publicado", "destaque",
        ]
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 7}),
            "tecnologias": forms.Textarea(attrs={"rows": 3}),
        }


class MembroForm(GestaoFormMixin, forms.ModelForm):
    class Meta:
        model = Membro
        fields = [
            "nome", "sobrenome", "cargo", "foto", "email", "bio",
            "github", "linkedin", "instagram", "ativo",
        ]
        widgets = {"bio": forms.Textarea(attrs={"rows": 5})}


class ParticipacaoForm(GestaoFormMixin, forms.ModelForm):
    class Meta:
        model = Participacao
        fields = ["membro", "funcao", "descricao", "ordem"]
        widgets = {"descricao": forms.Textarea(attrs={"rows": 3})}


class ImagemProjetoForm(GestaoFormMixin, forms.ModelForm):
    class Meta:
        model = ImagemProjeto
        fields = ["imagem", "legenda", "ordem"]


ParticipacaoFormSet = inlineformset_factory(
    Projeto, Participacao, form=ParticipacaoForm, extra=1, can_delete=True
)

ImagemProjetoFormSet = inlineformset_factory(
    Projeto, ImagemProjeto, form=ImagemProjetoForm, extra=1, can_delete=True
)
