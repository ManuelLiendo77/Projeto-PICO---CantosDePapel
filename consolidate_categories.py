import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Livro

# Mapeo de consolidación de categorías
consolidacao = {
    # Mantener estas categorías principales
    'Literatura Portuguesa': 'Literatura Portuguesa',
    'Crítica Literária': 'Crítica Literária',
    'Ficção': 'Ficção',
    'História de Portugal': 'História de Portugal',
    'História': 'História',
    
    # Consolidar categorías menores
    'Foreign Language Study': 'Línguas e Linguística',
    'Language Arts & Disciplines': 'Línguas e Linguística',
    'Brazilian literature': 'Literatura Brasileira',
    'African literature (Portuguese)': 'Literatura Lusófona',
    'Literary Collections': 'Antologias e Coletâneas',
    'Comparative literature': 'Estudos Literários',
    'Literatura Geral': 'Outros',
    
    # Categorías específicas que se pueden consolidar
    'Art': 'Arte e Cultura',
    'Performing Arts': 'Arte e Cultura',
    'Photography': 'Arte e Cultura',
    
    # Humanidades y ciencias sociales
    'Philosophy': 'Filosofia e Ciências Sociais',
    'Political Science': 'Filosofia e Ciências Sociais',
    'Psychology': 'Filosofia e Ciências Sociais',
    'Authoritarianism': 'Filosofia e Ciências Sociais',
    
    # Otros
    'Religion': 'Religião e Espiritualidade',
    'Autoajuda e Espiritualidade': 'Religião e Espiritualidade',
    'Antiques & Collectibles': 'Outros',
}

print("Consolidando categorías...")
print("=" * 60)

livros = Livro.objects.all()
atualizados = 0

for livro in livros:
    categoria_original = livro.categoria
    
    if categoria_original in consolidacao:
        categoria_nova = consolidacao[categoria_original]
        
        if categoria_original != categoria_nova:
            livro.categoria = categoria_nova
            livro.save()
            atualizados += 1
            print(f"✓ {livro.titulo[:40]}: {categoria_original} → {categoria_nova}")

print("\n" + "=" * 60)
print(f"Total actualizado: {atualizados} libros")

# Mostrar categorías finales
print("\n" + "=" * 60)
print("CATEGORÍAS FINALES:")
categorias_finales = Livro.objects.values_list('categoria', flat=True).distinct().order_by('categoria')

for cat in categorias_finales:
    if cat:
        count = Livro.objects.filter(categoria=cat).count()
        print(f"  • {cat}: {count} livros")
