## Plano de Desenvolvimento

- Pomodoro, Produtividade e Tarefas

| Etapa | Módulo | Tarefas Chave | Responsável | Finalizado |
|-------|--------|---------------|-------------|------------|
| Conexão DB | Conexão DB | Configurar conexão com Postgres | Pedro | Sim |
|            | Conexão DB | Inicializar SQLAlchemy e Bases declarativas | Pedro | Sim |
| Modelos ORM | Conexão DB | Definir os models: User, Task, PomodoroSession | Pedro | Parcial |
|             | Conexão DB | Criar primeira migration | Pedro | Sim |
| Autenticação | Registro/Login | Implementar hash de senha | Pedro | Sim |
|              | Registro/Login | Criar resource do usuário (CRUD) | Pedro | Sim |
| Frontend Básico | Frontend | Desenvolver página inicial de registro e login | Pedro | Sim |
|                 | Configuração | Implementar tela de configuração do usuário e configuração de sessão (st.session_state) | Pedro | Parcial (CookieManagement feito) |
| Gerenciamento de Tarefas | Lógica | Criar resource para o modelo de Task (Adicionar, listar, concluir, excluir) |
|                          | Frontend | Criar renderização para o gerenciamento de tarefas (Adicionar, listar, concluir, excluir) |
| Pomodoro Timer | Lógica | Implementar resource e lógica do timer pomodoro |
|                | Frontend | Criar a renderização para o timer do pomodoro |
| Histórico | Lógica | Implementar lógica no resource de Pomodoro e Tarefas para salvar as concluidas no banco |
|           | Frontend | Criar a renderização da página de histórico|
| Dashboard | Frontend | Criar dashboard com as visualizações em gráficos das informações |
| Finalização | Geral | Criar documentação sobre uso, BD, deploy e tals |
