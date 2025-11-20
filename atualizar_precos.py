import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Preco

# Actualizar todos los precios a valores más realistas
precos = Preco.objects.all()

precos_atualizados = 0

for preco in precos:
    # Convertir precios a valores más simples y realistas
    # Redondear a valores como 9.99, 12.99, 14.99, 15.99, 17.99, 19.99, etc.
    
    preco_atual = float(preco.preco)
    
    # Determinar un precio realista basado en el precio actual
    if preco_atual < 10:
        novo_preco = 9.99
    elif preco_atual < 12:
        novo_preco = 11.99
    elif preco_atual < 15:
        novo_preco = 14.99
    elif preco_atual < 18:
        novo_preco = 16.99
    elif preco_atual < 20:
        novo_preco = 19.99
    elif preco_atual < 25:
        novo_preco = 22.99
    else:
        novo_preco = 24.99
    
    preco.preco = novo_preco
    preco.save()
    precos_atualizados += 1
    print(f"✓ Actualizado: {preco.livro.titulo} - {preco.loja.nome}: {preco_atual:.2f}€ → {novo_preco:.2f}€")

print(f"\n✅ {precos_atualizados} preços actualizados com sucesso!")
print("Os preços agora são mais realistas e simples (ex: 9.99€, 14.99€, 19.99€)")
