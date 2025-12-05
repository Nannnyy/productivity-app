## FocusPom — Sistema de Produtividade, Pomodoro e Gerenciamento de Tarefas

## 1. Visão Geral
O FocusPom é uma aplicação web desenvolvida para auxiliar usuários na organização de tarefas e no gerenciamento do foco utilizando a técnica Pomodoro.
O sistema integra:
* Cadastro e login de usuários
* Criação e controle de tarefas
* Timer Pomodoro com registro automático
* Histórico de sessões
O objetivo é fornecer uma ferramenta simples e eficiente para melhorar produtividade, foco e acompanhamento de desempenho.

## 2. Objetivos do Sistema
* Facilitar o planejamento diário de atividades
* Aumentar foco usando ciclos Pomodoro
* Registrar sessões concluídas
* Exibir histórico de produtividade
* Fornecer interface simples, leve e responsiva

## 3. Funcionalidades
Autenticação
* Registro de usuário
* Login
* Senhas com hash
Gerenciamento de Tarefas
* Adicionar, listar, concluir e excluir tarefas
* Ligação entre tarefas e sessões Pomodoro
Pomodoro
* Timer funcional
* Registro automático da sessão no banco
Histórico
* Listagem de sessões realizadas
* Exibição das tarefas concluídas

## 4. Tecnologias
* Front-end: Streamlit
* Back-end: Python
* ORM: SQLAlchemy
* Migrações: Alembic
* Banco de dados: PostgreSQL
* Gerenciamento de dependências: requirements.txt

## 5. Estrutura do Repositório

```text
productivity-app/
├─ app/
│  ├─ main.py
│  ├─ db.py
│  ├─ models/
│  │  ├─ Pomodoro.py
│  │  ├─ Task.py
│  │  ├─ User.py
│  │  ├─ __init__.py
│  │  └─ database.py
│  ├─ resources/
│  │  ├─ CookieManager.py
│  │  ├─ Pomodoro.py
│  │  ├─ User.py
│  │  └─ __init__.py
│  ├─ pages/
│  │  ├─ Dashboard.py
│  │  ├─ Pomodoro.py
│  │  └─ RegisterUser.py
│  └─ partials/
│     └─ BasePage.py
├─ alembic/
│  ├─ versions/
│  │  ├─ 04db7a316a83_initial_migration.py
│  │  ├─ 07fda1024bd1_add_timezone_in_datetime_fields_in_.py
│  │  ├─ 16e59800ce9e_add_tables_for_pomodoro.py
│  │  └─ b5e7a62b5ca4_remove_unique_constraint_user_id_in_.py
│  ├─ script.py.mako
│  ├─ env.py
│  └─ README.md
├─ .streamlit/
│  └─ config.toml
├─ .env.example
├─ .gitignore
├─ alembic.ini
├─ requirements.txt
└─ README.md
```



## 6. Instalação (Local)

 1. Clonar o repositório
git clone <REPO_URL>
cd productivity-app




 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\\Scripts\\activate      # Windows




 3. Instalar dependências
pip install -r requirements.txt




 4. Configurar variáveis de ambiente
Copie .env.example → .env e configure:
* DATABASE_URL
* SECRET_KEY
* Outras variáveis necessárias
5. Rodar migrações
alembic upgrade head




 5. Executar o projeto
Frontend:
streamlit run app/main.py


## 7. Modelagem do Banco de Dados (DER)
Relacionamentos:
* User (1) — (N) Task
* User (1) — (N) PomodoroSession
* PomodoroCycle (1) — (N) PomodoroSession
* User (1) — (1) PomodoroConfig

Script SQL simplificado
```text
CREATE TABLE user (
  id SERIAL PRIMARY KEY,
  username VARCHAR(150) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);


CREATE TABLE task (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES user(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  due_date TIMESTAMP WITH TIME ZONE
);

CREATE TABLE pomodoro_cycle (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user(id) ON DELETE CASCADE,
    cycle_number INTEGER NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    status VARCHAR NOT NULL DEFAULT 'in_progress'
);

CREATE TABLE pomodoro_session (
    id SERIAL PRIMARY KEY,
    cycle_id INTEGER NOT NULL REFERENCES pomodoro_cycle(id) ON DELETE CASCADE,
    type VARCHAR NOT NULL,
    order_index INTEGER NOT NULL,
    duration_minutes INTEGER NOT NULL,
    remaining_seconds INTEGER,
    status VARCHAR NOT NULL DEFAULT 'pending',
    started_at TIMESTAMPTZ,
    paused_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    total_paused_seconds INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE pomodoro_user_config (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES user(id) ON DELETE CASCADE,

    work_minutes INTEGER NOT NULL DEFAULT 25,
    short_break_minutes INTEGER NOT NULL DEFAULT 5,
    long_break_minutes INTEGER NOT NULL DEFAULT 15,
    pomodoros_per_cycle INTEGER NOT NULL DEFAULT 4
);
```

## 9. Segurança
* Senha armazenadas com hash SHA-256 (hashlib)
* Uso do ORL SQLAlchemy (proteção contra SQL Injection)
* Autenticação por cookie assinado com SHA-256 + salt secreto fixo
* Validação de entradas no frontend (Streamlit)

## 10. Cronograma e Andamento

| Módulo           | Tarefa                           | Responsável | Status     |
|------------------|----------------------------------|-------------|------------|
| Conexão DB       | Configurar Postgres + SQLAlchemy | Pedro       | Concluído  |
| Modelos          | User e Task                      | Pedro       | Concluído  |
| Auth             | Registro/Login e telas           | Pedro       | Concluído  |
| Tasks            | Lógica para tarefas e telas      | Daniely     | Concluído  |
| Pomodoro (Models)| PomodoroCycle, PomodoroSession e PomodoroUserConfig | Carol | Concluído |
| Pomodoro         | Lógica para pomodoro e telas     | Carol       | Concluído  |
| Histórico        | Lógica para histórico e telas    | Luna        | Concluído  |
| Dashboard        | Tela                             | Daniely     | Concluído  |
| Documentação     | README, Documentação             | Leticia     | Concluído  |


## 11. Integrantes
* Pedro Henrique Barbosa da Cunha
* Daniely Evellin da Silva Vasconcelos
* Ana Carolina Santos Figueiredo
* Estela Luna dos Santos Oliveira
* Letícia Xavier Araújo Vasconcelos
