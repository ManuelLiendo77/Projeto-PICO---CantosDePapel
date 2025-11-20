import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Livro

# Obtener todas las categorías únicas
categorias = Livro.objects.values_list('categoria', flat=True).distinct().order_by('categoria')

print("CATEGORÍAS EN LA BASE DE DATOS:")
print("=" * 60)

for i, cat in enumerate(categorias, 1):
    if cat:
        count = Livro.objects.filter(categoria=cat).count()
        print(f"{i}. {cat} ({count} livros)")

print("\n" + "=" * 60)
print(f"TOTAL: {len([c for c in categorias if c])} categorías")
