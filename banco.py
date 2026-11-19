import sqlite3
from datetime import date

from modelos.usuario import Usuario
from modelos.habito import criar_habito


class BancoDados:
    """DEPENDÊNCIA: usa Usuario e Habito como parâmetros dos métodos,
    mas não guarda nenhum deles como atributo."""

    def __init__(self, arquivo="habitos.db"):
        self.conexao = sqlite3.connect(arquivo)
        self.criar_tabelas()

    def criar_tabelas(self):
        cursor = self.conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                xp INTEGER NOT NULL,
                nivel INTEGER NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habito (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                dificuldade INTEGER NOT NULL,
                frequencia TEXT NOT NULL,
                ultima_conclusao TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_habito TEXT NOT NULL,
                xp INTEGER NOT NULL,
                data TEXT NOT NULL
            )
        """)
        self.conexao.commit()

    def criar_usuario(self, nome):
        cursor = self.conexao.cursor()
        cursor.execute("INSERT INTO usuario (nome, xp, nivel) VALUES (?, 0, 1)", (nome,))
        self.conexao.commit()
        return Usuario(nome, id=cursor.lastrowid)

    def carregar_usuario(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT id, nome, xp, nivel FROM usuario LIMIT 1")
        linha = cursor.fetchone()
        if linha is None:
            return None
        usuario = Usuario(linha[1], linha[2], linha[3], linha[0])

        cursor.execute("SELECT id, nome, dificuldade, frequencia, ultima_conclusao FROM habito")
        for id, nome, dificuldade, frequencia, ultima in cursor.fetchall():
            ultima_conclusao = None
            if ultima:
                ultima_conclusao = date.fromisoformat(ultima)
            habito = criar_habito(nome, dificuldade, frequencia, id, ultima_conclusao)
            usuario.adicionar_habito(habito)

        cursor.execute("SELECT nome_habito, xp, data FROM historico")
        for nome_habito, xp, data in cursor.fetchall():
            usuario.historico.adicionar(nome_habito, xp, date.fromisoformat(data))

        return usuario

    def salvar_usuario(self, usuario):
        cursor = self.conexao.cursor()
        cursor.execute(
            "UPDATE usuario SET nome = ?, xp = ?, nivel = ? WHERE id = ?",
            (usuario.nome, usuario.xp, usuario.nivel, usuario.id),
        )
        self.conexao.commit()

    def inserir_habito(self, habito):
        cursor = self.conexao.cursor()
        cursor.execute(
            "INSERT INTO habito (nome, dificuldade, frequencia, ultima_conclusao) VALUES (?, ?, ?, ?)",
            (habito.nome, habito.dificuldade, habito.frequencia(), self.data_texto(habito.ultima_conclusao)),
        )
        self.conexao.commit()
        habito.id = cursor.lastrowid

    def atualizar_habito(self, habito):
        cursor = self.conexao.cursor()
        cursor.execute(
            "UPDATE habito SET nome = ?, dificuldade = ?, frequencia = ?, ultima_conclusao = ? WHERE id = ?",
            (habito.nome, habito.dificuldade, habito.frequencia(),
             self.data_texto(habito.ultima_conclusao), habito.id),
        )
        self.conexao.commit()

    def excluir_habito(self, habito):
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM habito WHERE id = ?", (habito.id,))
        self.conexao.commit()

    def salvar_conclusao(self, usuario, habito):
        """Salva o XP do usuário, a data no hábito e o último registro do histórico."""
        registro = usuario.historico.registros[-1]
        cursor = self.conexao.cursor()
        cursor.execute(
            "INSERT INTO historico (nome_habito, xp, data) VALUES (?, ?, ?)",
            (registro.nome_habito, registro.xp, registro.data.isoformat()),
        )
        self.conexao.commit()
        self.salvar_usuario(usuario)
        self.atualizar_habito(habito)

    def data_texto(self, data):
        if data is None:
            return None
        return data.isoformat()

    def fechar(self):
        self.conexao.close()
