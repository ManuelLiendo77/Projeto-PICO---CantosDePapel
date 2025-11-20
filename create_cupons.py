import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Cupom
from django.utils import timezone

print("Criando cupons de exemplo...")
print("=" * 60)

# Cupom 1: Desconto de 10% - Válido por 30 dias
cupom1, created = Cupom.objects.get_or_create(
    codigo='OUTONO2025',
    defaults={
        'descricao': 'Desconto de 10% para o outono - Válido em compras acima de €20',
        'tipo_desconto': 'percentagem',
        'valor': 10.00,
        'data_inicio': timezone.now(),
        'data_fim': timezone.now() + timedelta(days=30),
        'ativo': True,
        'uso_maximo': 100,
        'uso_por_utilizador': 3,
        'valor_minimo_pedido': 20.00,
    }
)
print(f"{'✓ Criado' if created else '⚠ Já existe'}: {cupom1.codigo} - {cupom1.valor}% de desconto")

# Cupom 2: Desconto de 20% - Black Friday (7 dias)
cupom2, created = Cupom.objects.get_or_create(
    codigo='BLACKFRIDAY2025',
    defaults={
        'descricao': 'Super desconto Black Friday - 20% OFF em qualquer compra!',
        'tipo_desconto': 'percentagem',
        'valor': 20.00,
        'data_inicio': timezone.now(),
        'data_fim': timezone.now() + timedelta(days=7),
        'ativo': True,
        'uso_maximo': 500,
        'uso_por_utilizador': 1,
        'valor_minimo_pedido': 0,
    }
)
print(f"{'✓ Criado' if created else '⚠ Já existe'}: {cupom2.codigo} - {cupom2.valor}% de desconto")

# Cupom 3: Desconto fixo de €5 - Primeiro pedido
cupom3, created = Cupom.objects.get_or_create(
    codigo='BEMVINDO5',
    defaults={
        'descricao': 'Desconto de €5 para novos clientes - Primeira compra!',
        'tipo_desconto': 'valor_fixo',
        'valor': 5.00,
        'data_inicio': timezone.now(),
        'data_fim': timezone.now() + timedelta(days=60),
        'ativo': True,
        'uso_maximo': 1000,
        'uso_por_utilizador': 1,
        'valor_minimo_pedido': 15.00,
    }
)
print(f"{'✓ Criado' if created else '⚠ Já existe'}: {cupom3.codigo} - €{cupom3.valor} de desconto")

# Cupom 4: Desconto de 15% - Natal (45 dias)
cupom4, created = Cupom.objects.get_or_create(
    codigo='NATAL2025',
    defaults={
        'descricao': 'Especial de Natal - 15% de desconto em compras acima de €30',
        'tipo_desconto': 'percentagem',
        'valor': 15.00,
        'data_inicio': timezone.now(),
        'data_fim': timezone.now() + timedelta(days=45),
        'ativo': True,
        'uso_maximo': 200,
        'uso_por_utilizador': 2,
        'valor_minimo_pedido': 30.00,
    }
)
print(f"{'✓ Criado' if created else '⚠ Já existe'}: {cupom4.codigo} - {cupom4.valor}% de desconto")

# Cupom 5: Desconto fixo de €10 - Compras grandes
cupom5, created = Cupom.objects.get_or_create(
    codigo='GRANDE10',
    defaults={
        'descricao': 'Desconto de €10 em compras acima de €50',
        'tipo_desconto': 'valor_fixo',
        'valor': 10.00,
        'data_inicio': timezone.now(),
        'data_fim': timezone.now() + timedelta(days=90),
        'ativo': True,
        'uso_maximo': 300,
        'uso_por_utilizador': 5,
        'valor_minimo_pedido': 50.00,
    }
)
print(f"{'✓ Criado' if created else '⚠ Já existe'}: {cupom5.codigo} - €{cupom5.valor} de desconto")

# Cupom 6: Desconto de 25% - VIP (limitado)
cupom6, created = Cupom.objects.get_or_create(
    codigo='VIP25',
    defaults={
        'descricao': 'Cupom VIP exclusivo - 25% OFF (apenas 50 usos!)',
        'tipo_desconto': 'percentagem',
        'valor': 25.00,
        'data_inicio': timezone.now(),
        'data_fim': timezone.now() + timedelta(days=14),
        'ativo': True,
        'uso_maximo': 50,
        'uso_por_utilizador': 1,
        'valor_minimo_pedido': 40.00,
    }
)
print(f"{'✓ Criado' if created else '⚠ Já existe'}: {cupom6.codigo} - {cupom6.valor}% de desconto")

print("\n" + "=" * 60)
print("Cupons criados com sucesso!")
print("\nResumo dos cupons:")
print("-" * 60)

for cupom in Cupom.objects.all().order_by('-valor'):
    tipo = f"{cupom.valor}%" if cupom.tipo_desconto == 'percentagem' else f"€{cupom.valor}"
    validade = "✓ Válido" if cupom.esta_valido() else "✗ Expirado"
    print(f"📌 {cupom.codigo:20} | {tipo:8} | Min: €{cupom.valor_minimo_pedido:5} | {validade}")
