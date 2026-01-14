from django.contrib import admin
from django.utils.html import format_html
from .models import Utilizador, Livro, Loja, Preco, Filme, Pedido, ItemPedido, Review, Favorito, Cupom, UsoCupom
from .emails import enviar_email_pedido_enviado


# ==================== ADMINISTRACIÓN DE USUARIOS ====================
@admin.register(Utilizador)
class UtilizadorAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'telefone', 'nif', 'pais', 'localidade', 'codigo_postal')
    list_filter = ('pais', 'localidade')
    search_fields = ('primeiro_nome', 'ultimo_nome', 'telefone', 'nif', 'morada')
    fieldsets = (
        ('Informação Pessoal', {
            'fields': ('primeiro_nome', 'ultimo_nome', 'telefone', 'nif')
        }),
        ('Morada', {
            'fields': ('pais', 'morada', 'porta', 'andar', 'codigo_postal', 'localidade')
        }),
    )
    
    def nome_completo(self, obj):
        return f"{obj.primeiro_nome} {obj.ultimo_nome}"
    nome_completo.short_description = 'Nome Completo'


# ==================== ADMINISTRACIÓN DE PREÇOS (Inline) ====================
class PrecoInline(admin.TabularInline):
    model = Preco
    extra = 1
    fields = ('loja', 'preco', 'url_produto')


# ==================== ADMINISTRACIÓN DE FILMES (Inline) ====================
class FilmeInline(admin.StackedInline):
    model = Filme
    extra = 0
    fields = (
        'titulo', 
        'trailer_url',
        ('url_netflix', 'url_prime_video'),
    )
    can_delete = True
    verbose_name = "Adaptação Cinematográfica"
    verbose_name_plural = "Adaptações Cinematográficas"
    
    help_texts = {
        'trailer_url': 'URL do YouTube ou Vimeo (será convertida automaticamente para formato embebido)',
        'url_netflix': 'Link direto para o filme na Netflix (opcional)',
        'url_prime_video': 'Link direto para o filme no Prime Video (opcional)',
    }


