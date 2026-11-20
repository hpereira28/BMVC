class Tarefa():
    """Uma tarefa de estudo, medida em pomodoros (blocos de 25 minutos)."""

    def __init__(self, id, titulo, materia, pomodoros, feitos=0, concluida=False):
        self.id = id
        self.titulo = titulo
        self.materia = materia
        self.pomodoros = pomodoros    # quantos pomodoros a tarefa deve levar
        self.feitos = feitos          # quantos pomodoros já foram feitos
        self.concluida = concluida

    def registrar_pomodoro(self):
        self.feitos += 1

    def alternar_concluida(self):
        self.concluida = not self.concluida

    def progresso(self):
        """Porcentagem de pomodoros feitos (no máximo 100)."""
        porcentagem = int(self.feitos / self.pomodoros * 100)
        return min(porcentagem, 100)

    def status(self):
        if self.concluida:
            return "Concluída"
        if self.feitos == 0:
            return "A fazer"
        return "Em andamento"
