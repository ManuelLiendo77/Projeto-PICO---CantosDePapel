import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Livro

# Buscar y eliminar todos los libros con título "Trip"
livros_trip = Livro.objects.filter(titulo__icontains='Trip')

print(f"Encontrados {livros_trip.count()} livros con 'Trip' en el título:")
for livro in livros_trip:
    print(f"  - ID: {livro.id}, Título: {livro.titulo}, Autor: {livro.autor}")

if livros_trip.exists():
    confirmacion = input("\n¿Deseas eliminar estos libros? (s/n): ")
    if confirmacion.lower() == 's':
        count = livros_trip.count()
        livros_trip.delete()
        print(f"\n✓ {count} livro(s) eliminado(s) con éxito!")
    else:
        print("\nOperación cancelada.")
else:
    print("\nNo se encontraron libros con 'Trip' en el título.")
