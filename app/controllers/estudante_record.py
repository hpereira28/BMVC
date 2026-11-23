from app.models.estudante import Estudante, criptografar
import json
import uuid


class EstudanteRecord():
    """Banco de dados JSON para as contas de estudantes, e controle de quem está logado"""

    def __init__(self, arquivo="app/controllers/db/estudantes.json"):
        self.__arquivo = arquivo
        self.__estudantes = []
        self.__sessoes = {}  # session_id -> estudante logado
        self.read()


    def read(self):
        try:
            with open(self.__arquivo, "r", encoding="utf-8") as arquivo_json:
                dados = json.load(arquivo_json)
                self.__estudantes = [Estudante(**item) for item in dados]
        except FileNotFoundError:
            self.__estudantes = []  # ainda não existe nenhuma conta


    def save(self):
        with open(self.__arquivo, "w", encoding="utf-8") as arquivo_json:
            dados = [vars(estudante) for estudante in self.__estudantes]
            json.dump(dados, arquivo_json, ensure_ascii=False, indent=2)


    def buscar(self, login):
        for estudante in self.__estudantes:
            if estudante.login == login:
                return estudante
        return None


    def cadastrar(self, nome, login, senha):
        novo = Estudante(nome, login, criptografar(senha))
        self.__estudantes.append(novo)
        self.save()
        return novo


    # ---------- login e sessões ----------

    def entrar(self, login, senha):
        estudante = self.buscar(login)
        if estudante and estudante.confere_senha(senha):
            session_id = str(uuid.uuid4())  # código único e aleatório para a sessão
            self.__sessoes[session_id] = estudante
            return session_id
        return None  # login ou senha errados


    def estudante_da_sessao(self, session_id):
        if session_id in self.__sessoes:
            return self.__sessoes[session_id]
        return None


    def sair(self, session_id):
        if session_id in self.__sessoes:
            del self.__sessoes[session_id]
