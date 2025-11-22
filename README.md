## Plano de Desenvolvimento

- Pomodoro, Produtividade e Tarefas

| Etapa | Módulo | Tarefas Chave | 
|-------|--------|---------------|
| Conexão DB | Conexão DB | Configurar conexão com Postgres |
|            | Conexão DB | Inicializar SQLAlchemy e Bases declarativas |
| Modelos ORM | Conexão DB | Definir os models: User, Task, PomodoroSession |
|             | Conexão DB | Criar primeira migration |
| Autenticação | Registro/Login | Implementar hash de senha |
|              | Registro/Login | Criar resource do usuário (CRUD) |
| Frontend Básico | Frontend | Desenvolver página inicial de registro e login |
|                 | Configuração | Implementar tela de configuração do usuário e configuração de sessão (st.session_state) |
| Gerenciamento de Tarefas | Lógica | Criar resource para o modelo de Task (Adicionar, listar, concluir, excluir) |
|                          | Frontend | Criar renderização para o gerenciamento de tarefas (Adicionar, listar, concluir, excluir) |
| Pomodoro Timer | Lógica | Implementar resource e lógica do timer pomodoro |
|                | Frontend | Criar a renderização para o timer do pomodoro |
| Histórico | Lógica | Implementar lógica no resource de Pomodoro e Tarefas para salvar as concluidas no banco |
|           | Frontend | Criar a renderização da página de histórico|
| Dashboard | Frontend | Criar dashboard com as visualizações em gráficos das informações |
| Finalização | Geral | Criar documentação sobre uso, BD, deploy e tals |