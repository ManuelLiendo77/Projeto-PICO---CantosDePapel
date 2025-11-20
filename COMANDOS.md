# =============================================================================
# COMANDOS ÚTEIS - Livraria Online
# =============================================================================
# Referência rápida de comandos Django para desenvolvimento e produção
# =============================================================================

# -----------------------------------------------------------------------------
# DESENVOLVIMENTO LOCAL
# -----------------------------------------------------------------------------

# Iniciar servidor de desenvolvimento
python manage.py runserver

# Servidor em porta específica
python manage.py runserver 8080

# Servidor acessível na rede local
python manage.py runserver 0.0.0.0:8000

# -----------------------------------------------------------------------------
# BASE DE DADOS
# -----------------------------------------------------------------------------

# Criar novas migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Ver SQL das migrações
python manage.py sqlmigrate members 0001

# Reverter migração
python manage.py migrate members 0001

# Resetar base de dados (CUIDADO!)
python manage.py flush

# Fazer backup da base de dados
python manage.py dumpdata > backup.json

# Restaurar backup
python manage.py loaddata backup.json

# -----------------------------------------------------------------------------
# SUPERUSER E UTILIZADORES
# -----------------------------------------------------------------------------

# Criar superuser
python manage.py createsuperuser

# Alterar password de utilizador
python manage.py changepassword username

# Shell interativa
python manage.py shell

# Shell com IPython (se instalado)
python manage.py shell -i ipython

# -----------------------------------------------------------------------------
# FICHEIROS ESTÁTICOS
# -----------------------------------------------------------------------------

# Coletar ficheiros estáticos para produção
python manage.py collectstatic

# Limpar ficheiros estáticos antigos
python manage.py collectstatic --clear --noinput

# -----------------------------------------------------------------------------
# TESTES
# -----------------------------------------------------------------------------

# Executar todos os testes
python manage.py test

# Testar app específica
python manage.py test members

# Testar com verbosidade
python manage.py test --verbosity=2

# Manter base de dados após testes
python manage.py test --keepdb

# -----------------------------------------------------------------------------
# EMAILS (DESENVOLVIMENTO)
# -----------------------------------------------------------------------------

# Enviar email de teste
python manage.py sendtestemail admin@example.com

# Servidor SMTP de teste (recebe emails na porta 1025)
python -m smtpd -n -c DebuggingServer localhost:1025

# -----------------------------------------------------------------------------
# DADOS DE TESTE
# -----------------------------------------------------------------------------

# Popular base de dados com dados de exemplo
python manage.py loaddata fixtures/livros.json

# Criar fixtures dos dados atuais
python manage.py dumpdata members.Livro --indent 2 > fixtures/livros.json

# -----------------------------------------------------------------------------
# LIMPEZA E MANUTENÇÃO
# -----------------------------------------------------------------------------

# Limpar sessões expiradas
python manage.py clearsessions

# Verificar problemas no projeto
python manage.py check

# Ver configurações atuais
python manage.py diffsettings

# -----------------------------------------------------------------------------
# SHELL PYTHON ÚTIL
# -----------------------------------------------------------------------------

# Dentro do shell Django (python manage.py shell):

# Listar todos os livros
from members.models import Livro
Livro.objects.all()

# Criar novo livro
livro = Livro.objects.create(
    titulo='Novo Livro',
    autor='Autor',
    preco=19.99,
    stock=50
)

# Atualizar preços em massa
Livro.objects.filter(categoria='Ficção').update(preco=15.99)

# Contar pedidos por status
from members.models import Pedido
Pedido.objects.values('status').annotate(count=Count('id'))

# Listar utilizadores
from django.contrib.auth.models import User
User.objects.all()

# Enviar email de teste
from django.core.mail import send_mail
send_mail(
    'Assunto',
    'Mensagem',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)

# -----------------------------------------------------------------------------
# PRODUÇÃO
# -----------------------------------------------------------------------------

# Coletar estáticos + migrar + reiniciar (uma linha)
python manage.py collectstatic --noinput && python manage.py migrate && sudo systemctl restart gunicorn

# Ver logs do Gunicorn
sudo journalctl -u gunicorn -f

# Ver logs do Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Reiniciar serviços
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# Ver status dos serviços
sudo systemctl status gunicorn
sudo systemctl status nginx

# -----------------------------------------------------------------------------
# GIT
# -----------------------------------------------------------------------------

# Status
git status

# Adicionar todos os ficheiros
git add .

# Commit
git commit -m "Mensagem do commit"

# Push
git push origin main

# Pull
git pull origin main

# Ver diferenças
git diff

# Ver histórico
git log --oneline

# -----------------------------------------------------------------------------
# VIRTUAL ENV
# -----------------------------------------------------------------------------

# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate

# Desativar
deactivate

# Instalar dependências
pip install -r requirements.txt

# Gerar requirements.txt
pip freeze > requirements.txt

# Atualizar pacote específico
pip install --upgrade Django

# -----------------------------------------------------------------------------
# ÚTEIS
# -----------------------------------------------------------------------------

# Ver versão do Django
python -m django --version

# Ver pacotes instalados
pip list

# Ver pacotes desatualizados
pip list --outdated

# Verificar vulnerabilidades de segurança
pip check

# Limpar cache do Python
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# =============================================================================
# ATALHOS PERSONALIZADOS (adicione ao .bashrc ou .zshrc)
# =============================================================================

# alias djrun='python manage.py runserver'
# alias djmig='python manage.py makemigrations && python manage.py migrate'
# alias djshell='python manage.py shell'
# alias djtest='python manage.py test'
# alias djsuper='python manage.py createsuperuser'

# =============================================================================
