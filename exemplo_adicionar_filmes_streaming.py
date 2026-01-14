"""
Script de exemplo para adicionar filmes com plataformas de streaming.
Execute: python manage.py shell < exemplo_adicionar_filmes_streaming.py
"""

from members.models import Livro, Filme

# Exemplo 1: Harry Potter e a Pedra Filosofal
try:
    livro = Livro.objects.get(titulo__icontains="Harry Potter")
    livro.tem_filme = True
    livro.save()
    
    filme, created = Filme.objects.update_or_create(
        livro=livro,
        defaults={
            'titulo': 'Harry Potter e a Pedra Filosofal',
            'trailer_url': 'https://www.youtube.com/watch?v=VyHV0BRtdxo',
            'url_netflix': 'https://www.netflix.com/title/81001301',
            'url_prime_video': 'https://www.primevideo.com/detail/0H3BLGK1MXSTLWHW3LQFNGQZ8A'
        }
    )
    print(f"✅ Filme {'criado' if created else 'atualizado'}: {filme.titulo}")
except Livro.DoesNotExist:
    print("❌ Livro Harry Potter não encontrado")

# Exemplo 2: O Senhor dos Anéis
try:
    livro = Livro.objects.get(titulo__icontains="Senhor dos Anéis")
    livro.tem_filme = True
    livro.save()
    
    filme, created = Filme.objects.update_or_create(
        livro=livro,
        defaults={
            'titulo': 'O Senhor dos Anéis: A Sociedade do Anel',
            'trailer_url': 'https://www.youtube.com/watch?v=V75dMMIW2B4',
            'url_netflix': None,  # Não disponível na Netflix
            'url_prime_video': 'https://www.primevideo.com/detail/0T3DOX07BFF9BE2XSPFMR5KMBV'
        }
    )
    print(f"✅ Filme {'criado' if created else 'atualizado'}: {filme.titulo}")
except Livro.DoesNotExist:
    print("❌ Livro O Senhor dos Anéis não encontrado")

# Exemplo 3: O Código Da Vinci
try:
    livro = Livro.objects.get(titulo__icontains="Código Da Vinci")
    livro.tem_filme = True
    livro.save()
    
    filme, created = Filme.objects.update_or_create(
        livro=livro,
        defaults={
            'titulo': 'O Código Da Vinci',
            'trailer_url': 'https://www.youtube.com/watch?v=5sU9MT8829k',
            'url_netflix': 'https://www.netflix.com/title/70044605',
            'url_prime_video': None  # Não disponível no Prime Video
        }
    )
    print(f"✅ Filme {'criado' if created else 'atualizado'}: {filme.titulo}")
except Livro.DoesNotExist:
    print("❌ Livro O Código Da Vinci não encontrado")

# Exemplo 4: 1984
try:
    livro = Livro.objects.get(titulo__icontains="1984")
    livro.tem_filme = True
    livro.save()
    
    filme, created = Filme.objects.update_or_create(
        livro=livro,
        defaults={
            'titulo': '1984',
            'trailer_url': 'https://www.youtube.com/watch?v=Z4rBDUJTnNU',
            'url_netflix': None,
            'url_prime_video': None  # Verificar disponibilidade manualmente
        }
    )
    print(f"✅ Filme {'criado' if created else 'atualizado'}: {filme.titulo}")
except Livro.DoesNotExist:
    print("❌ Livro 1984 não encontrado")

# Exemplo 5: O Hobbit
try:
    livro = Livro.objects.get(titulo__icontains="Hobbit")
    livro.tem_filme = True
    livro.save()
    
    filme, created = Filme.objects.update_or_create(
        livro=livro,
        defaults={
            'titulo': 'O Hobbit: Uma Jornada Inesperada',
            'trailer_url': 'https://www.youtube.com/watch?v=SDnYMbYB-nU',
            'url_netflix': None,
            'url_prime_video': 'https://www.primevideo.com/detail/0SZNQ73PU83PSM63N40ZVHF49E'
        }
    )
    print(f"✅ Filme {'criado' if created else 'atualizado'}: {filme.titulo}")
except Livro.DoesNotExist:
    print("❌ Livro O Hobbit não encontrado")

print("\n" + "="*50)
print("Script concluído!")
print("="*50)

# Verificar filmes criados
total_filmes = Filme.objects.count()
filmes_com_netflix = Filme.objects.exclude(url_netflix__isnull=True).exclude(url_netflix='').count()
filmes_com_prime = Filme.objects.exclude(url_prime_video__isnull=True).exclude(url_prime_video='').count()

print(f"\n📊 Estatísticas:")
print(f"Total de filmes: {total_filmes}")
print(f"Com Netflix: {filmes_com_netflix}")
print(f"Com Prime Video: {filmes_com_prime}")
print(f"Com ambas plataformas: {Filme.objects.exclude(url_netflix__isnull=True).exclude(url_prime_video__isnull=True).count()}")
