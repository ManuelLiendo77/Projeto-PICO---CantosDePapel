import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Livro, Preco, Loja

def recrear_tiendas_y_precios():
    """
    Recrea las tiendas Amazon y FNAC (solo reales, sin ficticias)
    y agrega precios para todos los libros.
    """
    
    # Crear/obtener tiendas reales
    amazon, created = Loja.objects.get_or_create(
        nome='Amazon',
        defaults={'url': 'https://www.amazon.es'}
    )
    print(f"{'✓ Creada' if created else '✓ Ya existe'}: Amazon")
    
    fnac, created = Loja.objects.get_or_create(
        nome='FNAC',
        defaults={'url': 'https://www.fnac.pt'}
    )
    print(f"{'✓ Creada' if created else '✓ Ya existe'}: FNAC")
    
    cantos_de_papel = Loja.objects.get(nome='Cantos de Papel')
    
    print("\n" + "="*60)
    print("Agregando precios para todos los libros...")
    print("="*60 + "\n")
    
    # Obtener todos los libros con precio de Cantos de Papel
    livros = Livro.objects.all()
    
    contador_actualizados = 0
    contador_sin_precio_base = 0
    
    for livro in livros:
        # Obtener el precio base de Cantos de Papel
        precio_cantos = livro.preco_set.filter(loja=cantos_de_papel).first()
        
        if not precio_cantos:
            contador_sin_precio_base += 1
            continue
        
        precio_base = float(precio_cantos.preco)
        
        # Generar precios para las otras tiendas con variaciones realistas
        # Amazon: generalmente más barato (5-15% menos)
        precio_amazon = precio_base * random.uniform(0.85, 0.95)
        
        # FNAC: generalmente un poco más caro (0-10% más)
        precio_fnac = precio_base * random.uniform(1.00, 1.10)
        
        # Redondear a 2 decimales y convertir a Decimal
        precio_amazon = Decimal(str(round(precio_amazon, 2)))
        precio_fnac = Decimal(str(round(precio_fnac, 2)))
        
        # Crear URLs realistas
        titulo_slug = livro.titulo.lower().replace(' ', '-').replace(',', '')[:50]
        isbn_slug = str(livro.isbn) if livro.isbn else 'no-isbn'
        
        # Crear o actualizar precios
        Preco.objects.get_or_create(
            livro=livro,
            loja=amazon,
            defaults={
                'preco': precio_amazon,
                'url_produto': f'https://www.amazon.es/dp/{isbn_slug}'
            }
        )
        
        Preco.objects.get_or_create(
            livro=livro,
            loja=fnac,
            defaults={
                'preco': precio_fnac,
                'url_produto': f'https://www.fnac.pt/livro/{titulo_slug}/{isbn_slug}'
            }
        )
        
        contador_actualizados += 1
        print(f"✓ {livro.titulo}")
        print(f"  Cantos de Papel: {precio_base:.2f}€ | Amazon: {precio_amazon:.2f}€ | FNAC: {precio_fnac:.2f}€")
    
    print("\n" + "="*60)
    print(f"✓ Proceso completado!")
    print(f"  - Libros actualizados: {contador_actualizados}")
    print(f"  - Libros sin precio base: {contador_sin_precio_base}")
    print(f"  - Total de precios en BD: {Preco.objects.count()}")
    print(f"  - Tiendas: {', '.join([l.nome for l in Loja.objects.all()])}")

if __name__ == '__main__':
    recrear_tiendas_y_precios()
