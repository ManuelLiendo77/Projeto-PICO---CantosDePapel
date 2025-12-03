import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Filme

# Ver las primeras 5 URLs
print("\n" + "="*80)
print("🔍 VERIFICANDO URLs DOS TRAILERS")
print("="*80 + "\n")

filmes = Filme.objects.all()[:5]

for filme in filmes:
    print(f"📚 {filme.titulo}")
    print(f"   URL: {filme.trailer_url}")
    print()

print(f"\nTotal de filmes: {Filme.objects.count()}")
