from app.models.tarefa import Tarefa
import json


class TarefaRecord():
    """Banco de dados JSON para o recurso Tarefas.
    Cada tarefa tem um dono, e cada estudante só enxerga as próprias tarefas."""

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

    def create(self, dono, titulo, materia, pomodoros):
        novo_id = 1
        for tarefa in self.__tarefas:
            if tarefa.id >= novo_id:
                novo_id = tarefa.id + 1
        nova = Tarefa(novo_id, dono, titulo, materia, pomodoros)
        self.__tarefas.append(nova)
        self.save()
        return nova


    def read_all(self, dono):
        tarefas_do_dono = []
        for tarefa in self.__tarefas:
            if tarefa.dono == dono:
                tarefas_do_dono.append(tarefa)
        return tarefas_do_dono


    def read_one(self, id, dono):
        try:
            id = int(id)  # a rota manda o id como texto
        except ValueError:
            return None   # id inválido, por exemplo /tarefas/editar/abc
        for tarefa in self.__tarefas:
            # só devolve a tarefa se ela for do estudante logado
            if tarefa.id == id and tarefa.dono == dono:
                return tarefa
        return None  # não achou


    def update(self, id, dono, titulo, materia, pomodoros):
        tarefa = self.read_one(id, dono)
        if tarefa:
            tarefa.titulo = titulo
            tarefa.materia = materia
            tarefa.pomodoros = pomodoros
            self.save()


    def delete(self, id, dono):
        tarefa = self.read_one(id, dono)
        if tarefa:
            self.__tarefas.remove(tarefa)
            self.save()


    # ---------- ações extras (também são "update") ----------

    def registrar_pomodoro(self, id, dono):
        tarefa = self.read_one(id, dono)
        if tarefa:
            tarefa.registrar_pomodoro()
            self.save()
        return tarefa  # o controlador usa para avisar o mural


    def alternar_concluida(self, id, dono):
        tarefa = self.read_one(id, dono)
        if tarefa:
            tarefa.alternar_concluida()
            self.save()
        return tarefa
