from datetime import datetime


class Atividade():
    """Algo que um estudante fez, mostrado ao vivo no mural (ex.: "Henrique fez um pomodoro de POO")."""

    def __init__(self, nome, texto):
        self.nome = nome
        self.texto = texto
        self.hora = datetime.now().strftime("%H:%M")

    def para_dicionario(self):
        # o WebSocket manda os dados para o navegador como dicionário (JSON)
        return {"nome": self.nome, "texto": self.texto, "hora": self.hora}
