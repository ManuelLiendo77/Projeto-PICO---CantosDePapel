# Como Adicionar Filmes com Streaming - Guia Rápido

## Método 1: Admin do Django (Recomendado)

### Passo 1: Aceder ao Admin
1. Vá para: `http://localhost:8000/admin/`
2. Login com conta de superusuário

### Passo 2: Editar um Livro
1. Clique em **"Livros"**
2. Selecione o livro que tem adaptação cinematográfica
3. Marque a caixa **"Tem filme"** ✓

### Passo 3: Adicionar Dados do Filme
Na secção **"Adaptação Cinematográfica"**:

**Título**: Nome do filme (ex: "Harry Potter e a Pedra Filosofal")

**Trailer URL**: Cole uma destas URLs:
- YouTube: `https://www.youtube.com/watch?v=VIDEO_ID`
- YouTube curto: `https://youtu.be/VIDEO_ID`
- Vimeo: `https://vimeo.com/VIDEO_ID`

**URL Netflix** (opcional): 
```
https://www.netflix.com/title/CODIGO_DO_FILME
```
Exemplo: `https://www.netflix.com/title/81001301`

**URL Prime Video** (opcional):
```
https://www.primevideo.com/detail/CODIGO_DO_FILME
```
Exemplo: `https://www.primevideo.com/detail/0H3BLGK1MXSTLWHW3LQFNGQZ8A`

### Passo 4: Guardar
Clique em **"Guardar"** no fundo da página

---

## Método 2: Shell do Django

### Executar o script de exemplo:
```bash
cd projeto_livraria
python manage.py shell < exemplo_adicionar_filmes_streaming.py
```

### Ou manualmente:
```bash
python manage.py shell
```

```python
from members.models import Livro, Filme

# Encontrar o livro
livro = Livro.objects.get(id=1)  # ou get(titulo__icontains="Nome do Livro")

# Marcar como tendo filme
livro.tem_filme = True
livro.save()

# Criar/Atualizar o filme
filme, created = Filme.objects.update_or_create(
    livro=livro,
    defaults={
        'titulo': 'Nome do Filme',
        'trailer_url': 'https://www.youtube.com/watch?v=...',
        'url_netflix': 'https://www.netflix.com/title/...',  # ou None
        'url_prime_video': 'https://www.primevideo.com/detail/...',  # ou None
    }
)

print(f"Filme {'criado' if created else 'atualizado'}: {filme.titulo}")
```

---

## Como Encontrar as URLs

### YouTube
1. Vá para o YouTube e procure: `"Nome do Livro" official trailer`
2. Abra o vídeo
3. Copie a URL da barra de endereço
4. Exemplo: `https://www.youtube.com/watch?v=VyHV0BRtdxo`

### Netflix
1. Vá para Netflix.com
2. Procure pelo filme
3. Abra a página do filme
4. Copie a URL (algo como `/title/81001301`)
5. URL completa: `https://www.netflix.com/title/81001301`

**Dica**: Se não encontrar, deixe em branco. O sistema mostrará um link de pesquisa.

### Prime Video
1. Vá para PrimeVideo.com
2. Procure pelo filme
3. Abra a página do filme
4. Copie a URL (algo como `/detail/CODIGO_LONGO`)
5. URL completa: `https://www.primevideo.com/detail/0H3BLGK1MXSTLWHW3LQFNGQZ8A`

---

## Exemplos de Livros Populares com Filmes

### Harry Potter
```python
Título do Filme: Harry Potter e a Pedra Filosofal
Trailer: https://www.youtube.com/watch?v=VyHV0BRtdxo
Netflix: https://www.netflix.com/title/81001301
Prime: (verificar disponibilidade)
```

### O Senhor dos Anéis
```python
Título do Filme: O Senhor dos Anéis: A Sociedade do Anel
Trailer: https://www.youtube.com/watch?v=V75dMMIW2B4
Netflix: (não disponível)
Prime: https://www.primevideo.com/detail/...
```

### O Código Da Vinci
```python
Título do Filme: O Código Da Vinci
Trailer: https://www.youtube.com/watch?v=5sU9MT8829k
Netflix: https://www.netflix.com/title/70044605
Prime: (verificar disponibilidade)
```

---

## Verificar se Funcionou

1. Vá para a página de detalhes do livro
2. Deve aparecer a secção **"Adaptação Cinematográfica"**
3. O trailer deve estar a reproduzir (se a URL estiver correta)
4. Os botões de streaming devem aparecer (se configurados)

### Troubleshooting

**Trailer não aparece?**
- Verifique se a URL está correta
- Teste a URL no navegador
- Certifique-se de que é YouTube ou Vimeo

**Botão de streaming não aparece?**
- Verifique se a URL está preenchida
- Não deve estar vazia ou `None`

**Secção não aparece?**
- Verifique se `tem_filme = True` no livro
- Verifique se existe um objeto `Filme` associado

---

## Migração de Dados em Massa

Se tiver muitos livros para atualizar, crie um script:

```python
# atualizar_filmes_streaming.py
from members.models import Livro, Filme

filmes_data = [
    {
        'livro_titulo': 'Harry Potter',
        'filme_titulo': 'Harry Potter e a Pedra Filosofal',
        'trailer': 'https://www.youtube.com/watch?v=VyHV0BRtdxo',
        'netflix': 'https://www.netflix.com/title/81001301',
        'prime': None,
    },
    # ... mais filmes
]

for data in filmes_data:
    try:
        livro = Livro.objects.get(titulo__icontains=data['livro_titulo'])
        livro.tem_filme = True
        livro.save()
        
        Filme.objects.update_or_create(
            livro=livro,
            defaults={
                'titulo': data['filme_titulo'],
                'trailer_url': data['trailer'],
                'url_netflix': data['netflix'],
                'url_prime_video': data['prime'],
            }
        )
        print(f"✅ {data['filme_titulo']}")
    except Exception as e:
        print(f"❌ Erro: {data['livro_titulo']} - {e}")
```

Execute:
```bash
python manage.py shell < atualizar_filmes_streaming.py
```

---

## Manutenção

### Verificar links quebrados
```python
from members.models import Filme
import requests

for filme in Filme.objects.all():
    if filme.url_netflix:
        # Verificar se link funciona
        # (implementar lógica de verificação)
        pass
```

### Estatísticas
```python
from members.models import Filme

total = Filme.objects.count()
com_netflix = Filme.objects.exclude(url_netflix__isnull=True).exclude(url_netflix='').count()
com_prime = Filme.objects.exclude(url_prime_video__isnull=True).exclude(url_prime_video='').count()

print(f"Total: {total}")
print(f"Netflix: {com_netflix} ({com_netflix/total*100:.1f}%)")
print(f"Prime: {com_prime} ({com_prime/total*100:.1f}%)")
```

---

**Última atualização**: 4 de janeiro de 2026  
**Documentação criada por**: Especialista em Integrações
