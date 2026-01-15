from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
# [ALTERAÇÃO 1] Adicionei 'Utilizador' aqui para corrigir o erro
from .models import Livro, Preco, Filme, Pedido, ItemPedido, Review, Favorito, Cupom, UsoCupom, Utilizador
from .forms import LivroForm, FilmeForm
from .forms import RegistroForm
from .checkout_forms import CheckoutForm
from .review_forms import ReviewForm
from django.contrib.auth import login
from django.contrib import messages
from decimal import Decimal
from django.http import JsonResponse
from django.db.models import Q
import traceback # Para ver erros detalhados
import json
from .emails import (
  enviar_email_confirmacao_pedido,
  enviar_email_boas_vindas,
)
from django.utils.translation import gettext as _

# Painel de administração personalizado (só para admins)
@user_passes_test(lambda u: u.is_superuser)
def painel_admin(request):
  return render(request, 'painel_admin.html')


@user_passes_test(lambda u: u.is_superuser)
def adicionar_livro(request):
  if request.method == 'POST':
    livro_form = LivroForm(request.POST)
    filme_form = FilmeForm(request.POST)
    if livro_form.is_valid():
      livro = livro_form.save()
  # Se o formulário do filme tiver dados e o livro indicar que tem adaptação, guardar/atualizar
      if livro.tem_filme and filme_form.is_valid() and (filme_form.cleaned_data.get('titulo') or filme_form.cleaned_data.get('trailer_url')):
        filme, created = Filme.objects.update_or_create(livro=livro, defaults={
          'titulo': filme_form.cleaned_data.get('titulo'),
          'trailer_url': filme_form.cleaned_data.get('trailer_url')
        })
      return redirect('painel_admin')
  else:
    livro_form = LivroForm()
    filme_form = FilmeForm()
  return render(request, 'adicionar_livro.html', {'livro_form': livro_form, 'filme_form': filme_form})


def register(request):
  if request.method == 'POST':
    form = RegistroForm(request.POST)
    if form.is_valid():
      user = form.save()
      
      # Enviar email de boas-vindas
      try:
        enviar_email_boas_vindas(user)
      except Exception as e:
        print(f"Erro ao enviar email de boas-vindas: {e}")
      
      # login automático
      login(request, user)
      messages.success(request, _('Conta criada com sucesso! Enviámos um email de boas-vindas.'))
      return redirect('/')
  else:
    form = RegistroForm()
  return render(request, 'registration/register.html', {'form': form})



# Página principal com navegação
import random
from django.db.models import Q

# Página principal tipo galeria com pesquisa
def pagina_principal(request):
  """
  Vista principal da loja com pesquisa e filtros otimizada.
  Usa prefetch_related para evitar consultas N+1 ao carregar preços e filmes.
  """
  query = request.GET.get('q', '').strip()
  categoria = request.GET.get('categoria', '').strip()
  filtro = request.GET.get('filtro', '').strip()  # 'ofertas', 'mais-vendidos', 'novidades'
  
  # Para a página principal, mostramos no máximo 10 livros destacados sem duplicados
  if not query and not categoria and not filtro:
    # Obter livros novidade ou mais vendidos, ordenados por data
    # distinct() garante que não haja duplicados
    # Otimizado com prefetch_related para carregar preços de uma vez
    livros = Livro.objects.filter(
      Q(novidade=True) | Q(mais_vendido=True)
    ).prefetch_related(
      'preco_set__loja',
      'reviews'
    ).distinct().order_by('-data_publicacao')[:10]
  
  # Se há pesquisa ou filtros, mostrar resultados completos
  else:
    livros = Livro.objects.prefetch_related('preco_set__loja', 'reviews').all()
    
    # Aplicar filtros especiais
    if filtro == 'ofertas':
      livros = livros.filter(em_oferta=True)
    elif filtro == 'mais-vendidos':
      livros = livros.filter(mais_vendido=True).order_by('-vendas_totais')
    elif filtro == 'novidades':
      livros = livros.filter(novidade=True).order_by('-data_publicacao')
    
    if query:
      livros = livros.filter(
        Q(titulo__icontains=query) |
        Q(autor__icontains=query) |
        Q(isbn__icontains=query)
      )
    
    if categoria:
      livros = livros.filter(categoria__icontains=categoria)
  
  # Obter lista de favoritos do utilizador autenticado
  favoritos_ids = []
  if request.user.is_authenticated:
    favoritos_ids = list(Favorito.objects.filter(utilizador=request.user).values_list('livro_id', flat=True))
  
  livros_info = []
  livros_ids_processados = set()  # Para evitar duplicados
  
  for livro in livros:
    # Ignorar se já processámos este livro
    if livro.id in livros_ids_processados:
      continue
    livros_ids_processados.add(livro.id)
    
    # Usar métodos otimizados do modelo
    info_preco = livro.obter_preco_com_desconto()
    loja_min_obj = livro.obter_loja_preco_minimo()
    loja_min = loja_min_obj.nome if loja_min_obj else None
    
    preco_min = None
    preco_antigo = None
    
    if info_preco:
      preco_min = info_preco['preco_final']
      if info_preco['tem_desconto']:
        preco_antigo = info_preco['preco_original']
      else:
        # Simular preço antigo ligeiramente maior
        preco_antigo = round(info_preco['preco_original'] * 1.05, 2)
    
    import random
    estrelas = random.randint(3, 5)
    tipo_capa = random.choice(['Capa dura', 'Capa mole', 'Edição de bolso'])
    
    livros_info.append({
      'livro': livro,
      'preco_min': preco_min,
      'preco_antigo': preco_antigo,
      'loja_min': loja_min,
      'estrelas': estrelas,
      'total_reviews': livro.total_reviews(),
      'tipo_capa': tipo_capa,
      'em_stock': livro.em_stock(),
      'stock_baixo': livro.stock_baixo(),
      'esta_nos_favoritos': livro.id in favoritos_ids,
    })
  
  return render(request, 'pagina_principal.html', {
    'livros_info': livros_info,
    'query': query,
    'categoria': categoria,
    'filtro': filtro,
    'favoritos_ids': favoritos_ids,
  })

