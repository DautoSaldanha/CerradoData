from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from aplicacao_cerrado import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projetos/', views.projetos, name='projetos'),
    path('projetos/<slug:slug>/', views.projeto_detalhe, name='projeto_detalhe'),
    path('gestao/login/', views.gestao_login, name='gestao_login'),
    path('gestao/sair/', views.gestao_logout, name='gestao_logout'),
    path('gestao/', views.gestao_dashboard, name='gestao_dashboard'),
    path('gestao/projetos/novo/', views.gestao_projeto_form, name='gestao_projeto_novo'),
    path('gestao/projetos/<int:pk>/editar/', views.gestao_projeto_form, name='gestao_projeto_editar'),
    path('gestao/projetos/<int:pk>/remover/', views.gestao_projeto_remover, name='gestao_projeto_remover'),
    path('gestao/membros/novo/', views.gestao_membro_form, name='gestao_membro_novo'),
    path('gestao/membros/<int:pk>/editar/', views.gestao_membro_form, name='gestao_membro_editar'),
    path('gestao/membros/<int:pk>/remover/', views.gestao_membro_remover, name='gestao_membro_remover'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
