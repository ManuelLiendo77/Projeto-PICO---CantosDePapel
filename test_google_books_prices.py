import requests
import json

# Probar con un libro conocido
response = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:9780451524935')  # 1984
data = response.json()

if data.get('totalItems', 0) > 0:
    item = data['items'][0]
    volume_info = item.get('volumeInfo', {})
    sale_info = item.get('saleInfo', {})
    
    print("=" * 60)
    print("LIBRO:", volume_info.get('title'))
    print("=" * 60)
    print("\nINFORMACIÓN DE VENTA (saleInfo):")
    print(json.dumps(sale_info, indent=2))
    
    print("\n" + "=" * 60)
    print("DATOS DISPONIBLES:")
    print("=" * 60)
    print(f"- Título: {volume_info.get('title')}")
    print(f"- Autor: {', '.join(volume_info.get('authors', []))}")
    print(f"- País: {sale_info.get('country')}")
    print(f"- Disponible para venta: {sale_info.get('saleability')}")
    
    if sale_info.get('listPrice'):
        print(f"- Precio de lista: {sale_info['listPrice'].get('amount')} {sale_info['listPrice'].get('currencyCode')}")
    
    if sale_info.get('retailPrice'):
        print(f"- Precio de venta: {sale_info['retailPrice'].get('amount')} {sale_info['retailPrice'].get('currencyCode')}")
else:
    print("No se encontró el libro")