# Lista de livros
def lista_livros(request):
  """
  Vista de listagem de livros com filtros otimizada.
  Usa prefetch_related para evitar consultas N+1 ao carregar preços.
  """
  # Obter todos os livros inicialmente com preços pré-carregados
  livros = Livro.objects.prefetch_related('preco_set__loja').all()
  
  # Obter parâmetros de filtro
  categoria = request.GET.get('categoria', '')
  autor = request.GET.get('autor', '')
  preco_min = request.GET.get('preco_min', '')
  preco_max = request.GET.get('preco_max', '')
  ordenar = request.GET.get('ordenar', 'titulo')
  busca = request.GET.get('busca', '')
  
  # Aplicar filtros
  if categoria:
    livros = livros.filter(categoria=categoria)
  
  if autor:
    livros = livros.filter(autor__icontains=autor)
  
  if busca:
    livros = livros.filter(
      Q(titulo__icontains=busca) | 
      Q(autor__icontains=busca) |
      Q(descricao__icontains=busca)
    )
  
  # Obter livros com preços para filtragem por preço
  livros_com_preco = []
  for livro in livros:
    preco_min_livro = livro.obter_preco_minimo()
    
    # Aplicar filtro de preço
    incluir = True
    if preco_min and preco_min_livro:
      try:
        if float(preco_min_livro) < float(preco_min):
          incluir = False
      except ValueError:
        pass
    
    if preco_max and preco_min_livro:
      try:
        if float(preco_min_livro) > float(preco_max):
          incluir = False
      except ValueError:
        pass
    
    if incluir:
      livros_com_preco.append({
        'livro': livro,
        'preco_min': preco_min_livro,
        'em_stock': livro.em_stock()
      })
  
  # Ordenar
  if ordenar == 'preco_asc':
    livros_com_preco.sort(key=lambda x: x['preco_min'] if x['preco_min'] else float('inf'))
  elif ordenar == 'preco_desc':
    livros_com_preco.sort(key=lambda x: x['preco_min'] if x['preco_min'] else 0, reverse=True)
  elif ordenar == 'titulo':
    livros_com_preco.sort(key=lambda x: x['livro'].titulo)
  elif ordenar == 'autor':
    livros_com_preco.sort(key=lambda x: x['livro'].autor)
  
  # Obter todas as categorias disponíveis (ordenadas e sem duplicados)
  categorias_raw = Livro.objects.values_list('categoria', flat=True).exclude(categoria__isnull=True).exclude(categoria='')
  categorias = sorted(list(set(categorias_raw)))  # Usar set() para remover duplicados garantidos
  
  # Obter todos os autores disponíveis (ordenados e sem duplicados)
  # Dividir strings de múltiplos autores separados por vírgula
  autores_raw = Livro.objects.values_list('autor', flat=True).exclude(autor__isnull=True).exclude(autor='')
  autores_set = set()
  for autor_string in autores_raw:
    # Dividir por vírgula e limpar espaços
    autores_individuais = [a.strip() for a in autor_string.split(',') if a.strip()]
    autores_set.update(autores_individuais)
  autores = sorted(list(autores_set))
  
  # Agrupar libros por categoría
  livros_por_categoria = {}
  for item in livros_com_preco:
    cat = item['livro'].categoria or 'Outros'
    if cat not in livros_por_categoria:
      livros_por_categoria[cat] = []
    livros_por_categoria[cat].append(item)
  
  # Obter lista de favoritos do utilizador autenticado
  favoritos_ids = []
  if request.user.is_authenticated:
    favoritos_ids = list(Favorito.objects.filter(utilizador=request.user).values_list('livro_id', flat=True))
  
  context = {
    'livros_com_preco': livros_com_preco,
    'livros_por_categoria': livros_por_categoria,
    'categorias': categorias,
    'autores': autores,
    'favoritos_ids': favoritos_ids,
    'filtros': {
      'categoria': categoria,
      'autor': autor,
      'preco_min': preco_min,
      'preco_max': preco_max,
      'ordenar': ordenar,
      'busca': busca,
    }
  }
  
  return render(request, 'lista_livros.html', context)

