import os
import django
import requests
import time
import random
from decimal import Decimal
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from members.models import Livro, Preco, Loja

# Lista de libros famosos con películas
LIVROS_COM_FILMES = [
    # Clásicos
    {"titulo": "Pride and Prejudice", "autor": "Jane Austen", "filme": "Pride & Prejudice (2005)"},
    {"titulo": "The Great Gatsby", "autor": "F. Scott Fitzgerald", "filme": "The Great Gatsby (2013)"},
    {"titulo": "To Kill a Mockingbird", "autor": "Harper Lee", "filme": "To Kill a Mockingbird (1962)"},
    {"titulo": "1984", "autor": "George Orwell", "filme": "1984 (1984)"},
    {"titulo": "Animal Farm", "autor": "George Orwell", "filme": "Animal Farm (1954)"},
    {"titulo": "The Lord of the Rings", "autor": "J.R.R. Tolkien", "filme": "The Lord of the Rings Trilogy"},
    {"titulo": "The Hobbit", "autor": "J.R.R. Tolkien", "filme": "The Hobbit Trilogy"},
    {"titulo": "Harry Potter and the Philosopher's Stone", "autor": "J.K. Rowling", "filme": "Harry Potter (2001)"},
    {"titulo": "The Chronicles of Narnia", "autor": "C.S. Lewis", "filme": "The Chronicles of Narnia (2005)"},
    {"titulo": "Gone with the Wind", "autor": "Margaret Mitchell", "filme": "Gone with the Wind (1939)"},
    
    # Ficción contemporánea
    {"titulo": "The Hunger Games", "autor": "Suzanne Collins", "filme": "The Hunger Games (2012)"},
    {"titulo": "Twilight", "autor": "Stephenie Meyer", "filme": "Twilight (2008)"},
    {"titulo": "The Fault in Our Stars", "autor": "John Green", "filme": "The Fault in Our Stars (2014)"},
    {"titulo": "Life of Pi", "autor": "Yann Martel", "filme": "Life of Pi (2012)"},
    {"titulo": "The Help", "autor": "Kathryn Stockett", "filme": "The Help (2011)"},
    {"titulo": "The Book Thief", "autor": "Markus Zusak", "filme": "The Book Thief (2013)"},
    {"titulo": "Water for Elephants", "autor": "Sara Gruen", "filme": "Water for Elephants (2011)"},
    {"titulo": "Me Before You", "autor": "Jojo Moyes", "filme": "Me Before You (2016)"},
    {"titulo": "The Notebook", "autor": "Nicholas Sparks", "filme": "The Notebook (2004)"},
    {"titulo": "A Walk to Remember", "autor": "Nicholas Sparks", "filme": "A Walk to Remember (2002)"},
    
    # Thriller y Misterio
    {"titulo": "Gone Girl", "autor": "Gillian Flynn", "filme": "Gone Girl (2014)"},
    {"titulo": "The Girl with the Dragon Tattoo", "autor": "Stieg Larsson", "filme": "The Girl with the Dragon Tattoo (2011)"},
    {"titulo": "The Da Vinci Code", "autor": "Dan Brown", "filme": "The Da Vinci Code (2006)"},
    {"titulo": "Angels and Demons", "autor": "Dan Brown", "filme": "Angels & Demons (2009)"},
    {"titulo": "The Silence of the Lambs", "autor": "Thomas Harris", "filme": "The Silence of the Lambs (1991)"},
    {"titulo": "Mystic River", "autor": "Dennis Lehane", "filme": "Mystic River (2003)"},
    {"titulo": "Shutter Island", "autor": "Dennis Lehane", "filme": "Shutter Island (2010)"},
    
    # Ciencia Ficción
    {"titulo": "Dune", "autor": "Frank Herbert", "filme": "Dune (2021)"},
    {"titulo": "The Martian", "autor": "Andy Weir", "filme": "The Martian (2015)"},
    {"titulo": "Jurassic Park", "autor": "Michael Crichton", "filme": "Jurassic Park (1993)"},
    {"titulo": "A Clockwork Orange", "autor": "Anthony Burgess", "filme": "A Clockwork Orange (1971)"},
    {"titulo": "Blade Runner", "autor": "Philip K. Dick", "filme": "Blade Runner (1982)"},
    {"titulo": "The Time Machine", "autor": "H.G. Wells", "filme": "The Time Machine (2002)"},
    {"titulo": "War of the Worlds", "autor": "H.G. Wells", "filme": "War of the Worlds (2005)"},
    
    # Drama y Históricos
    {"titulo": "The Remains of the Day", "autor": "Kazuo Ishiguro", "filme": "The Remains of the Day (1993)"},
    {"titulo": "Atonement", "autor": "Ian McEwan", "filme": "Atonement (2007)"},
    {"titulo": "Brooklyn", "autor": "Colm Tóibín", "filme": "Brooklyn (2015)"},
    {"titulo": "The English Patient", "autor": "Michael Ondaatje", "filme": "The English Patient (1996)"},
    {"titulo": "Cold Mountain", "autor": "Charles Frazier", "filme": "Cold Mountain (2003)"},
    {"titulo": "The Reader", "autor": "Bernhard Schlink", "filme": "The Reader (2008)"},
    
    # Terror
    {"titulo": "The Shining", "autor": "Stephen King", "filme": "The Shining (1980)"},
    {"titulo": "It", "autor": "Stephen King", "filme": "It (2017)"},
    {"titulo": "Carrie", "autor": "Stephen King", "filme": "Carrie (1976)"},
    {"titulo": "The Green Mile", "autor": "Stephen King", "filme": "The Green Mile (1999)"},
    {"titulo": "Misery", "autor": "Stephen King", "filme": "Misery (1990)"},
    
    # Biografías y Basados en hechos reales
    {"titulo": "The Blind Side", "autor": "Michael Lewis", "filme": "The Blind Side (2009)"},
    {"titulo": "Moneyball", "autor": "Michael Lewis", "filme": "Moneyball (2011)"},
    {"titulo": "Into the Wild", "autor": "Jon Krakauer", "filme": "Into the Wild (2007)"},
    {"titulo": "Wild", "autor": "Cheryl Strayed", "filme": "Wild (2014)"},
    {"titulo": "Eat Pray Love", "autor": "Elizabeth Gilbert", "filme": "Eat Pray Love (2010)"},
    
    # Otros
    {"titulo": "Forrest Gump", "autor": "Winston Groom", "filme": "Forrest Gump (1994)"},
    {"titulo": "The Perks of Being a Wallflower", "autor": "Stephen Chbosky", "filme": "The Perks of Being a Wallflower (2012)"},
    {"titulo": "Charlie and the Chocolate Factory", "autor": "Roald Dahl", "filme": "Charlie and the Chocolate Factory (2005)"},
    {"titulo": "Matilda", "autor": "Roald Dahl", "filme": "Matilda (1996)"},
]

