from app.models.tarefa import Tarefa
import json


class TarefaRecord():
    """Banco de dados JSON para o recurso Tarefas"""

    def __init__(self, arquivo="app/controllers/db/tarefas.json"):
        self.__arquivo = arquivo
        self.__tarefas = []
        self.read()


    def read(self):
        try:
            with open(self.__arquivo, "r", encoding="utf-8") as arquivo_json:
                dados = json.load(arquivo_json)
                self.__tarefas = [Tarefa(**item) for item in dados]
        except FileNotFoundError:
            self.__tarefas = []  # ainda não existe nenhuma tarefa salva


    def save(self):
        with open(self.__arquivo, "w", encoding="utf-8") as arquivo_json:
            dados = [vars(tarefa) for tarefa in self.__tarefas]
            json.dump(dados, arquivo_json, ensure_ascii=False, indent=2)


    # ---------- CRUD ----------

    def create(self, titulo, materia, pomodoros):
        novo_id = 1
        for tarefa in self.__tarefas:
            if tarefa.id >= novo_id:
                novo_id = tarefa.id + 1
        nova = Tarefa(novo_id, titulo, materia, pomodoros)
        self.__tarefas.append(nova)
        self.save()
        return nova


    def read_all(self):
        return self.__tarefas


    def read_one(self, id):
        try:
            id = int(id)  # a rota manda o id como texto
        except ValueError:
            return None   # id inválido, por exemplo /tarefas/editar/abc
        for tarefa in self.__tarefas:
            if tarefa.id == id:
                return tarefa
        return None  # não achou


    def update(self, id, titulo, materia, pomodoros):
        tarefa = self.read_one(id)
        if tarefa:
            tarefa.titulo = titulo
            tarefa.materia = materia
            tarefa.pomodoros = pomodoros
            self.save()


    def delete(self, id):
        tarefa = self.read_one(id)
        if tarefa:
            self.__tarefas.remove(tarefa)
            self.save()


    # ---------- ações extras (também são "update") ----------

    def registrar_pomodoro(self, id):
        tarefa = self.read_one(id)
        if tarefa:
            tarefa.registrar_pomodoro()
            self.save()


    def alternar_concluida(self, id):
        tarefa = self.read_one(id)
        if tarefa:
            tarefa.alternar_concluida()
            self.save()
