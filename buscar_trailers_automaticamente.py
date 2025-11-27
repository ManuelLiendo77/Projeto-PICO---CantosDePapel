import os
import django
import requests
import time
from urllib.parse import quote

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Livro, Filme

# No necesitas API key de YouTube para buscar, usamos scraping simple
def buscar_trailer_youtube(titulo_libro, autor):
    """Busca el trailer en YouTube y devuelve el video ID"""
    # Construir query de búsqueda
    query = f"{titulo_libro} {autor} official movie trailer"
    query_encoded = quote(query)
    
    # Construir URL de búsqueda de YouTube
    search_url = f"https://www.youtube.com/results?search_query={query_encoded}"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Buscar el primer video ID en la respuesta
            content = response.text
            
            # Buscar patrón de video ID
            import re
            pattern = r'"videoId":"([a-zA-Z0-9_-]{11})"'
            match = re.search(pattern, content)
            
            if match:
                video_id = match.group(1)
                trailer_url = f"https://www.youtube.com/watch?v={video_id}"
                embed_url = f"https://www.youtube.com/embed/{video_id}"
                return trailer_url, embed_url
    
    except Exception as e:
        print(f"  ⚠️  Erro ao buscar trailer: {e}")
    
    return None, None

def buscar_onde_assistir(titulo_livro):
    """Sugiere plataformas donde se puede ver la película"""
    # Plataformas comunes
    plataformas = [
        "Netflix",
        "Amazon Prime Video", 
        "Disney+",
        "HBO Max",
        "Apple TV+",
        "Paramount+"
    ]
    
    # Por ahora retornamos un mensaje genérico
    # En producción podrías usar APIs como JustWatch, TMDB, etc.
    return f"Verifique a disponibilidade em: {', '.join(plataformas)}"

def processar_livros_com_filmes():
    """Procesa todos los libros con películas y busca sus trailers"""
    print("\n" + "="*80)
    print("🎬 BUSCAR TRAILERS AUTOMÁTICAMENTE - YouTube")
    print("="*80 + "\n")
    
    # Obtener todos los libros que tienen película
    livros_com_filme = Livro.objects.filter(tem_filme=True)
    total = livros_com_filme.count()
    
    print(f"📚 Encontrados {total} livros com filmes\n")
    
    criados = 0
    atualizados = 0
    erros = 0
    
    for idx, livro in enumerate(livros_com_filme, 1):
        print(f"[{idx}/{total}] Processando: {livro.titulo} - {livro.autor}")
        
        # Verificar si ya tiene un registro de Filme
        try:
            filme = Filme.objects.get(livro=livro)
            if filme.trailer_url:
                print(f"  ℹ️  Já tem trailer: {filme.trailer_url}")
                continue
            
            # Buscar trailer
            trailer_url, embed_url = buscar_trailer_youtube(livro.titulo, livro.autor)
            
            if trailer_url:
                filme.trailer_url = embed_url
                filme.save()
                print(f"  ✓ Trailer atualizado: {trailer_url}")
                atualizados += 1
            else:
                print(f"  ❌ Trailer não encontrado")
                erros += 1
                
        except Filme.DoesNotExist:
            # Crear nuevo registro de Filme
            trailer_url, embed_url = buscar_trailer_youtube(livro.titulo, livro.autor)
            
            if trailer_url:
                # Crear título de película basado en el título del libro
                titulo_filme = livro.titulo
                
                Filme.objects.create(
                    livro=livro,
                    titulo=titulo_filme,
                    trailer_url=embed_url
                )
                print(f"  ✓ Filme criado com trailer: {trailer_url}")
                criados += 1
            else:
                # Crear sin trailer por ahora
                Filme.objects.create(
                    livro=livro,
                    titulo=livro.titulo,
                    trailer_url=""
                )
                print(f"  ⚠️  Filme criado sem trailer")
                erros += 1
        
        except Exception as e:
            print(f"  ❌ Erro: {e}")
            erros += 1
        
        # Delay para no sobrecargar YouTube
        time.sleep(1)
    
    # Resumen
    print("\n" + "="*80)
    print("📊 RESUMO")
    print("="*80)
    print(f"✓ Filmes criados com trailer: {criados}")
    print(f"✓ Trailers atualizados: {atualizados}")
    print(f"❌ Sem trailer: {erros}")
    print(f"📚 Total processado: {total}")
    print("="*80 + "\n")

if __name__ == "__main__":
    processar_livros_com_filmes()
