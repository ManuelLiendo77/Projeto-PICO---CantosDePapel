import os
import django
import requests
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Livro

def get_book_cover_from_google(titulo, autor, isbn):
    """Obtiene la portada del libro desde Google Books API"""
    base_url = "https://www.googleapis.com/books/v1/volumes"
    
    # Intentar primero por ISBN
    if isbn:
        params = {'q': f'isbn:{isbn}'}
        try:
            response = requests.get(base_url, params=params, timeout=5)
            data = response.json()
            
            if 'items' in data and len(data['items']) > 0:
                volume = data['items'][0]
                if 'imageLinks' in volume.get('volumeInfo', {}):
                    # Preferir thumbnail grande si existe
                    image_links = volume['volumeInfo']['imageLinks']
                    return image_links.get('thumbnail', '').replace('http://', 'https://')
        except:
            pass
    
    # Si no funciona ISBN, intentar por título y autor
    query = f'{titulo} {autor}'.strip()
    params = {'q': query, 'maxResults': 1}
    
    try:
        response = requests.get(base_url, params=params, timeout=5)
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            volume = data['items'][0]
            if 'imageLinks' in volume.get('volumeInfo', {}):
                image_links = volume['volumeInfo']['imageLinks']
                return image_links.get('thumbnail', '').replace('http://', 'https://')
    except:
        pass
    
    return None

def normalizar_categoria(categoria):
    """Normaliza las categorías para evitar duplicados"""
    categoria = categoria.strip()
    
    # Mapeo de categorías
    mapeo = {
        'Portuguese literature': 'Literatura Portuguesa',
        'Portugal': 'História de Portugal',
        'Literary Criticism': 'Crítica Literária',
        'History': 'História',
        'Livros': 'Literatura Geral',
        'Authors, Portuguese': 'Literatura Portuguesa',
        'Fiction': 'Ficção',
        'Body, Mind & Spirit': 'Autoajuda e Espiritualidade',
    }
    
    # Aplicar mapeo
    for key, value in mapeo.items():
        if key.lower() in categoria.lower():
            return value
    
    return categoria

# Obtener todos los libros
livros = Livro.objects.all()
total = livros.count()

print(f"Procesando {total} libros...")
print("=" * 60)

actualizados_imagen = 0
actualizados_categoria = 0
sin_imagen = 0

for i, livro in enumerate(livros, 1):
    print(f"\n[{i}/{total}] {livro.titulo[:50]}...")
    
    # Normalizar categoría
    categoria_antigua = livro.categoria
    categoria_nueva = normalizar_categoria(categoria_antigua)
    
    if categoria_antigua != categoria_nueva:
        livro.categoria = categoria_nueva
        actualizados_categoria += 1
        print(f"  📁 Categoría: {categoria_antigua} → {categoria_nueva}")
    
    # Obtener portada real
    print(f"  🔍 Buscando portada en Google Books...")
    cover_url = get_book_cover_from_google(livro.titulo, livro.autor, livro.isbn)
    
    if cover_url:
        livro.imagem_capa = cover_url
        actualizados_imagen += 1
        print(f"  ✅ Portada encontrada!")
    else:
        sin_imagen += 1
        print(f"  ⚠️  No se encontró portada")
    
    livro.save()
    
    # Pausa para no saturar la API
    if i % 10 == 0:
        print(f"\n  💤 Pausa de 2 segundos...")
        time.sleep(2)
    else:
        time.sleep(0.5)

print("\n" + "=" * 60)
print("RESUMEN:")
print(f"✅ Imágenes actualizadas: {actualizados_imagen}/{total}")
print(f"📁 Categorías normalizadas: {actualizados_categoria}/{total}")
print(f"⚠️  Sin imagen: {sin_imagen}/{total}")
print("\n¡Proceso completado!")

# Mostrar categorías únicas
print("\n" + "=" * 60)
print("CATEGORÍAS FINALES:")
categorias = Livro.objects.values_list('categoria', flat=True).distinct().order_by('categoria')
for cat in categorias:
    count = Livro.objects.filter(categoria=cat).count()
    print(f"  • {cat}: {count} libros")
