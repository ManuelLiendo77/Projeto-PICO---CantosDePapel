from django.core.management.base import BaseCommand
from members.models import Livro, Preco, Loja
import requests
import time
import random

class Command(BaseCommand):
    help = 'Importa livros desde Google Books API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--query',
            type=str,
            default='bestsellers',
            help='Término de búsqueda (default: bestsellers)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=20,
            help='Número de libros a importar (default: 20, max: 40)'
        )

    def handle(self, *args, **options):
        query = options['query']
        limit = min(options['limit'], 40)  # Google Books retorna max 40 por request
        
        self.stdout.write(self.style.WARNING(f'🔍 Buscando libros: "{query}"...'))
        
        # URL de Google Books API
        url = f'https://www.googleapis.com/books/v1/volumes'
        params = {
            'q': query,
            'maxResults': limit,
            'langRestrict': 'pt',  # Libros en portugués
            'orderBy': 'relevance'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'items' not in data:
                self.stdout.write(self.style.ERROR('❌ No se encontraron libros'))
                return
            
            items = data['items']
            importados = 0
            
            # Crear lojas si no existen
            loja_principal, _ = Loja.objects.get_or_create(
                nome='Livraria Online',
                defaults={'url': 'https://example.com'}
            )
            loja_amazon, _ = Loja.objects.get_or_create(
                nome='Amazon',
                defaults={'url': 'https://amazon.com'}
            )
            loja_fnac, _ = Loja.objects.get_or_create(
                nome='FNAC',
                defaults={'url': 'https://fnac.pt'}
            )
            
            lojas = [loja_principal, loja_amazon, loja_fnac]
            
            self.stdout.write(self.style.SUCCESS(f'📚 Procesando {len(items)} libros...'))
            
            for item in items:
                try:
                    volume_info = item.get('volumeInfo', {})
                    
                    # Extraer información
                    titulo = volume_info.get('title', 'Sin título')
                    autores = volume_info.get('authors', ['Desconocido'])
                    autor = ', '.join(autores)
                    
                    # ISBN
                    isbn = None
                    for identifier in volume_info.get('industryIdentifiers', []):
                        if identifier['type'] in ['ISBN_13', 'ISBN_10']:
                            isbn = identifier['identifier']
                            break
                    
                    if not isbn:
                        isbn = f'NO-ISBN-{random.randint(100000, 999999)}'
                    
                    # Descripción
                    descricao = volume_info.get('description', 'Sin descripción disponible')
                    if len(descricao) > 500:
                        descricao = descricao[:497] + '...'
                    
                    # Imagen de portada
                    image_links = volume_info.get('imageLinks', {})
                    imagem_capa = (
                        image_links.get('thumbnail', '') or 
                        image_links.get('smallThumbnail', '')
                    )
                    
                    # Categoría
                    categorias = volume_info.get('categories', ['Livros'])
                    categoria = categorias[0] if categorias else 'Livros'
                    
                    # Verificar si ya existe (por ISBN)
                    if Livro.objects.filter(isbn=isbn).exists():
                        self.stdout.write(f'⏭️  Ya existe: {titulo}')
                        continue
                    
                    # Crear libro
                    livro = Livro.objects.create(
                        titulo=titulo,
                        autor=autor,
                        isbn=isbn,
                        descricao=descricao,
                        imagem_capa=imagem_capa,
                        categoria=categoria,
                        novidade=random.choice([True, False]),
                        tem_filme=False
                    )
                    
                    # Crear precios aleatorios para diferentes lojas
                    preco_base = random.uniform(9.99, 29.99)
                    
                    for loja in lojas:
                        variacao = random.uniform(-3, 5)
                        preco_final = round(max(preco_base + variacao, 5.99), 2)
                        
                        Preco.objects.create(
                            livro=livro,
                            loja=loja,
                            preco=preco_final
                        )
                    
                    importados += 1
                    self.stdout.write(self.style.SUCCESS(f'✅ Importado: {titulo} ({isbn})'))
                    
                    # Pequeña pausa para no saturar la API
                    time.sleep(0.2)
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'❌ Error procesando libro: {str(e)}'))
                    continue
            
            self.stdout.write(self.style.SUCCESS(f'\n🎉 ¡Importación completada!'))
            self.stdout.write(self.style.SUCCESS(f'📊 Total importados: {importados}/{len(items)}'))
            
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'❌ Error de conexión: {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error inesperado: {str(e)}'))
