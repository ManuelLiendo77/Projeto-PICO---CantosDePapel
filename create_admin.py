import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livraria.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Eliminar usuario si ya existe
if User.objects.filter(username='manuelvalenteliendo77@gmail.com').exists():
    User.objects.filter(username='manuelvalenteliendo77@gmail.com').delete()
    print("Usuario anterior eliminado.")

# Crear nuevo superusuario
user = User.objects.create_user(
    username='manuelvalenteliendo77@gmail.com',
    email='manuelvalenteliendo77@gmail.com',
    password='demon1220'
)
user.is_superuser = True
user.is_staff = True
user.save()

print(f"✓ Superusuario creado exitosamente!")
print(f"Email: {user.email}")
print(f"Username: {user.username}")
print(f"Contraseña: demon1220")