# ==================== ADMINISTRACIÓN DE LIVROS ====================
@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'isbn', 'categoria', 'ver_capa', 'stock_status', 'novidade', 'oferta_badge', 'vendido_badge', 'tem_filme_badge', 'num_precos')
    list_filter = ('categoria', 'novidade', 'tem_filme', 'em_oferta', 'mais_vendido')
    search_fields = ('titulo', 'autor', 'isbn')
    list_editable = ('novidade',)
    ordering = ('-mais_vendido', '-em_oferta', '-novidade', 'titulo')
    
    fieldsets = (
        ('Informação Básica', {
            'fields': ('titulo', 'autor', 'isbn', 'categoria', 'data_publicacao')
        }),
        ('Detalhes', {
            'fields': ('descricao', 'imagem_capa')
        }),
        ('Stock e Inventário', {
            'fields': ('stock', 'stock_minimo'),
            'classes': ('collapse',)
        }),
        ('Ofertas e Promoções 🎁', {
            'fields': ('em_oferta', 'desconto_percentagem'),
            'classes': ('collapse',),
            'description': 'Configure as ofertas e descontos para este livro'
        }),
        ('Vendas e Popularidade ⭐', {
            'fields': ('mais_vendido', 'vendas_totais'),
            'classes': ('collapse',),
            'description': 'Informações sobre vendas e popularidade'
        }),
        ('Características', {
            'fields': ('novidade', 'tem_filme'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [PrecoInline, FilmeInline]
    
    def ver_capa(self, obj):
        if obj.imagem_capa:
            return format_html('<img src="{}" style="width: 50px; height: 70px; object-fit: cover; border-radius: 4px;" />', obj.imagem_capa)
        return format_html('<span style="color: #999;">📚 Sem capa</span>')
    ver_capa.short_description = 'Capa'
    
    def stock_status(self, obj):
        if obj.stock == 0:
            return format_html('<span style="background: #f44336; color: white; padding: 3px 10px; border-radius: 10px; font-size: 11px; font-weight: bold;">❌ SEM STOCK</span>')
        elif obj.stock_baixo():
            return format_html('<span style="background: #ff9800; color: white; padding: 3px 10px; border-radius: 10px; font-size: 11px; font-weight: bold;">⚠️ {} unid.</span>', obj.stock)
        else:
            return format_html('<span style="background: #4caf50; color: white; padding: 3px 10px; border-radius: 10px; font-size: 11px; font-weight: bold;">✅ {} unid.</span>', obj.stock)
    stock_status.short_description = 'Stock'
    
    def tem_filme_badge(self, obj):
        if obj.tem_filme:
            try:
                filme = Filme.objects.get(livro=obj)
                return format_html('<span style="background: #4caf50; color: white; padding: 3px 10px; border-radius: 10px; font-size: 11px; font-weight: bold;">🎬 SIM</span>')
            except Filme.DoesNotExist:
                return format_html('<span style="background: #ff9800; color: white; padding: 3px 10px; border-radius: 10px; font-size: 11px; font-weight: bold;">⚠️ Falta info</span>')
        return format_html('<span style="color: #999;">-</span>')
    tem_filme_badge.short_description = 'Tem Filme'
    
    def num_precos(self, obj):
        count = Preco.objects.filter(livro=obj).count()
        if count > 0:
            return format_html('<span style="background: #d2691e; color: white; padding: 3px 10px; border-radius: 10px; font-size: 11px; font-weight: bold;">💰 {} loja(s)</span>', count)
        return format_html('<span style="background: #f44336; color: white; padding: 3px 10px; border-radius: 10px; font-size: 11px; font-weight: bold;">⚠️ Sem preço</span>')
    num_precos.short_description = 'Preços'
    
    def oferta_badge(self, obj):
        if obj.em_oferta:
            return format_html('<span style="background: #ff4757; color: white; padding: 3px 10px; border-radius: 10px; font-size: 11px; font-weight: bold;">🎁 -{:.0f}%</span>', obj.desconto_percentagem)
        return format_html('<span style="color: #999;">-</span>')
    oferta_badge.short_description = 'Oferta'
    
    def vendido_badge(self, obj):
        if obj.mais_vendido:
            return format_html('<span style="background: #ffa502; color: white; padding: 3px 10px; border-radius: 10px; font-size: 11px; font-weight: bold;">⭐ {} vendas</span>', obj.vendas_totais)
        return format_html('<span style="color: #999;">-</span>')
    vendido_badge.short_description = 'Mais Vendido'
    
    actions = ['marcar_novidade', 'desmarcar_novidade', 'adicionar_filme', 'colocar_oferta', 'remover_oferta', 'marcar_mais_vendido']
    
    def marcar_novidade(self, request, queryset):
        updated = queryset.update(novidade=True)
        self.message_user(request, f'{updated} livro(s) marcado(s) como novidade.')
    marcar_novidade.short_description = '✨ Marcar como novidade'
    
    def desmarcar_novidade(self, request, queryset):
        updated = queryset.update(novidade=False)
        self.message_user(request, f'{updated} livro(s) desmarcado(s) como novidade.')
    desmarcar_novidade.short_description = '❌ Remover novidade'
    
    def colocar_oferta(self, request, queryset):
        import random
        for livro in queryset:
            livro.em_oferta = True
            livro.desconto_percentagem = random.choice([10, 15, 20, 25, 30])
            livro.save()
        self.message_user(request, f'{queryset.count()} livro(s) colocado(s) em oferta.')
    colocar_oferta.short_description = '🎁 Colocar em oferta'
    
    def remover_oferta(self, request, queryset):
        updated = queryset.update(em_oferta=False, desconto_percentagem=0)
        self.message_user(request, f'{updated} livro(s) removido(s) de oferta.')
    remover_oferta.short_description = '❌ Remover oferta'
    
    def marcar_mais_vendido(self, request, queryset):
        import random
        for livro in queryset:
            livro.mais_vendido = True
            livro.vendas_totais = random.randint(50, 500)
            livro.save()
        self.message_user(request, f'{queryset.count()} livro(s) marcado(s) como mais vendido.')
    marcar_mais_vendido.short_description = '⭐ Marcar como mais vendido'
    
    def adicionar_filme(self, request, queryset):
        updated = queryset.update(tem_filme=True)
        self.message_user(request, f'{updated} livro(s) marcado(s) como tendo filme.')
    adicionar_filme.short_description = '🎬 Marcar como tendo filme'


# ==================== ADMINISTRACIÓN DE LOJAS ====================
@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'url_link', 'num_livros', 'preco_medio')
    search_fields = ('nome',)
    
    def url_link(self, obj):
        return format_html('<a href="{}" target="_blank" style="color: #d2691e; font-weight: bold;">🔗 Visitar loja</a>', obj.url)
    url_link.short_description = 'URL'
    
    def num_livros(self, obj):
        count = Preco.objects.filter(loja=obj).count()
        return format_html('<span style="background: #2196f3; color: white; padding: 3px 10px; border-radius: 10px; font-size: 11px; font-weight: bold;">📚 {} livro(s)</span>', count)
    num_livros.short_description = 'Livros Disponíveis'
    
    def preco_medio(self, obj):
        precos = Preco.objects.filter(loja=obj)
        if precos.exists():
            media = sum(p.preco for p in precos) / precos.count()
            return format_html('<span style="color: #4caf50; font-weight: bold;">💰 {}€</span>', f'{media:.2f}')
        return format_html('<span style="color: #999;">-</span>')
    preco_medio.short_description = 'Preço Médio'


# ==================== ADMINISTRACIÓN DE PREÇOS ====================
@admin.register(Preco)
class PrecoAdmin(admin.ModelAdmin):
    list_display = ('livro_titulo', 'loja_nome', 'preco_formatado', 'ver_produto')
    list_filter = ('loja', 'livro')
    search_fields = ('livro__titulo', 'loja__nome')
    list_select_related = ('livro', 'loja')
    
    fieldsets = (
        ('Informação do Preço', {
            'fields': ('livro', 'loja', 'preco', 'url_produto')
        }),
    )
    
    def livro_titulo(self, obj):
        return obj.livro.titulo
    livro_titulo.short_description = 'Livro'
    
    def loja_nome(self, obj):
        return obj.loja.nome
    loja_nome.short_description = 'Loja'
    
    def preco_formatado(self, obj):
        return format_html('<span style="background: #4caf50; color: white; padding: 5px 12px; border-radius: 8px; font-size: 13px; font-weight: bold;">{}€</span>', f'{obj.preco:.2f}')
    preco_formatado.short_description = 'Preço'
    
    def ver_produto(self, obj):
        return format_html('<a href="{}" target="_blank" style="color: #d2691e; font-weight: bold;">🔗 Ver na loja</a>', obj.url_produto)
    ver_produto.short_description = 'Link'


# ==================== ADMINISTRACIÓN DE FILMES ====================
@admin.register(Filme)
class FilmeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'livro_relacionado', 'ver_trailer')
    search_fields = ('titulo', 'livro__titulo')
    list_select_related = ('livro',)
    
    def livro_relacionado(self, obj):
        return format_html('<span style="color: #d2691e; font-weight: bold;">📚 {}</span>', obj.livro.titulo)
    livro_relacionado.short_description = 'Livro'
    
    def ver_trailer(self, obj):
        if obj.trailer_url:
            return format_html('<a href="{}" target="_blank" style="background: #ff4444; color: white; padding: 3px 10px; border-radius: 10px; font-size: 11px; font-weight: bold; text-decoration: none;">▶️ Ver Trailer</a>', obj.trailer_url)
        return format_html('<span style="color: #999;">Sem trailer</span>')
    ver_trailer.short_description = 'Trailer'


# Personalizar o título do admin
admin.site.site_header = '📚 Cantos de Papel - Administração'
admin.site.site_title = 'Admin Livraria'
admin.site.index_title = '🎛️ Painel de Gestão'
admin.site.site_url = '/'  # Link para a página principal


# ==================== ADMINISTRAÇÃO DE PEDIDOS ====================
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('livro', 'quantidade', 'preco_unitario', 'subtotal')
    can_delete = False


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilizador_nome', 'data_pedido', 'status_badge', 'total_formatado', 'ver_detalhes')
    list_filter = ('status', 'data_pedido')
    search_fields = ('id', 'utilizador__username', 'email', 'nome_completo')
    readonly_fields = ('data_pedido', 'total', 'subtotal', 'iva')
    
    fieldsets = (
        ('Informação do Pedido', {
            'fields': ('utilizador', 'data_pedido', 'status', 'numero_rastreio')
        }),
        ('Valores', {
            'fields': ('subtotal', 'iva', 'total')
        }),
        ('Dados de Entrega', {
            'fields': ('nome_completo', 'email', 'telefone', 'morada', 'cidade', 'codigo_postal', 'pais')
        }),
        ('Observações', {
            'fields': ('notas',),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ItemPedidoInline]
    
    def utilizador_nome(self, obj):
        return obj.utilizador.username
    utilizador_nome.short_description = 'Utilizador'
    
    def status_badge(self, obj):
        colors = {
            'pendente': '#ff9800',
            'processando': '#2196f3',
            'enviado': '#00bcd4',
            'entregue': '#4caf50',
            'cancelado': '#f44336',
        }
        icons = {
            'pendente': '⏳',
            'processando': '⚙️',
            'enviado': '📦',
            'entregue': '✅',
            'cancelado': '❌',
        }
        color = colors.get(obj.status, '#999')
        icon = icons.get(obj.status, '�')
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 12px; border-radius: 10px; font-size: 11px; font-weight: bold;">{} {}</span>',
            color, icon, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def total_formatado(self, obj):
        return format_html('<span style="color: #4caf50; font-weight: bold; font-size: 1.1em;">{}€</span>', f'{obj.total:.2f}')
    total_formatado.short_description = 'Total'
    
    def ver_detalhes(self, obj):
        return format_html('<a href="/admin/members/pedido/{}/change/" style="color: #d2691e; font-weight: bold;">📄 Ver</a>', obj.id)
    ver_detalhes.short_description = 'Ações'
    
    actions = ['marcar_processando', 'marcar_enviado', 'marcar_entregue']
    
    def marcar_processando(self, request, queryset):
        updated = queryset.update(status='processando')
        self.message_user(request, f'{updated} pedido(s) marcado(s) como processando.')
    marcar_processando.short_description = '⚙️ Marcar como Processando'
    
    def marcar_enviado(self, request, queryset):
        updated = 0
        for pedido in queryset:
            if pedido.status != 'enviado':
                pedido.status = 'enviado'
                pedido.save()
                updated += 1
                # Enviar email
                try:
                    enviar_email_pedido_enviado(pedido)
                except Exception as e:
                    print(f"Error enviando email para pedido #{pedido.id}: {e}")
        
        self.message_user(request, f'{updated} pedido(s) marcado(s) como enviado. Emails enviados.')
    marcar_enviado.short_description = '📦 Marcar como Enviado (+ Email)'
    
    def marcar_entregue(self, request, queryset):
        updated = queryset.update(status='entregue')
        self.message_user(request, f'{updated} pedido(s) marcado(s) como entregue.')
    marcar_entregue.short_description = '✅ Marcar como Entregue'


# ==================== ADMINISTRACIÓN DE AVALIAÇÕES ====================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('livro', 'utilizador', 'rating_stars', 'titulo', 'verificado', 'data_criacao')
    list_filter = ('rating', 'verificado', 'data_criacao')
    search_fields = ('livro__titulo', 'utilizador__username', 'titulo', 'comentario')
    readonly_fields = ('data_criacao',)
    list_editable = ('verificado',)
    
    fieldsets = (
        ('Informação da Avaliação', {
            'fields': ('livro', 'utilizador', 'rating', 'titulo', 'comentario')
        }),
        ('Metadados', {
            'fields': ('verificado', 'data_criacao')
        }),
    )
    
    def rating_stars(self, obj):
        stars = '⭐' * obj.rating
        return format_html(f'<span style="font-size: 16px;">{stars}</span>')
    rating_stars.short_description = 'Avaliação'


# ==================== ADMINISTRACIÓN DE FAVORITOS ====================
@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('utilizador', 'livro', 'data_adicao')
    list_filter = ('data_adicao',)
    search_fields = ('utilizador__username', 'livro__titulo', 'livro__autor')
    readonly_fields = ('data_adicao',)
    
    fieldsets = (
        ('Informação do Favorito', {
            'fields': ('utilizador', 'livro')
        }),
        ('Metadados', {
            'fields': ('data_adicao',)
        }),
    )


# ==================== ADMINISTRACIÓN DE CUPONS ====================
class UsoCupomInline(admin.TabularInline):
    model = UsoCupom
    extra = 0
    readonly_fields = ('utilizador', 'pedido', 'data_uso', 'valor_desconto')
    can_delete = False


@admin.register(Cupom)
class CupomAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'tipo_desconto', 'valor_display', 'validade', 'status', 'usado_display', 'ativo')
    list_filter = ('tipo_desconto', 'ativo', 'data_inicio', 'data_fim')
    search_fields = ('codigo', 'descricao')
    list_editable = ('ativo',)
    readonly_fields = ('vezes_usado', 'data_criacao', 'uso_maximo', 'uso_por_utilizador')
    inlines = [UsoCupomInline]
    
    fieldsets = (
        ('Informação do Cupom', {
            'fields': ('codigo', 'descricao', 'ativo')
        }),
        ('Desconto', {
            'fields': ('tipo_desconto', 'valor', 'valor_minimo_pedido')
        }),
        ('Validade', {
            'fields': ('data_inicio', 'data_fim')
        }),
        ('⚠️ USO ÚNICO - AUTOMÁTICO', {
            'fields': ('uso_maximo', 'uso_por_utilizador'),
            'description': 'Estos campos son AUTOMÁTICOS. Todos los cupones son de UN SOLO USO.',
            'classes': ('collapse',)
        }),
        ('Estatísticas', {
            'fields': ('vezes_usado', 'data_criacao'),
            'classes': ('collapse',)
        }),
    )
    
    def valor_display(self, obj):
        if obj.tipo_desconto == 'percentagem':
            return f"{obj.valor}%"
        return f"€{obj.valor}"
    valor_display.short_description = 'Valor'
    
    def validade(self, obj):
        inicio = obj.data_inicio.strftime('%d/%m/%Y')
        fim = obj.data_fim.strftime('%d/%m/%Y')
        return f"{inicio} - {fim}"
    validade.short_description = 'Período de Validade'
    
    def status(self, obj):
        if obj.esta_valido():
            return format_html('<span style="color: green; font-weight: bold;">✓ Válido</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Inválido</span>')
    status.short_description = 'Status'
    
    def usado_display(self, obj):
        if obj.vezes_usado >= obj.uso_maximo:
            return format_html('<span style="color: red; font-weight: bold; font-size: 14px;">✗ USADO</span>')
        return format_html('<span style="color: green; font-weight: bold; font-size: 14px;">✓ DISPONIBLE</span>')
    usado_display.short_description = 'Estado de Uso'
    
    def save_model(self, request, obj, form, change):
        # FORZAR que SIEMPRE sea de un solo uso
        obj.uso_maximo = 1
        obj.uso_por_utilizador = 1
        super().save_model(request, obj, form, change)


@admin.register(UsoCupom)
class UsoCupomAdmin(admin.ModelAdmin):
    list_display = ('cupom', 'utilizador', 'pedido', 'valor_desconto_display', 'data_uso')
    list_filter = ('data_uso', 'cupom')
    search_fields = ('cupom__codigo', 'utilizador__username', 'pedido__id')
    readonly_fields = ('cupom', 'utilizador', 'pedido', 'data_uso', 'valor_desconto')
    
    def valor_desconto_display(self, obj):
        return f"€{obj.valor_desconto}"
    valor_desconto_display.short_description = 'Desconto'
    
    def has_add_permission(self, request):
        return False  # No permitir crear usos manualmente
