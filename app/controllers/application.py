from app.controllers.tarefa_record import TarefaRecord
from bottle import template, redirect


class Application():

    def __init__(self):
        self.pages = {
            'inicio': self.inicio,
            'tarefas': self.tarefas,
            'editar_tarefa': self.editar_tarefa
        }

        self.__tarefas = TarefaRecord()  # composição: Application -> TarefaRecord


    def render(self, page, parameter=None):
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content()
        else:
            return content(parameter)


    def helper(self):
        return template('app/views/html/helper')


    # ---------- páginas ----------

    def inicio(self):
        pendentes = []
        for tarefa in self.__tarefas.read_all():
            if not tarefa.concluida:
                pendentes.append(tarefa)
        return template('app/views/html/inicio', pendentes=pendentes)


    def tarefas(self):
        return template('app/views/html/tarefas', tarefas=self.__tarefas.read_all())


    def editar_tarefa(self, id):
        tarefa = self.__tarefas.read_one(id)
        if not tarefa:
            redirect('/tarefas')  # tarefa não existe: volta para a lista
        return template('app/views/html/editar_tarefa', tarefa=tarefa)


    # ---------- ações do CRUD ----------

    def criar_tarefa(self, titulo, materia, pomodoros):
        titulo = titulo.strip()
        if titulo == "":
            return  # não cria tarefa sem título
        self.__tarefas.create(titulo, materia.strip(), self.converter_pomodoros(pomodoros))


    def atualizar_tarefa(self, id, titulo, materia, pomodoros):
        titulo = titulo.strip()
        if titulo == "":
            return
        self.__tarefas.update(id, titulo, materia.strip(), self.converter_pomodoros(pomodoros))


    def excluir_tarefa(self, id):
        self.__tarefas.delete(id)


    def registrar_pomodoro(self, id):
        self.__tarefas.registrar_pomodoro(id)


    def alternar_tarefa(self, id):
        self.__tarefas.alternar_concluida(id)


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