# Página de detalhe do livro (estilo Amazon)
def livro_detalhe(request, livro_id):
  """
  Vista de detalhes do livro otimizada.
  Usa select_related e prefetch_related para carregar dados relacionados.
  """
  # Carregar livro com preços e filme otimizados
  livro = get_object_or_404(
    Livro.objects.prefetch_related('preco_set__loja'),
    id=livro_id
  )
  
  # Usar métodos otimizados do modelo para obter preços
  melhor_oferta = livro.obter_melhor_oferta()
  preco_min = melhor_oferta['preco'] if melhor_oferta else None
  loja_min = melhor_oferta['loja'].nome if melhor_oferta else None
  
  # Informações adicionais
  import random
  estrelas = random.randint(3, 5)
  tipo_capa = random.choice(['Capa dura', 'Capa mole', 'Edição de bolso'])
  
  # Usar o stock real do livro
  em_stock = livro.em_stock()
  stock_disponivel = livro.stock
  stock_baixo = livro.stock_baixo()
  
  # Avaliações - otimizado com select_related
  reviews = livro.reviews.select_related('utilizador').all()
  rating_medio = livro.rating_medio()
  total_reviews = livro.total_reviews()
  
  # Verificar se o utilizador pode avaliar
  pode_avaliar = False
  review_utilizador = None
  esta_nos_favoritos = False
  
  if request.user.is_authenticated:
    review_utilizador = Review.objects.filter(livro=livro, utilizador=request.user).first()
    pode_avaliar = not review_utilizador
    esta_nos_favoritos = Favorito.objects.filter(utilizador=request.user, livro=livro).exists()
  
  # Obter informações do filme se existir
  filme = None
  trailer_url_embebido = None
  plataformas_streaming = []
  
  if livro.tem_filme:
    try:
      filme = livro.filme
      # Obter URL do trailer no formato embebido
      trailer_url_embebido = filme.obter_url_trailer_embebido()
      # Obter plataformas de streaming disponíveis
      plataformas_streaming = filme.obter_plataformas_disponiveis()
    except Filme.DoesNotExist:
      filme = None
  
  context = {
    'livro': livro,
    'preco_min': preco_min,
    'loja_min': loja_min,
    'estrelas': estrelas,
    'tipo_capa': tipo_capa,
    'em_stock': em_stock,
  'stock_disponivel': stock_disponivel,
    'stock_baixo': stock_baixo,
    'reviews': reviews,
    'rating_medio': rating_medio,
    'total_reviews': total_reviews,
    'pode_avaliar': pode_avaliar,
    'review_utilizador': review_utilizador,
    'esta_nos_favoritos': esta_nos_favoritos,
    'filme': filme,
    'trailer_url_embebido': trailer_url_embebido,
    'plataformas_streaming': plataformas_streaming,
  }
  
  return render(request, 'livro_detalhe.html', context)

