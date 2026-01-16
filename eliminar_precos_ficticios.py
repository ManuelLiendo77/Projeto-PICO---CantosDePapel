import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Preco, Loja

def eliminar_precos_ficticios():
    """
    Elimina todos los precios de tiendas externas (Amazon, FNAC, Livraria Online)
    y elimina la tienda ficticia "Livraria Online".
    Solo deja los precios reales de "Cantos de Papel".
    """
    
    # Obtener las tiendas a eliminar
    try:
        livraria_online = Loja.objects.get(nome='Livraria Online')
        amazon = Loja.objects.get(nome='Amazon')
        fnac = Loja.objects.get(nome='FNAC')
        
        # Contar precios antes
        precos_livraria = Preco.objects.filter(loja=livraria_online).count()
        precos_amazon = Preco.objects.filter(loja=amazon).count()
        precos_fnac = Preco.objects.filter(loja=fnac).count()
        
        print("Eliminando precios ficticios...")
        print("="*60)
        print(f"Livraria Online: {precos_livraria} precios")
        print(f"Amazon: {precos_amazon} precios")
        print(f"FNAC: {precos_fnac} precios")
        print(f"Total a eliminar: {precos_livraria + precos_amazon + precos_fnac} precios")
        print()
        
        # Eliminar precios
        Preco.objects.filter(loja=livraria_online).delete()
        print(f"✓ Eliminados {precos_livraria} precios de Livraria Online")
        
        Preco.objects.filter(loja=amazon).delete()
        print(f"✓ Eliminados {precos_amazon} precios de Amazon")
        
        Preco.objects.filter(loja=fnac).delete()
        print(f"✓ Eliminados {precos_fnac} precios de FNAC")
        
        # Eliminar las tiendas (excepto Cantos de Papel)
        livraria_online.delete()
        print(f"✓ Eliminada tienda: Livraria Online")
        
        amazon.delete()
        print(f"✓ Eliminada tienda: Amazon")
        
        fnac.delete()
        print(f"✓ Eliminada tienda: FNAC")
        
        print()
        print("="*60)
        print("✓ Proceso completado!")
        print(f"  - Precios restantes en BD: {Preco.objects.count()}")
        print(f"  - Tiendas restantes: {Loja.objects.count()}")
        print()
        print("Ahora solo existen precios reales de 'Cantos de Papel'")
        print("Para comparar precios con otras tiendas necesitarás:")
        print("  1. Implementar web scraping de tiendas reales")
        print("  2. Usar APIs oficiales de tiendas (si existen)")
        print("  3. Actualizar manualmente los precios de otras tiendas")
        
    except Loja.DoesNotExist as e:
        print(f"Error: No se encontró la tienda: {e}")

if __name__ == '__main__':
    eliminar_precos_ficticios()
