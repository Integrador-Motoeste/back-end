# Motocar

Este é um guia para inicialização local do backend do projeto Motocar

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# Executando o Projeto Django

Siga os passos abaixo para configurar e executar o projeto Django localmente.

## Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas em sua máquina:

- [Python 3.x](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/)
- [Postgresql](https://www.postgresql.org/) 

## Clonando o Repositório

1. Clone o repositório do projeto:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git

2. Crie e ative um ambiente virtual
   ```bash
   pyton -m venv .venv
   .venv/scripts/activate
   #ou
   source .venv/bin/activate

3. Instale as depedências
   ```bash
   pip install -r requirements/local.txt
   pip install -r requirements/base.txt
   pip install -r requirements/production.txt

4. Crie um arquivo .env na raiz e coloque o seguinte código:
   ```bash
   DATABASE_URL=postgres://usuario_banco:senha_banco@127.0.0.1:5432/ride_app
   CELERY_BROKER_URL=redis://localhost:6379/0
   USE_DOCKER=No
   ASAAS_API_KEY=chave_api_asaas

5. Rode as migrações
   ```bash
   python manage.py makemigrations
   python manage.py migrate

6. Carregue dados iniciais
   ```bash
   python manage.py loaddata groups.json

7. Crie um superusuário
   ```bash
   python manage.py createsuperuser

8. Rode o servidor
   ```bash
   python manage.py runserver