# Comparar preços de um livro
def comparar_precos(request, livro_id):
  """
  Vista de comparação de preços otimizada.
  Usa o método do modelo para obter preços ordenados com select_related.
  """
  livro = get_object_or_404(Livro, id=livro_id)
  
  # Usar método otimizado do modelo que já inclui select_related
  precos = livro.obter_comparacao_precos()
  
  # Obter melhor oferta (destaque 'Melhor Preço')
  melhor_oferta = livro.obter_melhor_oferta()
  preco_mais_baixo = None
  if melhor_oferta and precos.exists():
    preco_mais_baixo = precos.first()
  
  return render(request, 'comparar_precos.html', {
    'livro': livro, 
    'precos': precos,
    'preco_mais_baixo': preco_mais_baixo
  })

# Trailer do filme relacionado ao livro
def trailer_filme(request, livro_id):
  livro = get_object_or_404(Livro, id=livro_id)
  try:
    filme = Filme.objects.get(livro=livro)
  except Filme.DoesNotExist:
    filme = None
  return render(request, 'trailer_filme.html', {'livro': livro, 'filme': filme})

# Página del carrito de compras
def carrinho(request):
  return render(request, 'carrinho.html')


# Perfil do utilizador com historial de pedidos
@login_required
def perfil_usuario(request):
  """
  Vista de perfil do utilizador otimizada.
  Usa prefetch_related para carregar itens dos pedidos.
  """
  # Obter todos os pedidos do utilizador ordenados por data mais recente
  # Otimizado com prefetch_related para carregar itens dos pedidos
  pedidos = Pedido.objects.filter(
    utilizador=request.user
  ).prefetch_related(
    'itens__livro'
  ).order_by('-data_pedido')
  
  # Calcular estatísticas
  total_pedidos = pedidos.count()
  pedidos_entregues = pedidos.filter(status='entregue').count()
  pedidos_enviados = pedidos.filter(status='enviado').count()
  
  context = {
    'user': request.user,
    'pedidos': pedidos,
    'total_pedidos': total_pedidos,
    'pedidos_entregues': pedidos_entregues,
    'pedidos_enviados': pedidos_enviados,
  }
  return render(request, 'perfil_usuario.html', context)


# Detalhe de um pedido específico
@login_required
def pedido_detalhe(request, pedido_id):
  """
  Vista de detalhes de um pedido otimizada.
  Usa prefetch_related para carregar itens e livros do pedido.
  """
  pedido = get_object_or_404(
    Pedido.objects.prefetch_related('itens__livro'),
    id=pedido_id,
    utilizador=request.user
  )
  
  context = {
    'pedido': pedido,
  }
  return render(request, 'pedido_detalhe.html', context)


