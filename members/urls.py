from django.urls import path
from . import views

urlpatterns = [
    path('painel-admin/', views.painel_admin, name='painel_admin'),
    path('painel-admin/adicionar-livro/', views.adicionar_livro, name='adicionar_livro'),
    path('accounts/register/', views.register, name='register'),
    path('', views.pagina_principal, name='pagina_principal'),
    path('livros/', views.lista_livros, name='lista_livros'),
    path('livros/<int:livro_id>/', views.livro_detalhe, name='livro_detalhe'),
    path('livros/<int:livro_id>/comparar/', views.comparar_precos, name='comparar_precos'),
    path('livros/<int:livro_id>/trailer/', views.trailer_filme, name='trailer_filme'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('pedidos/<int:pedido_id>/', views.pedido_detalhe, name='pedido_detalhe'),
    path('checkout/', views.checkout, name='checkout'),
    path('validar-cupom/', views.validar_cupom, name='validar_cupom'),
    path('pedido-confirmado/<int:pedido_id>/', views.pedido_confirmado, name='pedido_confirmado'),
    # Páginas legais
    path('privacidade/', views.politica_privacidad, name='politica_privacidad'),
    path('termos/', views.terminos_condiciones, name='terminos_condiciones'),
    path('cookies/', views.politica_cookies, name='politica_cookies'),
    # Avaliações
    path('livros/<int:livro_id>/avaliar/', views.submeter_review, name='submeter_review'),
    path('reviews/<int:review_id>/editar/', views.editar_review, name='editar_review'),
    path('reviews/<int:review_id>/remover/', views.remover_review, name='remover_review'),
    # Favoritos
    path('favoritos/', views.lista_favoritos, name='lista_favoritos'),
    path('favoritos/toggle/<int:livro_id>/', views.toggle_favorito, name='toggle_favorito'),
    path('livros/<int:livro_id>/favorito/adicionar/', views.adicionar_favorito, name='adicionar_favorito'),
    path('livros/<int:livro_id>/favorito/remover/', views.remover_favorito, name='remover_favorito'),
]