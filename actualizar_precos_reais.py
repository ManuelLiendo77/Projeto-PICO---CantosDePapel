import os
import django
import requests
import time
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Livro, Preco, Loja

def obtener_precio_real_google_books(livro):
    """
    Obtiene el precio real de Google Books API
    """
    # Intentar buscar por ISBN primero
    if livro.isbn and livro.isbn != 'N/A' and not livro.isbn.startswith('9999'):
        query = f"isbn:{livro.isbn}"
    else:
        # Si no hay ISBN válido, buscar por título y autor
        titulo = livro.titulo.replace(' ', '+')
        autor = livro.autor.replace(' ', '+') if livro.autor else ''
        query = f"{titulo}+inauthor:{autor}" if autor else titulo
    
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&country=PT"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            if data.get('totalItems', 0) > 0:
                item = data['items'][0]
                sale_info = item.get('saleInfo', {})
                
                # Intentar obtener el precio de venta (retail price)
                if sale_info.get('retailPrice'):
                    precio = sale_info['retailPrice'].get('amount')
                    moneda = sale_info['retailPrice'].get('currencyCode')
                    
                    if precio and moneda == 'EUR':
                        return Decimal(str(precio))
                
                # Si no hay precio de venta, intentar precio de lista
                if sale_info.get('listPrice'):
                    precio = sale_info['listPrice'].get('amount')
                    moneda = sale_info['listPrice'].get('currencyCode')
                    
                    if precio and moneda == 'EUR':
                        return Decimal(str(precio))
        
        # Pequeña pausa para no saturar la API
        time.sleep(0.5)
        
    except Exception as e:
        print(f"    ⚠️ Error al consultar API: {e}")
    
    return None

def generar_precio_estimado(livro):
    """
    Genera un precio estimado basado en características del libro
    cuando no hay precio disponible en la API
    """
    # Precio base según categoría
    if livro.categoria:
        categoria_lower = livro.categoria.lower()
        if 'fiction' in categoria_lower or 'literature' in categoria_lower:
            base = random.uniform(14.99, 22.99)
        elif 'science' in categoria_lower or 'history' in categoria_lower:
            base = random.uniform(18.99, 27.99)
        elif 'biography' in categoria_lower:
            base = random.uniform(16.99, 24.99)
        else:
            base = random.uniform(15.99, 23.99)
    else:
        base = random.uniform(16.99, 22.99)
    
    # Redondear a .99 o .49
    precio = round(base)
    if random.random() > 0.5:
        precio = precio - 0.01  # X.99
    else:
        precio = precio - 0.51  # X.49
    
    return Decimal(str(round(precio, 2)))

def actualizar_todos_los_precos():
    """
    Actualiza todos los precios de los libros:
    1. Cantos de Papel: precio real de Google Books o estimado
    2. Amazon: 5-12% más barato que Cantos de Papel
    3. FNAC: 2-8% más caro que Cantos de Papel
    """
    cantos_de_papel = Loja.objects.get(nome='Cantos de Papel')
    amazon = Loja.objects.get(nome='Amazon')
    fnac = Loja.objects.get(nome='FNAC')
    
    livros = Livro.objects.all()
    total = livros.count()
    
    print("="*70)
    print("ACTUALIZANDO PRECIOS CON DATOS REALES DE GOOGLE BOOKS API")
    print("="*70)
    print(f"Total de libros: {total}\n")
    
    contador_reales = 0
    contador_estimados = 0
    
    for idx, livro in enumerate(livros, 1):
        print(f"[{idx}/{total}] {livro.titulo[:50]}")
        
        # 1. Obtener precio real de Google Books
        precio_real = obtener_precio_real_google_books(livro)
        
        if precio_real:
            precio_cantos = precio_real
            contador_reales += 1
            print(f"    ✓ Precio real Google Books: {precio_cantos}€")
        else:
            precio_cantos = generar_precio_estimado(livro)
            contador_estimados += 1
            print(f"    📊 Precio estimado: {precio_cantos}€")
        
        # 2. Actualizar precio de Cantos de Papel
        preco_cantos = Preco.objects.filter(livro=livro, loja=cantos_de_papel).first()
        if preco_cantos:
            preco_cantos.preco = precio_cantos
            preco_cantos.save()
        else:
            Preco.objects.create(
                livro=livro,
                loja=cantos_de_papel,
                preco=precio_cantos,
                url_produto=f'https://cantosdepaapel.com/livros/{livro.id}/'
            )
        
        # 3. Calcular precios de Amazon y FNAC basados en el precio real
        # Amazon: 5-12% más barato
        descuento_amazon = random.uniform(0.05, 0.12)
        precio_amazon = float(precio_cantos) * (1 - descuento_amazon)
        precio_amazon = Decimal(str(round(precio_amazon, 2)))
        
        # FNAC: 2-8% más caro
        aumento_fnac = random.uniform(0.02, 0.08)
        precio_fnac = float(precio_cantos) * (1 + aumento_fnac)
        precio_fnac = Decimal(str(round(precio_fnac, 2)))
        
        # 4. Actualizar o crear precios de Amazon
        preco_amazon = Preco.objects.filter(livro=livro, loja=amazon).first()
        if preco_amazon:
            preco_amazon.preco = precio_amazon
            preco_amazon.save()
        else:
            isbn_slug = str(livro.isbn) if livro.isbn else 'no-isbn'
            Preco.objects.create(
                livro=livro,
                loja=amazon,
                preco=precio_amazon,
                url_produto=f'https://www.amazon.es/dp/{isbn_slug}'
            )
        
        # 5. Actualizar o crear precios de FNAC
        preco_fnac = Preco.objects.filter(livro=livro, loja=fnac).first()
        if preco_fnac:
            preco_fnac.preco = precio_fnac
            preco_fnac.save()
        else:
            titulo_slug = livro.titulo.lower().replace(' ', '-').replace(',', '')[:50]
            isbn_slug = str(livro.isbn) if livro.isbn else 'no-isbn'
            Preco.objects.create(
                livro=livro,
                loja=fnac,
                preco=precio_fnac,
                url_produto=f'https://www.fnac.pt/livro/{titulo_slug}/{isbn_slug}'
            )
        
        print(f"    → Amazon: {precio_amazon}€ (-{int(descuento_amazon*100)}%)")
        print(f"    → FNAC: {precio_fnac}€ (+{int(aumento_fnac*100)}%)\n")
    
    print("="*70)
    print("✓ PROCESO COMPLETADO")
    print("="*70)
    print(f"Total de libros procesados: {total}")
    print(f"Precios reales de Google Books: {contador_reales}")
    print(f"Precios estimados: {contador_estimados}")
    print(f"Total de precios en BD: {Preco.objects.count()}")
    print("\n✓ Todos los precios de Cantos de Papel ahora son reales o estimados")
    print("✓ Amazon y FNAC tienen precios basados en los reales con variaciones menores")

if __name__ == '__main__':
    actualizar_todos_los_precos()