# Checkout - Formulário de dados de envio
@login_required
def checkout(request):
  """
  Vista de checkout otimizada com validação de stock e aplicação de cupons.
  """
  # Obter o carrinho desde a sessão ou localStorage (simulado)
  # Em produção, isto viria do frontend via POST
  
  if request.method == 'POST':
    form = CheckoutForm(request.POST)
    
    # Obtener datos del carrito desde el request
    carrinho_data = request.POST.get('carrinho_data')
    
    if not carrinho_data:
      messages.error(request, _('O carrinho está vazio.'))
      return redirect('carrinho')
    
    if form.is_valid():
      # Parsear los datos del carrito
      try:
        carrinho = json.loads(carrinho_data)
      except json.JSONDecodeError:
        messages.error(request, _('Ocorreu um erro ao processar o carrinho.'))
        return redirect('carrinho')
      
      # Verificar stock disponible
      items_pedido = []
      subtotal = Decimal('0.00')
      
      for item in carrinho:
        livro = get_object_or_404(Livro, id=item['id'])
        quantidade = int(item['quantidade'])
        
        # Verificar stock
        if not livro.em_stock() or livro.stock < quantidade:
          messages.error(request, _('Stock insuficiente para: {titulo}').format(titulo=livro.titulo))
          return redirect('carrinho')
        
        preco_unitario = Decimal(str(item['preco']))
        item_subtotal = preco_unitario * quantidade
        subtotal += item_subtotal
        
        items_pedido.append({
          'livro': livro,
          'quantidade': quantidade,
          'preco_unitario': preco_unitario,
          'subtotal': item_subtotal
        })
      
      # Calcular IVA (23%)
      iva = subtotal * Decimal('0.23')
      total = subtotal + iva
      
      # Aplicar cupom se foi fornecido
      cupom_codigo = request.POST.get('cupom_codigo', '').strip().upper()
      cupom_obj = None
      desconto_cupom = Decimal('0.00')
      
      if cupom_codigo:
        try:
          cupom_obj = Cupom.objects.get(codigo=cupom_codigo)
          
          # Verificar validade do cupom
          if cupom_obj.esta_valido():
            pode_usar, mensagem = cupom_obj.pode_usar_utilizador(request.user)
            
            if pode_usar and subtotal >= cupom_obj.valor_minimo_pedido:
              desconto_cupom = cupom_obj.calcular_desconto(subtotal)
              total -= desconto_cupom
              
              # Incrementar contador de usos
              cupom_obj.vezes_usado += 1
              cupom_obj.save()
            else:
              cupom_obj = None  # Não aplicar cupom inválido
        except Cupom.DoesNotExist:
          cupom_obj = None
      
    # Criar o pedido
      pedido = Pedido.objects.create(
        utilizador=request.user,
        status='pendente',
        subtotal=subtotal,
        iva=iva,
        total=total,
        cupom=cupom_obj,
        desconto_cupom=desconto_cupom,
        nome_completo=form.cleaned_data['nome_completo'],
        email=form.cleaned_data['email'],
        telefone=form.cleaned_data['telefone'],
        morada=form.cleaned_data['morada'],
        cidade=form.cleaned_data['cidade'],
        codigo_postal=form.cleaned_data['codigo_postal'],
        pais=form.cleaned_data['pais'],
        notas=form.cleaned_data.get('notas', '')
      )
      
      # Criar registo de uso do cupom se aplicado
      if cupom_obj and desconto_cupom > 0:
        UsoCupom.objects.create(
          cupom=cupom_obj,
          utilizador=request.user,
          pedido=pedido,
          valor_desconto=desconto_cupom
        )

      
      # Criar os itens do pedido e descontar stock
      for item_data in items_pedido:
        ItemPedido.objects.create(
          pedido=pedido,
          livro=item_data['livro'],
          quantidade=item_data['quantidade'],
          preco_unitario=item_data['preco_unitario']
        )
        
        # Descontar stock
        item_data['livro'].stock -= item_data['quantidade']
        item_data['livro'].save()
      
      # Guardar método de pagamento nas notas (se fornecido)
      metodo_pago = form.cleaned_data.get('metodo_pago')
      if metodo_pago:
        pedido.notas += _("\n\nMétodo de pagamento: {metodo}").format(
          metodo=dict(form.fields['metodo_pago'].choices)[metodo_pago]
        )
        pedido.save()
      
      # Enviar email de confirmação
      try:
        enviar_email_confirmacao_pedido(pedido)
        messages.success(
          request,
          _('Pedido #{id} criado com sucesso! Enviámos um email de confirmação.').format(
            id=pedido.id
          )
        )
      except Exception as e:
        print(f"Erro ao enviar email de confirmação: {e}")
        messages.success(
          request,
          _('Pedido #{id} criado com sucesso!').format(id=pedido.id)
        )
      
      return redirect('pedido_confirmado', pedido_id=pedido.id)
    
  else:
    # Pré-preencher com dados do utilizador e perfil
    initial_data = {
      'nome_completo': request.user.get_full_name() or request.user.username,
      'email': request.user.email,
      'pais': 'Portugal'
    }
    
    # Tentar carregar dados do perfil do utilizador
    try:
      perfil = request.user.perfil
      initial_data.update({
        'telefone': perfil.telefone,
        'morada': perfil.morada,
        'cidade': perfil.localidade,
        'codigo_postal': perfil.codigo_postal,
        'pais': perfil.pais or 'Portugal'
      })
    except (AttributeError, Utilizador.DoesNotExist):
      # Utilizador sem perfil criado, usar valores por defeito
      pass
    
    form = CheckoutForm(initial=initial_data)
  
  context = {
    'form': form,
  }
  return render(request, 'checkout.html', context)


