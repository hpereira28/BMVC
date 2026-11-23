from app.controllers.tarefa_record import TarefaRecord
from app.controllers.estudante_record import EstudanteRecord
from bottle import template, redirect, request


class Application():

    def __init__(self):
        self.pages = {
            'inicio': self.inicio,
            'entrar': self.entrar,
            'cadastro': self.cadastro,
            'tarefas': self.tarefas,
            'editar_tarefa': self.editar_tarefa
        }

        # composição: Application -> TarefaRecord e Application -> EstudanteRecord
        self.__tarefas = TarefaRecord()
        self.__estudantes = EstudanteRecord()


    def render(self, page, parameter=None):
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content()
        else:
            return content(parameter)


    def helper(self):
        return template('app/views/html/helper')


    # ---------- controle de acesso ----------

    def get_session_id(self):
        return request.get_cookie('session_id')


    def estudante_logado(self):
        """Devolve o estudante logado neste navegador, ou None."""
        return self.__estudantes.estudante_da_sessao(self.get_session_id())


    def exigir_login(self):
        """Usado nas páginas restritas: sem login, manda para a página de entrar."""
        estudante = self.estudante_logado()
        if not estudante:
            redirect('/entrar')
        return estudante


    def autenticar(self, login, senha):
        self.sair()  # se já tinha alguém logado neste navegador, desconecta antes
        return self.__estudantes.entrar(login.strip().lower(), senha)


    def cadastrar(self, nome, login, senha, confirmacao):
        """Cria a conta. Devolve uma mensagem de erro, ou None se deu tudo certo."""
        nome = nome.strip()
        login = login.strip().lower()
        if nome == "" or login == "" or senha == "":
            return "Preencha todos os campos."
        if " " in login:
            return "O login não pode ter espaços."
        if len(senha) < 4:
            return "A senha precisa ter pelo menos 4 caracteres."
        if senha != confirmacao:
            return "As senhas não são iguais."
        if self.__estudantes.buscar(login):
            return "Esse login já está em uso. Escolha outro."
        self.__estudantes.cadastrar(nome, login, senha)
        return None


    def sair(self):
        session_id = self.get_session_id()
        if session_id:
            self.__estudantes.sair(session_id)


    # ---------- páginas ----------

    def inicio(self):
        estudante = self.estudante_logado()
        pendentes = []
        if estudante:
            for tarefa in self.__tarefas.read_all(estudante.login):
                if not tarefa.concluida:
                    pendentes.append(tarefa)
        return template('app/views/html/inicio', estudante=estudante, pendentes=pendentes)


    def entrar(self, mensagem=None):
        return template('app/views/html/entrar', estudante=self.estudante_logado(), mensagem=mensagem)


    def cadastro(self, mensagem=None):
        return template('app/views/html/cadastro', estudante=self.estudante_logado(), mensagem=mensagem)


    def tarefas(self):
        estudante = self.exigir_login()  # página restrita
        return template('app/views/html/tarefas', estudante=estudante,
                        tarefas=self.__tarefas.read_all(estudante.login))


    def editar_tarefa(self, id):
        estudante = self.exigir_login()  # página restrita
        tarefa = self.__tarefas.read_one(id, estudante.login)
        if not tarefa:
            redirect('/tarefas')  # a tarefa não existe ou é de outro estudante
        return template('app/views/html/editar_tarefa', estudante=estudante, tarefa=tarefa)


    # ---------- ações do CRUD (todas exigem login) ----------

    def criar_tarefa(self, titulo, materia, pomodoros):
        estudante = self.exigir_login()
        titulo = titulo.strip()
        if titulo == "":
            return  # não cria tarefa sem título
        self.__tarefas.create(estudante.login, titulo, materia.strip(),
                              self.converter_pomodoros(pomodoros))


    def atualizar_tarefa(self, id, titulo, materia, pomodoros):
        estudante = self.exigir_login()
        titulo = titulo.strip()
        if titulo == "":
            return
        self.__tarefas.update(id, estudante.login, titulo, materia.strip(),
                              self.converter_pomodoros(pomodoros))


    def excluir_tarefa(self, id):
        estudante = self.exigir_login()
        self.__tarefas.delete(id, estudante.login)


    def registrar_pomodoro(self, id):
        estudante = self.exigir_login()
        self.__tarefas.registrar_pomodoro(id, estudante.login)


    def alternar_tarefa(self, id):
        estudante = self.exigir_login()
        self.__tarefas.alternar_concluida(id, estudante.login)


    def converter_pomodoros(self, texto):
        # o formulário manda texto: converte para número entre 1 e 20
        try:
            numero = int(texto)
        except (ValueError, TypeError):
            return 1
        if numero < 1:
            return 1
        if numero > 20:
            return 20
        return numero
