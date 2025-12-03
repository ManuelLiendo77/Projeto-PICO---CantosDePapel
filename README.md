# Cantos de Papel - Plataforma de Comércio Eletrónico

![Estado](https://img.shields.io/badge/Estado-Em_Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-336791)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> **Solução completa de livraria online** com gestão de inventário, sistema de carrinho persistente, processamento de encomendas e painel de administração avançado.

---

**Nota Importante:**
Este projeto encontra-se atualmente **em fase de desenvolvimento**. Embora as funcionalidades principais estejam operacionais, 
continuamos a trabalhar em melhorias e otimizações. Este README será atualizado oficialmente assim que a versão final (v1.0) for publicada.

---

## Sobre o Projeto

**Cantos de Papel** é uma aplicação web *Full-Stack* desenvolvida para simular o ecossistema completo de uma livraria digital moderna. O projeto foca-se em oferecer uma experiência de utilizador fluida (UX) e uma gestão robusta de dados no backend.

Este projeto demonstra a capacidade de construir arquiteturas escaláveis utilizando **Django**, implementando desde a autenticação de utilizadores até ao fluxo completo de checkout, incluindo características avançadas como SEO técnico, gestão de cupões e implementação em servidor Linux.

### Autores
* **Manuel Liendo** - [GitHub](https://github.com/ManuelLiendo77) | [LinkedIn](https://www.linkedin.com/in/manuel-liendo-6b68a933b)
* **Bruno Monteiro** - [GitHub](https://github.com/Brunom83) | [LinkedIn](https://www.linkedin.com/in/bruno-monteiroinf)

---

## Características Principais

### Experiência de Compra (Frontend)
* **Catálogo Dinâmico:** Filtragem avançada por categoria, autor, intervalo de preços e ordenação dinâmica.
* **Pesquisa Inteligente:** Barra de pesquisa em tempo real por título, autor ou ISBN.
* **Carrinho de Compras:** Gestão de estado persistente (Base de dados + Sessão) e atualizações de quantidade em tempo real.
* **Sistema de Reviews:** Avaliações de 1 a 5 estrelas e comentários, com verificação de "Compra Confirmada" para garantir autenticidade.
* **Lista de Desejos (Favoritos):** Sistema para guardar livros favoritos para compra futura.

### Gestão e Backend
* **Painel de Administração Personalizado:** Gestão integral de livros, stock, encomendas e utilizadores através do Django Admin.
* **Sistema de Cupões:** Lógica complexa para descontos fixos ou percentuais, com validação de datas de validade e limites de utilização por utilizador.
* **Gestão de Encomendas:** Fluxo de estados (Pendente -> A Processar -> Enviado -> Entregue) com notificações automáticas por email.
* **Scripts de Automação:** Comandos personalizados (management commands) para importação de livros via Google Books API e normalização de dados.

### Segurança e SEO
* **Autenticação Robusta:** Login, Registo e Recuperação de palavra-passe via Email.
* **SEO Técnico:** Implementação de sitemaps.xml, robots.txt e meta-etiquetas dinâmicas para indexação.
* **Proteção:** Tokens CSRF, validação de formulários e decoradores de segurança nas views.

---

## Stack Tecnológico

| Área | Tecnologias |
| :--- | :--- |
| **Backend** | Python, Django 5.2, Django ORM |
| **Frontend** | HTML5, CSS3 (Design Responsivo), JavaScript (ES6+), Jinja2 Templates |
| **Base de Dados** | PostgreSQL (Produção), SQLite (Desenvolvimento) |
| **Infraestrutura** | Nginx, Gunicorn, Bash Scripting (Auto-setup) |
| **APIs** | Google Books API (Data Seeding) |

---

## Galeria

*(Nota: Capturas de ecrã serão adicionadas futuramente)*

---

## Instalação e Configuração

### Requisitos Prévios
* Python 3.8+
* Git

### Passos para Desenvolvimento Local

1.  **Clonar o repositório**
    ```bash
    git clone [https://github.com/ManuelLiendo77/Projeto-PICO---CantosDePapel.git](https://github.com/ManuelLiendo77/Projeto-PICO---CantosDePapel.git)
    cd Projeto-PICO---CantosDePapel
    ```

2.  **Criar e ativar ambiente virtual**
    ```bash
    python -m venv venv
    # No Windows:
    venv\Scripts\activate
    # No Mac/Linux:
    source venv/bin/activate
    ```

3.  **Instalar dependências**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variáveis de ambiente**
    Cria um ficheiro `.env` baseado no exemplo fornecido:
    ```bash
    cp .env.example .env
    # Edita o ficheiro .env com a tua configuração local
    ```

5.  **Aplicar migrações e criar superutilizador**
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

6.  **Executar o servidor**
    ```bash
    python manage.py runserver
    ```
    Visita `http://127.0.0.1:8000` no teu navegador.

### Implementação (Produção)

O projeto inclui um script de configuração automatizada (`setup_server.sh`) para servidores Linux (Ubuntu/Debian) que configura:
* Atualização do sistema.
* Instalação de PostgreSQL e Nginx.
* Configuração do Gunicorn como serviço do sistema (systemd).
* Configuração de proxy reverso com Nginx.

---

## Estrutura do Projeto

```text
cantos-de-papel/
├── members/                 # Aplicação principal
│   ├── models.py            # Modelos de BD (Livro, Pedido, Cupom, etc.)
│   ├── views.py             # Lógica de negócio e controladores
│   ├── urls.py              # Encaminhamento (Routing)
│   ├── templates/           # Templates HTML
│   ├── static/              # CSS, JS e Imagens
│   └── management/          # Scripts personalizados (Importação API, etc.)
├── projeto_livraria/        # Configuração do projeto Django
├── requirements.txt         # Dependências
├── setup_server.sh          # Script de implementação (deploy)
└── manage.py
