# Template tags personalizados para Cantos de Papel
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter para acessar itens de dicionário por chave.
    Uso: {{ meu_dict|get_item:chave }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)
