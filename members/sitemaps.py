from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Livro

class LivroSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Livro.objects.all()

    def lastmod(self, obj):
        # Retorna a data de última modificação se existir
        return None
    
    def location(self, obj):
        return reverse('livro_detalhe', args=[obj.id])


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return [
            'pagina_principal',
            'lista_livros',
            'politica_privacidad',
            'terminos_condiciones',
            'politica_cookies',
        ]

    def location(self, item):
        return reverse(item)
