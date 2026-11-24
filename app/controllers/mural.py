from app.models.atividade import Atividade
from datetime import date


class Mural():
    """Guarda (em memória) as últimas atividades de todos os estudantes, para mostrar ao vivo."""

    LIMITE = 8  # quantas atividades aparecem no mural

    def __init__(self):
        self.__atividades = []
        self.__pomodoros_hoje = 0
        self.__dia = date.today()


    def registrar(self, nome, texto, foi_pomodoro=False):
        self.verificar_dia()
        if foi_pomodoro:
            self.__pomodoros_hoje += 1
        self.__atividades.insert(0, Atividade(nome, texto))  # a mais nova fica em cima
        if len(self.__atividades) > Mural.LIMITE:
            self.__atividades.pop()  # tira a mais antiga


    def verificar_dia(self):
        if date.today() != self.__dia:  # virou o dia: zera o contador de pomodoros
            self.__dia = date.today()
            self.__pomodoros_hoje = 0


    def estado(self, conectados):
        """Tudo o que a página precisa para desenhar o mural."""
        self.verificar_dia()
        atividades = []
        for atividade in self.__atividades:
            atividades.append(atividade.para_dicionario())
        return {
            "conectados": conectados,
            "pomodoros_hoje": self.__pomodoros_hoje,
            "atividades": atividades
        }
