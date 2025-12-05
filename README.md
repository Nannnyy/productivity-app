## FocusPom — Sistema de Produtividade, Pomodoro e Gerenciamento de Tarefas

## 1. Visão Geral
O FocusPom é uma aplicação web desenvolvida para auxiliar usuários na organização de tarefas e no gerenciamento do foco utilizando a técnica Pomodoro.
O sistema integra:
* Cadastro e login de usuários
* Criação e controle de tarefas
* Timer Pomodoro com registro automático
* Histórico de sessões
* Dashboard 
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
Dashboard
* Visualizações gráficas sobre:
   * Tarefas concluídas
   * Tempo total em Pomodoro
   * Dias mais produtivos

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
streamlit run app/frontend.py




Backend:
uvicorn app.main:app --reload


## 7. Modelagem do Banco de Dados (DER)
Relacionamentos:
* User (1) — (N) Task
* User (1) — (N) PomodoroSession
* Task (1) — (N) PomodoroSession 

Script SQL simplificado
```text
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(150) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);


CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  due_date TIMESTAMP WITH TIME ZONE
);


CREATE TABLE pomodoro_sessions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  task_id INTEGER REFERENCES tasks(id) ON DELETE SET NULL,
  start_time TIMESTAMP WITH TIME ZONE NOT NULL,
  end_time TIMESTAMP WITH TIME ZONE,
  duration INTEGER,
  completed BOOLEAN DEFAULT false
);
```


## 8. Endpoints Principais
* POST /auth/register — Registrar usuário
* POST /auth/login — Login
* GET /tasks — Listar tarefas
* POST /tasks — Criar tarefa
* PATCH /tasks/{id}/complete — Concluir
* POST /pomodoros — Iniciar/registrar sessão
* GET /pomodoros — Histórico

## 9. Segurança
* Senhas com hash
* Uso de ORM
* Validação no backend
* Proteção básica contra XSS no Streamlit

## 10. Cronograma e Andamento

| Módulo           | Tarefa                          | Responsável | Status     |
|------------------|----------------------------------|-------------|------------|
| Conexão DB       | Configurar Postgres + SQLAlchemy | Pedro       | Concluído  |
| Modelos          | User, Task, PomodoroSession      | Pedro       | Concluído  |
| Auth             | Registro/Login                   | Pedro       | Concluído  |
| Tasks (API)      | CRUD                             | Daniely     | Concluído  |
| Tasks (Frontend) | Interface                        | Daniely     | Concluído  |
| Pomodoro         | Lógica + UI                      | Carol       | Concluído  |
| Histórico        | Lógica + UI                      | Luna        | Concluído  |
| Documentação     | README, Documentação             | Leticia     | Concluído  |


## 11. Integrantes
* Pedro — Backend / DB
* Daniely — Tarefas / Frontend
* Carol — Pomodoro
* Luna — Histórico / Frontend
* Letícia — Documentação
