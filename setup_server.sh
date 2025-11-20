#!/bin/bash
# =============================================================================
# Configuração Inicial do Servidor - Livraria Online
# =============================================================================
# Execute este script UMA VEZ após clonar o projeto num servidor novo
# =============================================================================

set -e

echo "🔧 Configurando servidor para Livraria Online..."

# Atualizar sistema
echo "📦 Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependências do sistema
echo "📚 Instalando dependências..."
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git

# Criar ambiente virtual
echo "🐍 Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependências Python
echo "📦 Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

# Configurar PostgreSQL
echo "🗄️  Configurando PostgreSQL..."
sudo -u postgres psql << EOF
CREATE DATABASE livraria_db;
CREATE USER livraria_user WITH PASSWORD 'CHANGE_THIS_PASSWORD';
ALTER ROLE livraria_user SET client_encoding TO 'utf8';
ALTER ROLE livraria_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE livraria_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE livraria_db TO livraria_user;
\q
EOF

# Criar ficheiro .env
echo "⚙️  Criando ficheiro de configuração..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "❗ IMPORTANTE: Edite o ficheiro .env com as suas credenciais!"
fi

# Executar migrações
echo "🗄️  Executando migrações..."
python manage.py migrate

# Criar superuser
echo "👤 Criar superuser (siga as instruções):"
python manage.py createsuperuser

# Coletar ficheiros estáticos
echo "📁 Coletando ficheiros estáticos..."
python manage.py collectstatic --noinput

# Configurar Gunicorn
echo "🔧 Configurando Gunicorn..."
sudo tee /etc/systemd/system/gunicorn.service > /dev/null << EOF
[Unit]
Description=Gunicorn daemon para Livraria Online
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/gunicorn --workers 3 --bind unix:$(pwd)/gunicorn.sock projeto_livraria.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Configurar Nginx
echo "🌐 Configurando Nginx..."
sudo tee /etc/nginx/sites-available/livraria > /dev/null << EOF
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias $(pwd)/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$(pwd)/gunicorn.sock;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/livraria /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Ativar e iniciar serviços
echo "🚀 Ativando serviços..."
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl enable nginx

echo "✅ Configuração concluída!"
echo ""
echo "📝 PRÓXIMOS PASSOS:"
echo "1. Edite o ficheiro .env com as credenciais corretas"
echo "2. Configure o DNS do seu domínio para apontar ao servidor"
echo "3. Configure SSL com Certbot: sudo certbot --nginx -d seu-dominio.com"
echo "4. Reinicie os serviços: sudo systemctl restart gunicorn nginx"
