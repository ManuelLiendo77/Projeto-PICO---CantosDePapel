import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Livro, Preco, Loja

def agregar_precos_para_todos_los_libros():
    """
    Agrega precios de otras tiendas para todos los libros que solo tienen precio de Cantos de Papel.
    """
    # Obtener todas las tiendas
    cantos_de_papel = Loja.objects.get(nome='Cantos de Papel')
    amazon = Loja.objects.get(nome='Amazon')
    fnac = Loja.objects.get(nome='FNAC')
    livraria_online = Loja.objects.get(nome='Livraria Online')
    
    # Obtener libros que solo tienen precio de Cantos de Papel
    livros = Livro.objects.all()
    
    contador_actualizados = 0
    contador_ya_tienen = 0
    
    for livro in livros:
        precos_existentes = livro.preco_set.count()
        
        # Si el libro ya tiene múltiples precios, saltar
        if precos_existentes > 1:
            contador_ya_tienen += 1
            continue
        
        # Obtener el precio base de Cantos de Papel
        precio_cantos = livro.preco_set.filter(loja=cantos_de_papel).first()
        
        if not precio_cantos:
            print(f"⚠ {livro.titulo} no tiene precio de Cantos de Papel, saltando...")
            continue
        
        precio_base = float(precio_cantos.preco)
        
        # Generar precios para las otras tiendas con variaciones realistas
        # Amazon: generalmente más barato (5-15% menos)
        precio_amazon = precio_base * random.uniform(0.85, 0.95)
        
        # FNAC: generalmente un poco más caro (0-10% más)
        precio_fnac = precio_base * random.uniform(1.00, 1.10)
        
        # Livraria Online: varía más (10% menos a 5% más)
        precio_livraria = precio_base * random.uniform(0.90, 1.05)
        
        # Redondear a 2 decimales y convertir a Decimal
        precio_amazon = Decimal(str(round(precio_amazon, 2)))
        precio_fnac = Decimal(str(round(precio_fnac, 2)))
        precio_livraria = Decimal(str(round(precio_livraria, 2)))
        
        # Crear URLs ficticias pero realistas
        titulo_slug = livro.titulo.lower().replace(' ', '-')[:50]
        isbn_slug = str(livro.isbn) if livro.isbn else 'no-isbn'
        
        # Crear o actualizar precios
        Preco.objects.get_or_create(
            livro=livro,
            loja=amazon,
            defaults={
                'preco': precio_amazon,
                'url_produto': f'https://www.amazon.com/dp/{isbn_slug}'
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
        
        Preco.objects.get_or_create(
            livro=livro,
            loja=livraria_online,
            defaults={
                'preco': precio_livraria,
                'url_produto': f'https://www.livrariaonline.pt/produto/{isbn_slug}'
            }
        )
        
        contador_actualizados += 1
        print(f"✓ {livro.titulo}")
        print(f"  Base: {precio_base:.2f}€")
        print(f"  Amazon: {precio_amazon:.2f}€ | FNAC: {precio_fnac:.2f}€ | Livraria: {precio_livraria:.2f}€")
    
    print("\n" + "="*60)
    print(f"✓ Proceso completado!")
    print(f"  - Libros actualizados: {contador_actualizados}")
    print(f"  - Libros que ya tenían múltiples precios: {contador_ya_tienen}")
    print(f"  - Total de precios en BD: {Preco.objects.count()}")

if __name__ == '__main__':
    print("Agregando precios de otras tiendas para todos los libros...")
    print("="*60)
    agregar_precos_para_todos_los_libros()
