import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Livro, Preco, Loja

def agregar_precios_base_y_comparacion():
    """
    1. Agrega precios base de Cantos de Papel a todos los libros sin precio
    2. Agrega precios de Amazon y FNAC para todos los libros
    """
    
    cantos_de_papel = Loja.objects.get(nome='Cantos de Papel')
    amazon = Loja.objects.get(nome='Amazon')
    fnac = Loja.objects.get(nome='FNAC')
    
    livros = Livro.objects.all()
    
    print("="*60)
    print("PASO 1: Agregando precios base de Cantos de Papel")
    print("="*60 + "\n")
    
    contador_nuevos = 0
    
    for livro in livros:
        # Verificar si ya tiene precio de Cantos de Papel
        if livro.preco_set.filter(loja=cantos_de_papel).exists():
            continue
        
        # Generar precio base realista según categoría
        if livro.categoria:
            categoria_lower = livro.categoria.lower()
            if 'fiction' in categoria_lower or 'literature' in categoria_lower:
                precio_base = random.uniform(12.99, 24.99)
            elif 'science' in categoria_lower or 'history' in categoria_lower:
                precio_base = random.uniform(15.99, 29.99)
            elif 'biography' in categoria_lower or 'travel' in categoria_lower:
                precio_base = random.uniform(14.99, 26.99)
            else:
                precio_base = random.uniform(13.99, 25.99)
        else:
            precio_base = random.uniform(14.99, 24.99)
        
        # Redondear a .99 o .49
        precio_base = round(precio_base)
        if random.random() > 0.5:
            precio_base = precio_base - 0.01  # X.99
        else:
            precio_base = precio_base - 0.51  # X.49
        
        precio_base = Decimal(str(round(precio_base, 2)))
        
        # Crear precio de Cantos de Papel
        Preco.objects.create(
            livro=livro,
            loja=cantos_de_papel,
            preco=precio_base,
            url_produto=f'https://cantosdepaapel.com/livros/{livro.id}/'
        )
        
        contador_nuevos += 1
        print(f"✓ {livro.titulo[:50]}: {precio_base}€")
    
    print(f"\n✓ Agregados {contador_nuevos} precios base de Cantos de Papel\n")
    
    print("="*60)
    print("PASO 2: Agregando precios de Amazon y FNAC")
    print("="*60 + "\n")
    
    contador_comparacion = 0
    
    for livro in livros:
        # Obtener precio base
        precio_cantos = livro.preco_set.filter(loja=cantos_de_papel).first()
        if not precio_cantos:
            continue
        
        precio_base = float(precio_cantos.preco)
        
        # Si ya tiene precios de otras tiendas, saltar
        if livro.preco_set.filter(loja=amazon).exists():
            continue
        
        # Generar precios para otras tiendas
        precio_amazon = precio_base * random.uniform(0.85, 0.95)
        precio_fnac = precio_base * random.uniform(1.00, 1.10)
        
        precio_amazon = Decimal(str(round(precio_amazon, 2)))
        precio_fnac = Decimal(str(round(precio_fnac, 2)))
        
        # Crear URLs
        titulo_slug = livro.titulo.lower().replace(' ', '-').replace(',', '')[:50]
        isbn_slug = str(livro.isbn) if livro.isbn else 'no-isbn'
        
        Preco.objects.create(
            livro=livro,
            loja=amazon,
            preco=precio_amazon,
            url_produto=f'https://www.amazon.es/dp/{isbn_slug}'
        )
        
        Preco.objects.create(
            livro=livro,
            loja=fnac,
            preco=precio_fnac,
            url_produto=f'https://www.fnac.pt/livro/{titulo_slug}/{isbn_slug}'
        )
        
        contador_comparacion += 1
        print(f"✓ {livro.titulo[:40]}: Cantos {precio_base:.2f}€ | Amazon {precio_amazon:.2f}€ | FNAC {precio_fnac:.2f}€")
    
    print("\n" + "="*60)
    print("✓ Proceso completado!")
    print(f"  - Nuevos precios base: {contador_nuevos}")
    print(f"  - Precios de comparación agregados: {contador_comparacion}")
    print(f"  - Total libros en BD: {Livro.objects.count()}")
    print(f"  - Total precios en BD: {Preco.objects.count()}")
    print(f"  - Libros con comparación: {Livro.objects.filter(preco__loja=amazon).distinct().count()}")

if __name__ == '__main__':
    agregar_precios_base_y_comparacion()
