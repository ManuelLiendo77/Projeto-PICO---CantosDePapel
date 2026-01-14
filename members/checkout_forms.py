from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class CheckoutForm(forms.Form):
    # Dados pessoais
    nome_completo = forms.CharField(
        max_length=255,
        label=_('Nome completo'),
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'O seu nome completo'
        })
    )
    
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'seu@email.com'
        })
    )
    
    telefone = forms.CharField(
        max_length=20,
        label=_('Telefone'),
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '+351 912 345 678'
        })
    )
    
    # Morada de envio
    morada = forms.CharField(
        max_length=255,
        label=_('Morada'),
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Rua, número, piso'
        })
    )
    
    cidade = forms.CharField(
        max_length=100,
        label=_('Cidade'),
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Lisboa'
        })
    )
    
    codigo_postal = forms.CharField(
        max_length=10,
        label=_('Código postal'),
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '1000-001'
        })
    )
    
    pais = forms.CharField(
        max_length=50,
        initial='Portugal',
        label=_('País'),
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'readonly': 'readonly'
        })
    )
    
    # Notas adicionais
    notas = forms.CharField(
        required=False,
        label=_('Notas do pedido (opcional)'),
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Instruções especiais para a entrega...',
            'rows': 3
        })
    )
    
    # Método de pagamento
    METODOS_PAGO = [
        ('mbway', _('MB Way')),
        ('multibanco', _('Multibanco')),
        ('cartao', _('Cartão de crédito/débito')),
        ('paypal', _('PayPal')),
    ]
    
    metodo_pago = forms.ChoiceField(
        choices=METODOS_PAGO,
        required=False,  # Opcional ya que PayPal se procesa aparte
        widget=forms.RadioSelect(attrs={
            'class': 'form-radio'
        }),
        label=_('Método de pagamento')
    )
    
    # Aceitar termos
    aceitar_termos = forms.BooleanField(
        required=True,
        label=_('Aceito os termos e condições'),
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox'
        })
    )
