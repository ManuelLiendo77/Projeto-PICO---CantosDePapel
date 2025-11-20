from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Modelo para utilizadores
class Utilizador(models.Model):
  primeiro_nome = models.CharField(max_length=255)
  ultimo_nome = models.CharField(max_length=255)
  telefone = models.CharField(max_length=9, blank=True)
  nif = models.CharField(max_length=9, blank=True)
  pais = models.CharField(max_length=30, blank=True)
  morada = models.CharField(max_length=255, blank=True)
  porta = models.CharField(max_length=4, blank=True)
  andar = models.CharField(max_length=3, blank=True)
  codigo_postal = models.CharField(max_length=10, blank=True)
  localidade = models.CharField(max_length=100, blank=True)
  
  def __str__(self):
    return f"{self.primeiro_nome} {self.ultimo_nome}"
  
  class Meta:
    verbose_name = "Utilizador"
    verbose_name_plural = "Utilizadores"


# Modelo para livros
class Livro(models.Model):
  titulo = models.CharField(max_length=255)
  autor = models.CharField(max_length=255)
  isbn = models.CharField(max_length=13, unique=True)
  descricao = models.TextField(blank=True)
  tem_filme = models.BooleanField(default=False)
  imagem_capa = models.URLField(blank=True, null=True, help_text="URL da imagem da capa do livro")
  categoria = models.CharField(max_length=100, blank=True, default="Livros")
  novidade = models.BooleanField(default=False, help_text="Marcar como novidade")
  stock = models.IntegerField(default=0, help_text="Quantidade disponível em stock")
  stock_minimo = models.IntegerField(default=5, help_text="Alerta quando stock está baixo")
  
  # Novos campos para ofertas e mais vendidos
  em_oferta = models.BooleanField(default=False, help_text="Livro em oferta/promoção")
  desconto_percentagem = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Percentagem de desconto (0-100)")
  mais_vendido = models.BooleanField(default=False, help_text="Marcar como mais vendido")
  vendas_totais = models.IntegerField(default=0, help_text="Total de vendas do livro")
  data_publicacao = models.DateField(blank=True, null=True, help_text="Data de publicação do livro")
  
  def __str__(self):
    return f"{self.titulo} - {self.autor}"
  
  def em_stock(self):
    return self.stock > 0
  
  def stock_baixo(self):
    return self.stock <= self.stock_minimo and self.stock > 0
  
  def rating_medio(self):
    """Calcula a média das avaliações do livro"""
    reviews = self.reviews.all()
    if reviews.exists():
      return round(sum(r.rating for r in reviews) / reviews.count(), 1)
    return 0
  
  def total_reviews(self):
    """Retorna o número total de avaliações"""
    return self.reviews.count()
  
  class Meta:
    verbose_name = "Livro"
    verbose_name_plural = "Livros"
    ordering = ['titulo']


# Modelo para lojas
class Loja(models.Model):
  nome = models.CharField(max_length=255)
  url = models.URLField()
  
  def __str__(self):
    return self.nome
  
  class Meta:
    verbose_name = "Loja"
    verbose_name_plural = "Lojas"


# Modelo para preços de livros em lojas
class Preco(models.Model):
  livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
  loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
  preco = models.DecimalField(max_digits=8, decimal_places=2)
  url_produto = models.URLField()
  
  def __str__(self):
    return f"{self.livro.titulo} - {self.loja.nome}: {self.preco}€"
  
  class Meta:
    verbose_name = "Preço"
    verbose_name_plural = "Preços"


# Modelo para filmes relacionados a livros
class Filme(models.Model):
  livro = models.OneToOneField(Livro, on_delete=models.CASCADE)
  titulo = models.CharField(max_length=255)
  trailer_url = models.URLField(blank=True)
  
  def __str__(self):
    return f"Filme: {self.titulo}"
  
  class Meta:
    verbose_name = "Filme"
    verbose_name_plural = "Filmes"


# Modelo para pedidos
class Pedido(models.Model):
  STATUS_CHOICES = [
    ('pendente', 'Pendente'),
    ('processando', 'Processando'),
    ('enviado', 'Enviado'),
    ('entregue', 'Entregue'),
    ('cancelado', 'Cancelado'),
  ]
  
  utilizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
  data_pedido = models.DateTimeField(default=timezone.now)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
  total = models.DecimalField(max_digits=10, decimal_places=2)
  subtotal = models.DecimalField(max_digits=10, decimal_places=2)
  iva = models.DecimalField(max_digits=10, decimal_places=2)
  
  # Cupom de desconto
  cupom = models.ForeignKey('Cupom', on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos')
  desconto_cupom = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Valor do desconto aplicado")
  
  # Dados de entrega
  nome_completo = models.CharField(max_length=255)
  email = models.EmailField()
  telefone = models.CharField(max_length=20)
  morada = models.CharField(max_length=255)
  cidade = models.CharField(max_length=100)
  codigo_postal = models.CharField(max_length=10)
  pais = models.CharField(max_length=50, default='Portugal')
  
  # Informações adicionais
  notas = models.TextField(blank=True)
  numero_rastreio = models.CharField(max_length=100, blank=True)
  
  def __str__(self):
    return f"Pedido #{self.id} - {self.utilizador.username} - {self.status}"
  
  class Meta:
    verbose_name = "Pedido"
    verbose_name_plural = "Pedidos"
    ordering = ['-data_pedido']


# Modelo para itens do pedido
class ItemPedido(models.Model):
  pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
  livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
  quantidade = models.IntegerField(default=1)
  preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)
  subtotal = models.DecimalField(max_digits=10, decimal_places=2)
  
  def __str__(self):
    return f"{self.quantidade}x {self.livro.titulo}"
  
  def save(self, *args, **kwargs):
    self.subtotal = self.quantidade * self.preco_unitario
    super().save(*args, **kwargs)
  
  class Meta:
    verbose_name = "Item do Pedido"
    verbose_name_plural = "Itens do Pedido"


