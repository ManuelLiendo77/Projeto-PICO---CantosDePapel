import os
import django
import random
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Livro

# Obtener todos los libros con stock
livros_com_stock = list(Livro.objects.filter(stock__gt=0))

print(f"\n📚 Total de livros com stock: {len(livros_com_stock)}")

# 1. CONFIGURAR OFERTAS (10-15 libros aleatorios)
num_ofertas = min(random.randint(10, 15), len(livros_com_stock))
livros_oferta = random.sample(livros_com_stock, num_ofertas)

print(f"\n🎁 Configurando {num_ofertas} livros em oferta...")
for livro in livros_oferta:
    livro.em_oferta = True
    livro.desconto_percentagem = random.choice([10, 15, 20, 25, 30])
    livro.save()
    print(f"   ✓ {livro.titulo[:50]} - {livro.desconto_percentagem}% desconto")

# 2. CONFIGURAR MAIS VENDIDOS (13 libros aleatorios)
print(f"\n⭐ Configurando 13 livros como mais vendidos...")
num_vendidos = min(13, len(livros_com_stock))
livros_vendidos = random.sample(livros_com_stock, num_vendidos)

for livro in livros_vendidos:
    livro.mais_vendido = True
    livro.vendas_totais = random.randint(50, 500)  # Simular ventas
    livro.save()
    print(f"   ✓ {livro.titulo[:50]} - {livro.vendas_totais} vendas")

# 3. CONFIGURAR DATAS DE PUBLICAÇÃO (para novidades)
print(f"\n📅 Configurando datas de publicação...")
ano_atual = date.today().year
for livro in Livro.objects.all():
    if not livro.data_publicacao:
        # Asignar fecha aleatoria entre 2020 y 2025
        ano = random.randint(2020, ano_atual)
        mes = random.randint(1, 12)
        dia = random.randint(1, 28)
        livro.data_publicacao = date(ano, mes, dia)
        livro.save()

# Marcar como novidades los libros del año actual
novidades = Livro.objects.filter(data_publicacao__year=ano_atual).update(novidade=True)
print(f"   ✓ {novidades} livros marcados como novidades ({ano_atual})")

print("\n✅ Configuração concluída!")
print(f"\n📊 Resumo:")
print(f"   🎁 Ofertas: {Livro.objects.filter(em_oferta=True).count()} livros")
print(f"   ⭐ Mais Vendidos: {Livro.objects.filter(mais_vendido=True).count()} livros")
print(f"   🍁 Novidades: {Livro.objects.filter(novidade=True).count()} livros")