def buscar_livro_google(titulo, autor):
    """Busca un libro en Google Books API"""
    query = f"{titulo} {autor}".replace(" ", "+")
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&langRestrict=pt&maxResults=1"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('totalItems', 0) > 0:
                return data['items'][0]
    except Exception as e:
        print(f"  ⚠️  Erro ao buscar {titulo}: {e}")
    
    return None

def extrair_info_livro(item, filme_info):
    """Extrae información del libro desde Google Books"""
    volume_info = item.get('volumeInfo', {})
    
    info = {
        'titulo': volume_info.get('title', ''),
        'autor': ', '.join(volume_info.get('authors', [])) if volume_info.get('authors') else '',
        'isbn': None,
        'editora': volume_info.get('publisher', ''),
        'data_publicacao': volume_info.get('publishedDate', ''),
        'numero_paginas': volume_info.get('pageCount'),
        'idioma': volume_info.get('language', 'pt'),
        'descricao': volume_info.get('description', ''),
        'imagem_capa': None,
        'categoria': ', '.join(volume_info.get('categories', [])) if volume_info.get('categories') else 'Ficção',
        'filme': filme_info
    }
    
    # Extraer ISBN
    for identifier in volume_info.get('industryIdentifiers', []):
        if identifier['type'] in ['ISBN_13', 'ISBN_10']:
            info['isbn'] = identifier['identifier']
            break
    
    # Extraer imagen de capa (usar la de mejor calidad)
    image_links = volume_info.get('imageLinks', {})
    if 'large' in image_links:
        info['imagem_capa'] = image_links['large'].replace('http://', 'https://')
    elif 'medium' in image_links:
        info['imagem_capa'] = image_links['medium'].replace('http://', 'https://')
    elif 'thumbnail' in image_links:
        info['imagem_capa'] = image_links['thumbnail'].replace('http://', 'https://')
    
    return info

