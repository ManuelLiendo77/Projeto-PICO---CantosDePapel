"""
Sistema de emails para Cantos de Papel
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.translation import gettext as _


def enviar_email_confirmacao_pedido(pedido):
    """Envia email de confirmação quando uma encomenda é criada."""
    subject = _('Confirmação da encomenda #{id} - Cantos de Papel').format(id=pedido.id)
    
    # Contexto para la plantilla
    context = {
        'pedido': pedido,
        'user': pedido.utilizador,
        'items': pedido.itens.all(),
    }
    
    # Renderizar plantilla HTML
    html_message = render_to_string('emails/confirmacao_pedido.html', context)
    plain_message = strip_tags(html_message)
    
    # Enviar email
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[pedido.email],
        html_message=html_message,
        fail_silently=False,
    )
    
    return True


def enviar_email_pedido_enviado(pedido):
    """Envia email quando a encomenda é expedida."""
    subject = _('A sua encomenda #{id} foi enviada - Cantos de Papel').format(id=pedido.id)
    
    context = {
        'pedido': pedido,
        'user': pedido.utilizador,
    }
    
    html_message = render_to_string('emails/pedido_enviado.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[pedido.email],
        html_message=html_message,
        fail_silently=False,
    )
    
    return True


def enviar_email_boas_vindas(user):
    """Envia email de boas-vindas quando um utilizador se regista."""
    subject = _('Bem-vindo(a) à Cantos de Papel! 📚')
    
    context = {
        'user': user,
    }
    
    html_message = render_to_string('emails/boas_vindas.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )
    
    return True


def enviar_email_recuperacao_password(user, reset_url):
    """Envia email para recuperação de palavra-passe."""
    subject = _('Recuperação de palavra-passe - Cantos de Papel')
    
    context = {
        'user': user,
        'reset_url': reset_url,
    }
    
    html_message = render_to_string('emails/recuperacao_password.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )
    
    return True
