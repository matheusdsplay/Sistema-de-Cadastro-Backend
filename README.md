# Projeto Backend - Cadastro e Login de Usuários

Este é um projeto simples de backend em Python usando Flask e SQLite, que permite o cadastro, login e gerenciamento de usuários.

## Funcionalidades

- Cadastro de novos usuários com nome, e-mail e senha (senha protegida por hash)
- Login de usuários usando e-mail e senha
- Listagem de usuários cadastrados (rota protegida)
- Atualização e remoção de usuários via API
- Interface web estilizada com HTML e CSS
- Mensagens de erro amigáveis para o usuário

## Tecnologias Utilizadas

- Python 3
- Flask
- Flask-SQLAlchemy
- Werkzeug (para hash de senha)
- SQLite (banco de dados local)
- HTML5 e CSS3

## Como rodar o projeto

1. **Clone este repositório:**
   bash
   git clone https://github.com/matheusdsplay/Sistema-de-Cadastro-Backend.git
   cd Sistema-de-Cadastro-Backend
   

2. **Instale as dependências:**
   bash
   pip install flask flask_sqlalchemy werkzeug
   

3. **Execute o aplicativo:**
   bash
   python app.py
   

4. **Acesse no navegador:**
   http://localhost:5000/
   

## Estrutura de Pastas
projeto-backend/
│
├── app.py
├── users.db
├── static/
│   └── style.css
└── templates/
    ├── index.html
    ├── register.html
    └── dashboard.html

## Rotas Principais

- `/` — Página inicial de login
- `/register` — Página de cadastro de usuário
- `/dashboard/<nome>` — Painel do usuário logado
- `/users` — API para listar/criar usuários (GET/POST)
- `/users/<id>` — API para atualizar/deletar usuário (PUT/DELETE)

## Observações

- As senhas são armazenadas de forma segura usando hash.
- O banco de dados `users.db` é criado automaticamente na primeira execução.
- Para reiniciar o banco, basta apagar o arquivo `users.db` e rodar o app novamente.

---

Feito com ❤️ usando Flask!