# Modelo para avaliações de livros
class Review(models.Model):
  RATING_CHOICES = [
    (1, '1 - Muito mau'),
    (2, '2 - Mau'),
    (3, '3 - Médio'),
    (4, '4 - Bom'),
    (5, '5 - Excelente'),
  ]
  
  livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='reviews')
  utilizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
  rating = models.IntegerField(choices=RATING_CHOICES)
  titulo = models.CharField(max_length=200)
  comentario = models.TextField()
  data_criacao = models.DateTimeField(auto_now_add=True)
  verificado = models.BooleanField(default=False, help_text="Compra verificada")
  
  def __str__(self):
    return f"{self.utilizador.username} - {self.livro.titulo} ({self.rating}★)"
  
  class Meta:
    verbose_name = "Avaliação"
    verbose_name_plural = "Avaliações"
    ordering = ['-data_criacao']
    unique_together = ['livro', 'utilizador']  # Um utilizador só pode avaliar um livro uma vez


# Modelo para favoritos/wishlist
class Favorito(models.Model):
  utilizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
  livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='favoritos')
  data_adicao = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.utilizador.username} - {self.livro.titulo}"
  
  class Meta:
    verbose_name = "Favorito"
    verbose_name_plural = "Favoritos"
    ordering = ['-data_adicao']
    unique_together = ['utilizador', 'livro']  # Um utilizador não pode adicionar o mesmo livro duas vezes


# Modelo para cupons de desconto
class Cupom(models.Model):
  TIPO_DESCONTO = (
    ('percentagem', 'Percentagem'),
    ('valor_fixo', 'Valor Fixo'),
  )
  
  codigo = models.CharField(max_length=50, unique=True, help_text="Código do cupom (ex: VERAO2025)")
  descricao = models.TextField(blank=True, help_text="Descrição do cupom")
  tipo_desconto = models.CharField(max_length=15, choices=TIPO_DESCONTO, default='percentagem')
  valor = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor do desconto (% ou €)")
  
  # Validez
  data_inicio = models.DateTimeField(help_text="Data de início da validade")
  data_fim = models.DateTimeField(help_text="Data de fim da validade")
  
  # Limites
  ativo = models.BooleanField(default=True, help_text="Cupom ativo")
  uso_maximo = models.IntegerField(default=100, help_text="Número máximo de usos do cupom")
  uso_por_utilizador = models.IntegerField(default=1, help_text="Usos permitidos por utilizador")
  valor_minimo_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Valor mínimo do pedido para usar o cupom")
  
  # Controle
  vezes_usado = models.IntegerField(default=0, help_text="Número de vezes que o cupom foi usado")
  data_criacao = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.codigo} - {self.get_tipo_desconto_display()}"
  
  def esta_valido(self):
    """Verifica se o cupom está válido"""
    agora = timezone.now()
    return (
      self.ativo and
      self.data_inicio <= agora <= self.data_fim and
      self.vezes_usado < self.uso_maximo
    )
  
  def calcular_desconto(self, valor_pedido):
    """Calcula o valor do desconto para um pedido"""
    if not self.esta_valido():
      return 0
    
    if valor_pedido < self.valor_minimo_pedido:
      return 0
    
    if self.tipo_desconto == 'percentagem':
      desconto = (valor_pedido * self.valor) / 100
    else:  # valor_fixo
      desconto = self.valor
    
    # O desconto não pode ser maior que o valor do pedido
    return min(desconto, valor_pedido)
  
  def pode_usar_utilizador(self, utilizador):
    """Verifica se um utilizador pode usar este cupom"""
    if not self.esta_valido():
      return False, "Cupom inválido ou expirado"
    
    # Verificar quantas vezes o utilizador já usou este cupom
    usos_utilizador = UsoCupom.objects.filter(cupom=self, utilizador=utilizador).count()
    
    if usos_utilizador >= self.uso_por_utilizador:
      return False, f"Você já usou este cupom {self.uso_por_utilizador} vez(es)"
    
    return True, "Cupom válido"
  
  class Meta:
    verbose_name = "Cupom"
    verbose_name_plural = "Cupons"
    ordering = ['-data_criacao']


# Modelo para rastrear uso de cupons por utilizador
class UsoCupom(models.Model):
  cupom = models.ForeignKey(Cupom, on_delete=models.CASCADE, related_name='usos')
  utilizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cupons_usados')
  pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True, blank=True)
  data_uso = models.DateTimeField(auto_now_add=True)
  valor_desconto = models.DecimalField(max_digits=10, decimal_places=2)
  
  def __str__(self):
    return f"{self.utilizador.username} - {self.cupom.codigo} ({self.data_uso.strftime('%d/%m/%Y')})"
  
  class Meta:
    verbose_name = "Uso de Cupom"
    verbose_name_plural = "Usos de Cupons"
    ordering = ['-data_uso']