import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Filme
import re

print("\n" + "="*80)
print("🔧 CORRIGIENDO URLs DE TRAILERS")
print("="*80 + "\n")

filmes = Filme.objects.all()
total = filmes.count()
corrigidos = 0

for filme in filmes:
    if filme.trailer_url:
        # Extraer el video ID de la URL actual
        match = re.search(r'(?:embed/|watch\?v=)([a-zA-Z0-9_-]{11})', filme.trailer_url)
        
        if match:
            video_id = match.group(1)
            
            # Crear nueva URL con parámetros que mejoran compatibilidad
            # origin permite que YouTube sepa de dónde viene el embed
            # rel=0 reduce videos relacionados
            # modestbranding=1 reduce branding de YouTube
            # fs=1 permite pantalla completa
            nova_url = f"https://www.youtube-nocookie.com/embed/{video_id}?rel=0&modestbranding=1&autoplay=0&fs=1&enablejsapi=1"
            
            if filme.trailer_url != nova_url:
                print(f"📚 {filme.titulo}")
                print(f"   Antes: {filme.trailer_url}")
                print(f"   Depois: {nova_url}")
                
                filme.trailer_url = nova_url
                filme.save()
                corrigidos += 1
                print("   ✓ Corrigido\n")

print("="*80)
print(f"✓ URLs corrigidas: {corrigidos}/{total}")
print("="*80 + "\n")
