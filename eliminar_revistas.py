import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Livro

# Buscar todos los libros que parecen ser revistas
# Buscamos por título que contenga "Trip", "Revista", "Magazine", etc.
revistas_keywords = ['trip', 'revista', 'magazine', 'journal', 'periódico']

livros_eliminados = []

for keyword in revistas_keywords:
    revistas = Livro.objects.filter(titulo__icontains=keyword)
    
    for revista in revistas:
        print(f"📰 Encontrada revista: {revista.titulo} (ID: {revista.id})")
        print(f"   Autor: {revista.autor}")
        print(f"   ISBN: {revista.isbn}")
        livros_eliminados.append(revista.titulo)
        revista.delete()
        print(f"   ✅ Eliminada!\n")

if livros_eliminados:
    print(f"\n✅ Total de revistas eliminadas: {len(livros_eliminados)}")
    print("Revistas eliminadas:")
    for titulo in livros_eliminados:
        print(f"  - {titulo}")
else:
    print("ℹ️ No se encontraron revistas en la base de datos.")
