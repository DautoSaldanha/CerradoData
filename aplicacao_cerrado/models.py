from django.db import models
from django.urls import reverse


class Membro(models.Model):
    nome = models.CharField(max_length=120)
    sobrenome = models.CharField(max_length=120, blank=True)
    cargo = models.CharField(max_length=120, blank=True)
    foto = models.ImageField(upload_to="membros/", blank=True)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome", "sobrenome"]
        verbose_name = "Membro"
        verbose_name_plural = "Membros"

    def __str__(self):
        return self.nome_completo

    @property
    def nome_completo(self):
        return " ".join(filter(None, [self.nome, self.sobrenome]))


class Projeto(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    categoria = models.CharField(max_length=100)
    resumo = models.CharField(max_length=300)
    descricao = models.TextField()
    cliente = models.CharField(max_length=160, blank=True)
    ano = models.PositiveIntegerField(blank=True, null=True)
    imagem_capa = models.ImageField(upload_to="projetos/capas/", blank=True)
    url_projeto = models.URLField(blank=True)
    tecnologias = models.TextField(
        blank=True,
        help_text="Separe cada tecnologia por vírgula.",
    )
    publicado = models.BooleanField(default=False)
    destaque = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-destaque", "-criado_em"]
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("projeto_detalhe", kwargs={"slug": self.slug})

    @property
    def lista_tecnologias(self):
        return [tecnologia.strip() for tecnologia in self.tecnologias.split(",") if tecnologia.strip()]


class Participacao(models.Model):
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name="participacoes",
    )
    membro = models.ForeignKey(
        Membro,
        on_delete=models.PROTECT,
        related_name="participacoes",
    )
    funcao = models.CharField(max_length=120)
    descricao = models.TextField(blank=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordem", "membro__nome"]
        constraints = [
            models.UniqueConstraint(
                fields=["projeto", "membro"],
                name="participacao_unica_por_projeto",
            ),
        ]
        verbose_name = "Participação"
        verbose_name_plural = "Participações"

    def __str__(self):
        return f"{self.membro} — {self.projeto}"


class ImagemProjeto(models.Model):
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name="imagens",
    )
    imagem = models.ImageField(upload_to="projetos/galeria/")
    legenda = models.CharField(max_length=200, blank=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordem", "id"]
        verbose_name = "Imagem do projeto"
        verbose_name_plural = "Imagens do projeto"

    def __str__(self):
        return self.legenda or f"Imagem de {self.projeto}"