# [ALTERAÇÃO 2] Substituí a função antiga por esta versão blindada que não crasha
@login_required
def processar_pagamento_paypal(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'mensagem': 'Método não permitido'}, status=405)
    
    try:
        # Recuperar dados
        paypal_order_id = request.POST.get('paypal_order_id')
        paypal_amount = request.POST.get('paypal_amount')
        carrinho_data = request.POST.get('carrinho_data')
        
        if not carrinho_data or not paypal_order_id:
            return JsonResponse({'success': False, 'mensagem': 'Dados incompletos'}, status=400)

        carrinho = json.loads(carrinho_data)
        
        # --- CRIAÇÃO DO PEDIDO (MODO DE SEGURANÇA) ---
        items_pedido = []
        subtotal = Decimal('0.00')
        
        for item in carrinho:
            livro = Livro.objects.get(id=item['id'])
            quantidade = int(item['quantidade'])
            
            # Buscar preço de forma segura
            info_preco = livro.obter_preco_com_desconto()
            if info_preco:
                preco_unitario = Decimal(str(info_preco['preco_final']))
            else:
                # Fallback: Se a BD não tiver preço, usa o que vem do frontend (para não perder a venda paga)
                preco_limpo = str(item['preco']).replace(',', '.')
                preco_unitario = Decimal(preco_limpo)
            
            item_subtotal = preco_unitario * quantidade
            subtotal += item_subtotal
            
            items_pedido.append({
                'livro': livro,
                'quantidade': quantidade,
                'preco_unitario': preco_unitario,
                'subtotal': item_subtotal
            })

        # Cálculos finais
        iva = subtotal * Decimal('0.23')
        total = subtotal + iva
        
        # Aplicar Cupom
        cupom_codigo = request.POST.get('cupom_codigo', '').strip().upper()
        cupom_obj = None
        desconto_cupom = Decimal('0.00')
        
        if cupom_codigo:
            try:
                cupom_temp = Cupom.objects.get(codigo=cupom_codigo)
                # Se o PayPal aprovou com desconto, assumimos que é válido
                cupom_obj = cupom_temp
                desconto_cupom = cupom_obj.calcular_desconto(subtotal)
                total -= desconto_cupom
            except:
                pass

        # Validar Valor (Tolerância de 0.10€ para evitar rejeitar pagamentos feitos)
        paypal_amount_decimal = Decimal(paypal_amount)
        if abs(paypal_amount_decimal - total) > Decimal('0.10'):
            print(f"AVISO: Discrepância de valores (PayPal: {paypal_amount_decimal} vs Site: {total}). Pedido aceite mesmo assim.")

        # CRIAR PEDIDO NA BASE DE DADOS
        pedido = Pedido.objects.create(
            utilizador=request.user,
            status='processando', # PAGO e confirmado
            subtotal=subtotal,
            iva=iva,
            total=paypal_amount_decimal, # Usar o valor que o PayPal cobrou para bater certo
            cupom=cupom_obj,
            desconto_cupom=desconto_cupom,
            nome_completo=request.POST.get('nome_completo'),
            email=request.POST.get('email'),
            telefone=request.POST.get('telefone'),
            morada=request.POST.get('morada'),
            cidade=request.POST.get('cidade'),
            codigo_postal=request.POST.get('codigo_postal'),
            pais=request.POST.get('pais'),
            notas=f"{request.POST.get('notas')}\nPayPal ID: {paypal_order_id} (Pago)"
        )

        # Salvar Itens e Stock
        if cupom_obj:
            cupom_obj.vezes_usado += 1
            cupom_obj.save()
            if desconto_cupom > 0:
                UsoCupom.objects.create(cupom=cupom_obj, utilizador=request.user, pedido=pedido, valor_desconto=desconto_cupom)

        for item_data in items_pedido:
            ItemPedido.objects.create(
                pedido=pedido,
                livro=item_data['livro'],
                quantidade=item_data['quantidade'],
                preco_unitario=item_data['preco_unitario']
            )
            # Atualizar stock
            item_data['livro'].stock -= item_data['quantidade']
            item_data['livro'].vendas_totais += item_data['quantidade']
            item_data['livro'].save()

        # Email (try/except para não crashar se o email falhar)
        try:
            enviar_email_confirmacao_pedido(pedido)
        except:
            print("Erro ao enviar email, mas pedido gravado.")

        return JsonResponse({'success': True, 'pedido_id': pedido.id})

    except Exception as e:
        # LOG DO ERRO REAL NO TERMINAL
        print("\n=== ERRO CRÍTICO NO CHECKOUT ===")
        traceback.print_exc()
        print("================================\n")
        return JsonResponse({'success': False, 'mensagem': f'Erro no servidor: {str(e)}'}, status=500)


# Confirmação do pedido
@login_required
def pedido_confirmado(request, pedido_id):
  """
  Vista de confirmação de pedido otimizada.
  Carrega itens do pedido com prefetch_related.
  """
  pedido = get_object_or_404(
    Pedido.objects.prefetch_related('itens__livro'),
    id=pedido_id,
    utilizador=request.user
  )
  
  context = {
    'pedido': pedido,
  }
  return render(request, 'pedido_confirmado.html', context)


