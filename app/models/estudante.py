import hashlib


def criptografar(senha):
    """Transforma a senha num código (hash), para não guardar a senha de verdade no arquivo."""
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


class Estudante():
    """Conta de um estudante que usa o Foco+."""

    def __init__(self, nome, login, senha_hash):
        self.nome = nome
        self.login = login
        self.senha_hash = senha_hash

    def confere_senha(self, senha):
        return self.senha_hash == criptografar(senha)

    def primeiro_nome(self):
        return self.nome.split()[0]
