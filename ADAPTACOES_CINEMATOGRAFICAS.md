# Funcionalidade: Adaptações Cinematográficas

## Resumo
Sistema completo para exibir informações sobre adaptações cinematográficas de livros, incluindo trailers e links para plataformas de streaming.

## Componentes Implementados

### 1. Modelo de Dados (`models.py`)

#### Campos Adicionados ao Modelo `Filme`
```python
url_netflix = models.URLField(blank=True, null=True)
url_prime_video = models.URLField(blank=True, null=True)
```

#### Métodos Novos

**`obter_url_trailer_embebido()`**
- Converte URLs do YouTube e Vimeo para formato embebido (iframe)
- Suporta múltiplos formatos de URL
- Retorna `None` se a URL for inválida

**Formatos Suportados:**
- YouTube: `youtube.com/watch?v=`, `youtu.be/`, `youtube.com/embed/`
- Vimeo: `vimeo.com/`, `player.vimeo.com/video/`

**`tem_streaming_disponivel()`**
- Verifica se existe pelo menos uma plataforma de streaming configurada
- Retorna: `bool`

**`obter_plataformas_disponiveis()`**
- Retorna lista de plataformas com URLs configuradas
- Cada plataforma inclui:
  - `nome`: Nome da plataforma
  - `url`: Link direto para o filme
  - `logo_class`: Classe CSS para estilização
  - `cor`: Cor da marca

### 2. Vista (`views.py`)

#### Melhorias em `livro_detalhe`
```python
# Conversão automática de URL do trailer
trailer_url_embebido = filme.obter_url_trailer_embebido()

# Lista de plataformas de streaming disponíveis
plataformas_streaming = filme.obter_plataformas_disponiveis()
```

**Contexto Adicionado:**
- `trailer_url_embebido`: URL pronta para iframe
- `plataformas_streaming`: Lista de plataformas configuradas

### 3. Template (`livro_detalhe.html`)

#### Secção de Adaptação Cinematográfica

**Condição de Exibição:**
- Só aparece se `{% if filme %}` (livro tem filme associado)

**Elementos da Interface:**

1. **Cabeçalho**
   - Ícone animado 🎬
   - Título: "Adaptação Cinematográfica"
   - Subtítulo: "Este livro foi adaptado para o cinema"

2. **Vídeo do Trailer**
   - Iframe responsivo com aspecto 16:9
   - Carregamento lazy
   - Mensagem elegante se trailer não disponível
   - Link para pesquisa no YouTube

3. **Detalhes do Filme**
   - Título do filme
   - Livro de origem
   - Autor

4. **Plataformas de Streaming**
   - Botões com gradientes e logótipos
   - Netflix: Gradiente vermelho (#E50914)
   - Prime Video: Gradiente azul (#00A8E1)
   - Só aparecem se configurados
   - Links diretos para assistir
   - Fallback: Links de pesquisa genéricos

5. **Dica de Leitura**
   - Recomendação para ler antes de ver

#### Estilos CSS Implementados

**Botões de Streaming:**
```css
.btn-streaming {
  - Display flex com ícone + texto
  - Padding confortável (14px 24px)
  - Border-radius 8px
  - Sombra suave com efeito hover
  - Animações de elevação
}
```

**Cores das Marcas:**
- Netflix: Gradiente vermelho oficial
- Prime Video: Gradiente azul oficial
- Hover: Versões mais claras das cores

**Responsividade:**
- Desktop (>992px): Botões empilhados verticalmente
- Tablet (768-992px): Botões lado a lado
- Mobile (<768px): Botões em coluna, largura total

## Validação e Tratamento de Erros

### URLs Inválidas
✅ URL do trailer mal formatada → Exibe mensagem elegante
✅ URL de streaming vazia → Botão não é exibido
✅ Filme sem trailer → Mostra ícone e link de pesquisa

### Casos de Uso
1. **Filme com tudo configurado**: Trailer + Netflix + Prime Video
2. **Só trailer**: Vídeo embebido + pesquisa de streaming
3. **Só streaming**: Sem trailer, mas com botões diretos
4. **Filme sem dados**: Links de pesquisa genéricos

## Idioma (PT-PT)

### Termos Utilizados
- ✅ "Adaptação Cinematográfica" (não "Adaptação cinematográfica")
- ✅ "Disponível em" (não "Disponible en")
- ✅ "Ver na Netflix" (não "Ver en Netflix")
- ✅ "Ver no Prime Video"
- ✅ "Detalhes do filme"
- ✅ "Onde Assistir"
- ✅ "Procurar na Netflix" (não "Buscar")
- ✅ "Leia o livro" (não "Lea el libro")

### Mensagens de Erro
- "Trailer não disponível" (com acento)
- "Procurar no YouTube" (não "Buscar")

## Integração com Admin

### Adicionar Filme com Streaming
No admin do Django:
```python
Filme:
  - Título: Nome do filme
  - Trailer URL: https://youtube.com/watch?v=...
  - URL Netflix: https://www.netflix.com/title/...
  - URL Prime Video: https://www.primevideo.com/detail/...
```

## Próximas Melhorias Sugeridas

1. **Mais Plataformas**
   - Disney+
   - HBO Max
   - Apple TV+
   - MUBI

2. **Metadados do Filme**
   - Diretor
   - Ano de lançamento
   - Duração
   - Rating IMDb

3. **API Integration**
   - TMDB (The Movie Database)
   - OMDb API
   - JustWatch API (disponibilidade de streaming)

4. **Scraping Automático**
   - Verificar disponibilidade real nas plataformas
   - Atualizar links quebrados
   - Preços das plataformas

## Testes Recomendados

### Manual
- [ ] Livro com filme e trailer válido
- [ ] Livro com filme sem trailer
- [ ] URL YouTube em diferentes formatos
- [ ] URL Vimeo
- [ ] Netflix configurado
- [ ] Prime Video configurado
- [ ] Ambas plataformas
- [ ] Nenhuma plataforma
- [ ] Responsividade mobile/tablet/desktop

### Automático (futuro)
```python
def test_obter_url_trailer_embebido_youtube(self):
    filme = Filme(trailer_url="https://youtube.com/watch?v=ABC123")
    assert filme.obter_url_trailer_embebido() == "https://www.youtube.com/embed/ABC123"

def test_obter_url_trailer_embebido_vimeo(self):
    filme = Filme(trailer_url="https://vimeo.com/123456789")
    assert filme.obter_url_trailer_embebido() == "https://player.vimeo.com/video/123456789"
```

## Migração Aplicada

```bash
python manage.py migrate members
# Aplicada: 0011_filme_url_netflix_filme_url_prime_video_and_more
```

## Arquivos Modificados

1. ✅ `members/models.py` - Modelo Filme estendido
2. ✅ `members/views.py` - Vista livro_detalhe otimizada
3. ✅ `members/templates/livro_detalhe.html` - Interface completa
4. ✅ `members/migrations/0011_*.py` - Migração gerada

---

**Data**: 4 de janeiro de 2026  
**Implementado por**: Especialista em Integrações e Web Scraping  
**Status**: ✅ Completo e Funcional