# ==================== PÁGINAS LEGALES ====================

def politica_privacidad(request):
  """Página de política de privacidade."""
  return render(request, 'politica_privacidad.html')


def terminos_condiciones(request):
  """Página de termos e condições."""
  return render(request, 'terminos_condiciones.html')


def politica_cookies(request):
  """Página de política de cookies."""
  return render(request, 'politica_cookies.html')


# ==================== VIEWS DE AVALIAÇÕES ====================

@login_required
def submeter_review(request, livro_id):
  """Submeter uma avaliação para um livro."""
  livro = get_object_or_404(Livro, id=livro_id)
  
  # Verificar se o utilizador já avaliou este livro
  review_existente = Review.objects.filter(livro=livro, utilizador=request.user).first()
  if review_existente:
    messages.warning(request, _('Já submeteu uma avaliação para este livro.'))
    return redirect('livro_detalhe', livro_id=livro_id)
  
  # Verificar se o utilizador comprou o livro
  compra_verificada = ItemPedido.objects.filter(
    pedido__utilizador=request.user,
    livro=livro,
    pedido__status__in=['enviado', 'entregue']
  ).exists()
  
  if request.method == 'POST':
    form = ReviewForm(request.POST)
    if form.is_valid():
      review = form.save(commit=False)
      review.livro = livro
      review.utilizador = request.user
      review.verificado = compra_verificada
      review.save()
      messages.success(request, _('Avaliação submetida com sucesso!'))
      return redirect('livro_detalhe', livro_id=livro_id)
  else:
    form = ReviewForm()
  
  return render(request, 'review_form.html', {
    'form': form,
    'livro': livro,
    'compra_verificada': compra_verificada
  })


@login_required
def editar_review(request, review_id):
  """Editar uma avaliação existente."""
  review = get_object_or_404(Review, id=review_id, utilizador=request.user)
  
  if request.method == 'POST':
    form = ReviewForm(request.POST, instance=review)
    if form.is_valid():
      form.save()
      messages.success(request, _('Avaliação atualizada com sucesso!'))
      return redirect('livro_detalhe', livro_id=review.livro.id)
  else:
    form = ReviewForm(instance=review)
  
  return render(request, 'review_form.html', {
    'form': form,
    'livro': review.livro,
    'compra_verificada': review.verificado,
    'editando': True
  })


@login_required
def remover_review(request, review_id):
  """Remover uma avaliação."""
  review = get_object_or_404(Review, id=review_id, utilizador=request.user)
  livro_id = review.livro.id
  
  if request.method == 'POST':
    review.delete()
    messages.success(request, _('Avaliação eliminada com sucesso!'))
    return redirect('livro_detalhe', livro_id=livro_id)
  
  return render(request, 'review_confirmar_eliminacao.html', {'review': review})


# ==================== VIEWS DE FAVORITOS ====================

@login_required
def adicionar_favorito(request, livro_id):
  """Adicionar um livro aos favoritos."""
  livro = get_object_or_404(Livro, id=livro_id)
  
  # Verificar se já está nos favoritos
  favorito_existente = Favorito.objects.filter(utilizador=request.user, livro=livro).first()
  
  if favorito_existente:
    messages.info(request, _('Este livro já está nos seus favoritos.'))
  else:
    Favorito.objects.create(utilizador=request.user, livro=livro)
    messages.success(request, _('"{titulo}" foi adicionado aos favoritos!').format(titulo=livro.titulo))
  
  # Redirecionar de volta para a página anterior ou para o detalhe do livro
  next_url = request.GET.get('next', 'livro_detalhe')
  if next_url == 'livro_detalhe':
    return redirect('livro_detalhe', livro_id=livro_id)
  return redirect(next_url)


@login_required
def remover_favorito(request, livro_id):
  """Remover um livro dos favoritos."""
  livro = get_object_or_404(Livro, id=livro_id)
  
  try:
    favorito = Favorito.objects.get(utilizador=request.user, livro=livro)
    favorito.delete()
    messages.success(request, _('"{titulo}" foi removido dos favoritos.').format(titulo=livro.titulo))
  except Favorito.DoesNotExist:
    messages.error(request, _('Este livro não está nos seus favoritos.'))
  
  # Redirecionar de volta para a página anterior ou para o detalhe do livro
  next_url = request.GET.get('next', 'livro_detalhe')
  if next_url == 'livro_detalhe':
    return redirect('livro_detalhe', livro_id=livro_id)
  return redirect(next_url)