def criar_livro(info):
    """Cria ou atualiza un libro en la base de datos"""
    try:
        # Verificar si ya existe
        if info['isbn']:
            livro_existente = Livro.objects.filter(isbn=info['isbn']).first()
            if livro_existente:
                print(f"  ℹ️  Livro já existe: {info['titulo']}")
                # Actualizar para indicar que tiene película
                if not livro_existente.tem_filme:
                    livro_existente.tem_filme = True
                    livro_existente.save()
                    print(f"  ✓ Atualizado para tem_filme=True")
                return livro_existente
        
        # Si no tiene ISBN, generar uno falso único
        if not info['isbn']:
            info['isbn'] = f"9999{random.randint(100000000, 999999999)}"
        
        # Parsear fecha de publicación
        data_pub = None
        if info['data_publicacao']:
            try:
                if len(info['data_publicacao']) == 4:  # Solo año
                    data_pub = f"{info['data_publicacao']}-01-01"
                elif len(info['data_publicacao']) == 7:  # Año-Mes
                    data_pub = f"{info['data_publicacao']}-01"
                else:
                    data_pub = info['data_publicacao']
            except:
                pass
        
        # Crear nuevo libro
        livro = Livro.objects.create(
            titulo=info['titulo'][:255],
            autor=info['autor'][:255],
            isbn=info['isbn'][:13],
            descricao=info['descricao'][:5000] if info['descricao'] else f"📖 {info['titulo']} por {info['autor']}\n\n🎬 Adaptado para cinema: {info['filme']}",
            imagem_capa=info['imagem_capa'],
            categoria=info['categoria'][:100],
            tem_filme=True,
            data_publicacao=data_pub,
            stock=random.randint(5, 30),
            novidade=True
        )
        
        # Obtener o crear loja
        loja, _ = Loja.objects.get_or_create(
            nome='Cantos de Papel',
            defaults={'url': 'https://cantosdepaapel.com'}
        )
        
        # Crear precio
        preco_base = Decimal('12.99') + (Decimal(random.randint(0, 20)) * Decimal('0.50'))
        Preco.objects.create(
            livro=livro,
            loja=loja,
            preco=preco_base,
            url_produto=f'https://cantosdepaapel.com/livro/{livro.id}'
        )
        
        print(f"  ✓ Criado: {info['titulo']} - {info['autor']}")
        print(f"     🎬 Filme: {info['filme']}")
        return livro
        
    except Exception as e:
        print(f"  ❌ Erro ao criar {info['titulo']}: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("\n" + "="*80)
    print("🎬 IMPORTAÇÃO DE LIVROS COM FILMES - Google Books API")
    print("="*80 + "\n")
    
    livros_criados = 0
    livros_existentes = 0
    erros = 0
    
    total = len(LIVROS_COM_FILMES)
    
    for idx, livro_info in enumerate(LIVROS_COM_FILMES, 1):
        print(f"\n[{idx}/{total}] Buscando: {livro_info['titulo']} - {livro_info['autor']}")
        
        # Buscar en Google Books
        item = buscar_livro_google(livro_info['titulo'], livro_info['autor'])
        
        if item:
            info = extrair_info_livro(item, livro_info['filme'])
            livro = criar_livro(info)
            
            if livro:
                if Livro.objects.filter(isbn=info['isbn']).count() == 1:
                    livros_criados += 1
                else:
                    livros_existentes += 1
            else:
                erros += 1
        else:
            print(f"  ❌ Não encontrado na API do Google Books")
            erros += 1
        
        # Delay para não sobrecargar la API
        time.sleep(0.5)
    
    # Resumen
    print("\n" + "="*80)
    print("📊 RESUMO DA IMPORTAÇÃO")
    print("="*80)
    print(f"✓ Livros criados: {livros_criados}")
    print(f"ℹ️  Livros já existentes: {livros_existentes}")
    print(f"❌ Erros: {erros}")
    print(f"📚 Total processado: {total}")
    print(f"🎬 Todos os livros têm filmes associados!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
