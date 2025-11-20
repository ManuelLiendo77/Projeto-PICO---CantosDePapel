import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Livro

# URLs de imágenes de libros de ejemplo (placeholder de alta calidad)
imagenes_ejemplo = [
    "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=600&fit=crop",
    "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400&h=600&fit=crop",
    "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=600&fit=crop",
    "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400&h=600&fit=crop",
    "https://images.unsplash.com/photo-1524578271613-d550eacf6090?w=400&h=600&fit=crop",
    "https://images.unsplash.com/photo-1509266272358-7701da638078?w=400&h=600&fit=crop",
    "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400&h=600&fit=crop",
    "https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=400&h=600&fit=crop",
]

livros = Livro.objects.all()
print(f"Actualizando {livros.count()} libros con imágenes...")

for i, livro in enumerate(livros):
    imagen_url = imagenes_ejemplo[i % len(imagenes_ejemplo)]
    livro.imagem_capa = imagen_url
    livro.save()
    print(f"✓ {livro.titulo} - Imagen agregada")

print("\n¡Completado! Todos los libros ahora tienen imágenes.")