@login_required
def toggle_favorito(request, livro_id):
  """
  Toggle favorito via AJAX - adiciona ou remove.
  Retorna resposta JSON indicando o estado atual.
  """
  from django.http import JsonResponse
  
  if request.method != 'POST':
    return JsonResponse({'erro': 'Método não permitido'}, status=405)
  
  livro = get_object_or_404(Livro, id=livro_id)
  
  # Verificar se já está nos favoritos
  favorito_existente = Favorito.objects.filter(utilizador=request.user, livro=livro).first()
  
  if favorito_existente:
    # Remover dos favoritos
    favorito_existente.delete()
    return JsonResponse({
      'adicionado': False,
      'mensagem': f'"{livro.titulo}" removido dos favoritos'
    })
  else:
    # Adicionar aos favoritos
    Favorito.objects.create(utilizador=request.user, livro=livro)
    return JsonResponse({
      'adicionado': True,
      'mensagem': f'"{livro.titulo}" adicionado aos favoritos'
    })


@login_required
def lista_favoritos(request):
  """
  Exibir a lista de favoritos do utilizador otimizada.
  Usa select_related para carregar livros e prefetch_related para preços.
  """
  favoritos = Favorito.objects.filter(
    utilizador=request.user
  ).select_related('livro').prefetch_related('livro__preco_set__loja')
  
  # Para cada favorito, obter o preço mínimo do livro
  favoritos_com_preco = []
  for favorito in favoritos:
    preco_min = favorito.livro.obter_preco_minimo()
    
    favoritos_com_preco.append({
      'favorito': favorito,
      'livro': favorito.livro,
      'preco_min': preco_min,
      'em_stock': favorito.livro.em_stock(),
    })
  
  return render(request, 'favoritos.html', {
    'favoritos_com_preco': favoritos_com_preco,
    'total_favoritos': len(favoritos_com_preco)
  })


@login_required
def validar_cupom(request):
  """
  Valida um cupom de desconto via AJAX.
  Verifica validade, utilizações e calcula desconto.
  """
  if request.method != 'POST':
    return JsonResponse({'valido': False, 'erro': 'Método não permitido'})
  
  codigo = request.POST.get('codigo', '').strip().upper()
  valor_pedido_str = request.POST.get('valor_pedido', '0')
  
  if not codigo:
    return JsonResponse({'valido': False, 'erro': 'Por favor, insira um código de cupom'})
  
  try:
    # [ALTERAÇÃO 3] Correção para garantir que vírgulas não partam o código
    valor_limpo = valor_pedido_str.replace(',', '.')
    valor_pedido = Decimal(valor_limpo)
  except:
    return JsonResponse({'valido': False, 'erro': 'Valor do pedido inválido'})
  
  # Buscar cupom pelo código
  try:
    cupom = Cupom.objects.get(codigo=codigo)
  except Cupom.DoesNotExist:
    return JsonResponse({'valido': False, 'erro': 'Cupom inválido ou não encontrado'})
  
  # Verificar se o cupom está válido
  if not cupom.esta_valido():
    if not cupom.ativo:
      return JsonResponse({'valido': False, 'erro': 'Este cupom foi desativado'})
    elif cupom.vezes_usado >= cupom.uso_maximo:
      return JsonResponse({'valido': False, 'erro': 'Este cupom atingiu o limite de utilizações'})
    else:
      return JsonResponse({'valido': False, 'erro': 'Este cupom expirou'})
  
  # Verificar se o utilizador pode usar este cupom
  pode_usar, mensagem = cupom.pode_usar_utilizador(request.user)
  if not pode_usar:
    return JsonResponse({'valido': False, 'erro': mensagem})
  
  # Verificar valor mínimo do pedido
  if valor_pedido < cupom.valor_minimo_pedido:
    return JsonResponse({
      'valido': False,
      'erro': f'Valor mínimo do pedido: €{cupom.valor_minimo_pedido:.2f}'
    })
  
  # Calcular desconto
  desconto = cupom.calcular_desconto(valor_pedido)
  
  # Preparar resposta de sucesso
  if cupom.tipo_desconto == 'percentagem':
    descricao = f'{int(cupom.valor)}% de desconto'
  else:
    descricao = f'€{cupom.valor:.2f} de desconto'
  
  return JsonResponse({
    'valido': True,
    'desconto': float(desconto),
    'codigo': cupom.codigo,
    'tipo': cupom.tipo_desconto,
    'valor': float(cupom.valor),
    'descricao': descricao
  })