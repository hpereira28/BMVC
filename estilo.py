import tkinter as tk
from tkinter import ttk

# fonte e cores usadas em todas as telas
FONTE = "Segoe UI"

COR_FUNDO = "#F3F0FA"
COR_CARTAO = "#FFFFFF"
COR_BORDA = "#E3DDF2"
COR_PRIMARIA = "#6C3FC5"
COR_PRIMARIA_CLARA = "#EDE6FB"
COR_PRIMARIA_ESCURA = "#4E2B99"
COR_SECUNDARIA = "#8E7CC3"
COR_NEUTRA = "#A19DB3"
COR_SUCESSO = "#2E9E5B"
COR_PERIGO = "#D9534F"
COR_DESTAQUE = "#FFC83D"
COR_TEXTO = "#2B2840"
COR_TEXTO_CLARO = "#7C7891"


def aplicar_estilo(janela):
    """Configura o tema dos componentes ttk (tabela, barra de XP, campos)."""
    janela.configure(bg=COR_FUNDO)
    tema = ttk.Style(janela)
    tema.theme_use("clam")

    tema.configure("Treeview", background=COR_CARTAO, fieldbackground=COR_CARTAO,
                   foreground=COR_TEXTO, rowheight=30, font=(FONTE, 10),
                   bordercolor=COR_BORDA, lightcolor=COR_BORDA, darkcolor=COR_BORDA)
    tema.configure("Treeview.Heading", background=COR_PRIMARIA_CLARA, foreground=COR_PRIMARIA,
                   font=(FONTE, 10, "bold"), relief="flat", padding=6)
    tema.map("Treeview", background=[("selected", COR_PRIMARIA)], foreground=[("selected", "white")])
    tema.map("Treeview.Heading", background=[("active", COR_PRIMARIA_CLARA)])

    tema.configure("XP.Horizontal.TProgressbar", troughcolor=COR_PRIMARIA_ESCURA,
                   background=COR_DESTAQUE, lightcolor=COR_DESTAQUE, darkcolor=COR_DESTAQUE,
                   bordercolor=COR_PRIMARIA_ESCURA, thickness=14)

    # campos de texto e de seleção brancos, com borda roxa clara
    tema.configure("TEntry", padding=5, bordercolor=COR_BORDA, lightcolor=COR_BORDA)
    tema.map("TEntry", bordercolor=[("focus", COR_PRIMARIA)], lightcolor=[("focus", COR_PRIMARIA)])
    tema.configure("TCombobox", padding=4, bordercolor=COR_BORDA, lightcolor=COR_BORDA,
                   background=COR_PRIMARIA_CLARA, arrowcolor=COR_PRIMARIA)
    tema.map("TCombobox",
             fieldbackground=[("readonly", COR_CARTAO)],
             selectbackground=[("readonly", COR_CARTAO)],
             selectforeground=[("readonly", COR_TEXTO)],
             background=[("active", COR_PRIMARIA_CLARA)])


def criar_botao(pai, texto, cor, comando):
    return tk.Button(pai, text=texto, command=comando, bg=cor, fg="white",
                     activebackground=cor, activeforeground="white",
                     font=(FONTE, 10, "bold"), relief="flat", borderwidth=0,
                     padx=14, pady=6, cursor="hand2")


def criar_cartao(pai):
    """Um quadro branco com borda fininha, usado como 'cartão'."""
    return tk.Frame(pai, bg=COR_CARTAO, padx=15, pady=15,
                    highlightthickness=1, highlightbackground=COR_BORDA)


def criar_titulo(pai, texto):
    return tk.Label(pai, text=texto, bg=COR_CARTAO, fg=COR_TEXTO, font=(FONTE, 12, "bold"))
