# 🚀 Guia de Deployment - Livraria Online

## 📋 Índice
1. [Pré-requisitos](#pré-requisitos)
2. [Desenvolvimento Local](#desenvolvimento-local)
3. [Configuração de Produção](#configuração-de-produção)
4. [Deploy em Servidor](#deploy-em-servidor)
5. [Configuração de Email](#configuração-de-email)
6. [SSL/HTTPS](#sslhttps)
7. [Base de Dados](#base-de-dados)
8. [Backup](#backup)
9. [Monitorização](#monitorização)
10. [Troubleshooting](#troubleshooting)

---

## 🔧 Pré-requisitos

### Software Necessário
- **Python 3.11+**
- **pip** (gestor de pacotes Python)
- **PostgreSQL 15+** (para produção)
- **Git** (controlo de versões)
- **Nginx** ou **Apache** (servidor web)
- **Supervisor** ou **systemd** (gestão de processos)

### Pacotes Python
```bash
pip install -r requirements.txt
```

---

## 💻 Desenvolvimento Local

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/livraria-online.git
cd livraria-online
```

### 2. Criar Ambiente Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
```bash
# Copiar template
cp .env.example .env

# Editar .env com suas configurações
# IMPORTANTE: Use DJANGO_ENV=development
```

### 5. Executar Migrações
```bash
cd projeto_livraria
python manage.py makemigrations
python manage.py migrate
```

### 6. Criar Superusuário
```bash
python manage.py createsuperuser
```

### 7. Carregar Dados de Teste (Opcional)
```bash
python manage.py loaddata fixtures/livros.json
```

### 8. Executar Servidor de Desenvolvimento
```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

---

## 🌐 Configuração de Produção

### 1. Variáveis de Ambiente

Crie um ficheiro `.env` em produção:

```bash
DJANGO_ENV=production
SECRET_KEY=gere-uma-chave-secreta-forte-aqui
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
SITE_DOMAIN=seu-dominio.com

# Database
DB_NAME=livraria_db
DB_USER=livraria_user
DB_PASSWORD=senha-forte-aqui
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-aplicacao
```

### 2. Gerar SECRET_KEY Nova
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 3. Configurar PostgreSQL

```bash
# Entrar no PostgreSQL
sudo -u postgres psql

# Criar base de dados e utilizador
CREATE DATABASE livraria_db;
CREATE USER livraria_user WITH PASSWORD 'senha-forte-aqui';
ALTER ROLE livraria_user SET client_encoding TO 'utf8';
ALTER ROLE livraria_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE livraria_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE livraria_db TO livraria_user;
\q
```

### 4. Instalar Adaptador PostgreSQL
```bash
pip install psycopg2-binary
```

### 5. Executar Migrações em Produção
```bash
python manage.py migrate
```

### 6. Coletar Ficheiros Estáticos
```bash
python manage.py collectstatic --noinput
```

### 7. Configurar Nginx para os Estáticos
Garanta que o Nginx aponte para a pasta configurada em `STATIC_ROOT` (por padrão `staticfiles/`).

```nginx
location /static/ {
  alias /caminho/absoluto/para/o/projeto/staticfiles/;
}
```

Usar `alias` evita que o servidor procure os ficheiros na pasta errada (ex.: `members/static`).

### 8. Testar Configuração
```bash
python manage.py check --deploy
```

---

## 📧 Configuração de Email

### Gmail

1. **Ativar Verificação em 2 Etapas:**
   - Aceda a: https://myaccount.google.com/security
   - Ative "Verificação em 2 etapas"

2. **Criar Senha de Aplicação:**
   - Aceda a: https://myaccount.google.com/apppasswords
   - Selecione "Aplicação: Email" e "Dispositivo: Outro"
   - Copie a senha gerada para `EMAIL_HOST_PASSWORD`

3. **Configurar .env:**
```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=senha-de-aplicacao-de-16-caracteres
```

### SendGrid (Alternativa Recomendada)

```bash
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=sua-api-key-do-sendgrid
```

---

## 🔒 SSL/HTTPS

### Opção 1: Let's Encrypt (Grátis)

```bash
# Instalar Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Renovação automática (já configurado)
sudo certbot renew --dry-run
```

### Opção 2: Cloudflare (Grátis + CDN)

1. Adicione seu domínio ao Cloudflare
2. Aponte os nameservers
3. Ative SSL/TLS "Full (strict)"
4. Configure Page Rules para cache

---

## 🗄️ Base de Dados

### Backup Manual

```bash
# Backup
pg_dump -U livraria_user -h localhost livraria_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar
psql -U livraria_user -h localhost livraria_db < backup_20250107_120000.sql
```

### Backup Automático (Cron)

```bash
# Editar crontab
crontab -e

# Adicionar linha (backup diário às 2h da manhã)
0 2 * * * /usr/bin/pg_dump -U livraria_user livraria_db > /backups/db_$(date +\%Y\%m\%d).sql
```

### Limpeza de Backups Antigos

```bash
# Manter apenas últimos 7 dias
find /backups -name "db_*.sql" -mtime +7 -delete
```

---

## 📊 Monitorização

### Logs do Django

```bash
# Ver logs de erro
tail -f logs/django_errors.log

# Ver logs do Nginx
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

### Monitorização de Performance

**Sentry (Recomendado):**
```bash
pip install sentry-sdk

# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://sua-chave@sentry.io/seu-projeto",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)
```

---

## 🐳 Deploy com Docker (Opcional)

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Coletar estáticos
RUN python manage.py collectstatic --noinput

# Executar
CMD ["gunicorn", "projeto_livraria.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: livraria_db
      POSTGRES_USER: livraria_user
      POSTGRES_PASSWORD: senha-forte
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn projeto_livraria.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
```

---

## 🔧 Troubleshooting

### Problema: "DisallowedHost"
**Solução:** Adicione o domínio a `ALLOWED_HOSTS` no `.env`

### Problema: Emails não são enviados
**Solução:** 
1. Verifique credenciais em `.env`
2. Confirme que a senha de aplicação do Gmail está correta
3. Teste com: `python manage.py shell`
```python
from django.core.mail import send_mail
send_mail('Teste', 'Mensagem', 'de@email.com', ['para@email.com'])
```

### Problema: Ficheiros estáticos não carregam
**Solução:**
```bash
python manage.py collectstatic --clear
python manage.py collectstatic
```

### Problema: Erros 500 em produção
**Solução:**
1. Configure `DEBUG=True` temporariamente para ver o erro
2. Verifique logs: `tail -f logs/django_errors.log`
3. Volte `DEBUG=False` depois

---

## 📝 Checklist de Deployment

- [ ] Variáveis de ambiente configuradas
- [ ] SECRET_KEY única gerada
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS configurado
- [ ] PostgreSQL instalado e configurado
- [ ] Migrações executadas
- [ ] Ficheiros estáticos coletados
- [ ] SSL/HTTPS ativo
- [ ] Email SMTP configurado
- [ ] Backups automáticos configurados
- [ ] Logs monitorizados
- [ ] Firewall configurado
- [ ] Domínio apontado corretamente

---

## 🆘 Suporte

Para problemas ou dúvidas:
- **Email:** suporte@livraria-online.pt
- **Documentação Django:** https://docs.djangoproject.com/
- **Stack Overflow:** Tag `django`

---

## 📜 Licença

© 2025 Livraria Online - Cantos de Papel. Todos os direitos reservados.
