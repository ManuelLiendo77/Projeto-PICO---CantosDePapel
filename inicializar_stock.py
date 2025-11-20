import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Livro

# Actualizar stock de todos los libros
livros = Livro.objects.all()

for livro in livros:
    # Asignar stock aleatorio entre 0 y 50 (más realista)
    livro.stock = random.randint(5, 50)
    livro.stock_minimo = 5
    livro.save()
    print(f"✓ {livro.titulo}: {livro.stock} unidades")

print(f"\n✅ Stock inicializado para {livros.count()} livros!")
