import os
import tkinter as tk

from banco import BancoDados
from interface import App

# o banco fica salvo na mesma pasta deste arquivo
ARQUIVO_BANCO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "habitos.db")


def main():
    banco = BancoDados(ARQUIVO_BANCO)
    janela = tk.Tk()
    App(janela, banco)
    janela.mainloop()
    banco.fechar()


if __name__ == "__main__":
    main()
