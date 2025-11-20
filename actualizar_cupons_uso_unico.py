#!/usr/bin/env python
"""
Script para actualizar TODOS los cupones a UN SOLO USO
Los cupones deben ser exclusivos y secretos
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Cupom

def actualizar_cupons():
    # Actualizar todos los cupones existentes
    cupons_actualizados = Cupom.objects.all().update(
        uso_maximo=1,
        uso_por_utilizador=1
    )
    
    print(f"✅ Actualizados {cupons_actualizados} cupones")
    print("\n📋 Cupones después de la actualización:")
    print("-" * 80)
    
    for cupom in Cupom.objects.all():
        print(f"Código: {cupom.codigo}")
        print(f"  - Uso máximo: {cupom.uso_maximo}")
        print(f"  - Uso por utilizador: {cupom.uso_por_utilizador}")
        print(f"  - Veces usado: {cupom.vezes_usado}")
        print(f"  - Estado: {'✓ Disponible' if cupom.vezes_usado < cupom.uso_maximo else '✗ Agotado'}")
        print()

if __name__ == '__main__':
    actualizar_cupons()
