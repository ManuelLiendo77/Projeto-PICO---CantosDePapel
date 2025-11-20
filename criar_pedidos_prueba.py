"""
Script para crear pedidos de prueba en el sistema
"""
import os
import django
import random
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from django.contrib.auth.models import User
from members.models import Livro, Pedido, ItemPedido

def crear_pedidos_prueba():
    # Obtener usuario admin (o crear uno de prueba)
    try:
        usuario = User.objects.get(username='manuel')
    except User.DoesNotExist:
        # Intentar con el primer usuario que no sea superuser
        usuario = User.objects.filter(is_superuser=False).first()
        if not usuario:
            print("⚠️ No hay usuarios regulares. Crea uno primero con: python manage.py createsuperuser")
            return
    
    # Obtener algunos libros aleatorios
    libros = list(Livro.objects.all().order_by('?')[:20])
    
    if not libros:
        print("⚠️ No hay libros en la base de datos")
        return
    
    # Estados posibles
    estados = ['pendente', 'processando', 'enviado', 'entregue', 'cancelado']
    
    # Direcciones de prueba
    direcciones = [
        {
            'nome': 'Manuel Silva',
            'email': 'manuel@example.com',
            'telefone': '+351 912345678',
            'morada': 'Rua da Liberdade, 123, 4º Andar',
            'cidade': 'Lisboa',
            'codigo_postal': '1250-142',
        },
        {
            'nome': 'João Santos',
            'email': 'joao@example.com',
            'telefone': '+351 923456789',
            'morada': 'Avenida dos Aliados, 456',
            'cidade': 'Porto',
            'codigo_postal': '4000-064',
        },
        {
            'nome': 'Maria Costa',
            'email': 'maria@example.com',
            'telefone': '+351 934567890',
            'morada': 'Rua do Comércio, 789, Apto 2B',
            'cidade': 'Coimbra',
            'codigo_postal': '3000-086',
        },
    ]
    
    # Crear 10 pedidos de prueba
    pedidos_creados = 0
    
    for i in range(10):
        # Seleccionar estado aleatorio
        status = random.choice(estados)
        
        # Seleccionar dirección aleatoria
        direccion = random.choice(direcciones)
        
        # Seleccionar entre 1 y 5 libros diferentes
        num_items = random.randint(1, 5)
        libros_pedido = random.sample(libros, min(num_items, len(libros)))
        
        # Calcular total
        subtotal = Decimal('0.00')
        items_info = []
        
        for livro in libros_pedido:
            # Precio aleatorio entre 9.99 y 29.99
            precio = Decimal(str(random.choice([9.99, 12.99, 14.99, 19.99, 24.99, 29.99])))
            cantidad = random.randint(1, 3)
            item_subtotal = precio * cantidad
            subtotal += item_subtotal
            
            items_info.append({
                'livro': livro,
                'precio': precio,
                'cantidad': cantidad,
                'subtotal': item_subtotal
            })
        
        # Calcular IVA (23%)
        iva = subtotal * Decimal('0.23')
        total = subtotal + iva
        
        # Crear el pedido
        pedido = Pedido.objects.create(
            utilizador=usuario,
            status=status,
            subtotal=subtotal,
            iva=iva,
            total=total,
            nome_completo=direccion['nome'],
            email=direccion['email'],
            telefone=direccion['telefone'],
            morada=direccion['morada'],
            cidade=direccion['cidade'],
            codigo_postal=direccion['codigo_postal'],
            pais='Portugal'
        )
        
        # Crear los items del pedido
        for item_info in items_info:
            ItemPedido.objects.create(
                pedido=pedido,
                livro=item_info['livro'],
                quantidade=item_info['cantidad'],
                preco_unitario=item_info['precio']
            )
        
        pedidos_creados += 1
        print(f"✓ Pedido #{pedido.id} creado - {status} - {len(items_info)} artículos - {total:.2f}€")
    
    print(f"\n✅ {pedidos_creados} pedidos de prueba creados exitosamente para {usuario.username}!")
    print(f"📍 Visita /perfil/ para ver tus pedidos")

if __name__ == '__main__':
    crear_pedidos_prueba()
