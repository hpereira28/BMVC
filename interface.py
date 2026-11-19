import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import date, timedelta

import estilo
from modelos.habito import criar_habito
from modelos.recompensa import catalogo_padrao

DIFICULDADES = {"Fácil": 1, "Médio": 2, "Difícil": 3}
NOMES_DIFICULDADE = {1: "Fácil", 2: "Médio", 3: "Difícil"}
FREQUENCIAS = {"Diária": "diaria", "Semanal": "semanal"}
NOMES_FREQUENCIA = {"diaria": "Diária", "semanal": "Semanal"}


class App:
    def __init__(self, janela, banco):
        self.janela = janela
        self.banco = banco  # ASSOCIAÇÃO: a App usa o banco criado no main.py
        self.catalogo = catalogo_padrao()

        self.usuario = self.banco.carregar_usuario()
        if self.usuario is None:
            nome = simpledialog.askstring("Bem-vindo", "Qual é o seu nome?", parent=janela)
            if not nome:
                nome = "Jogador"
            self.usuario = self.banco.criar_usuario(nome.strip())
        self.usuario.desbloquear_recompensas(self.catalogo)

        # sem geometry(): a janela se ajusta sozinha ao tamanho do conteúdo
        self.janela.title("Hábitos Gamificados")
        estilo.aplicar_estilo(self.janela)

        self.criar_cabecalho()
        self.criar_lista()
        self.criar_formulario()
        self.atualizar_tela()

    # ---------- montagem da tela ----------

    def criar_cabecalho(self):
        topo = tk.Frame(self.janela, bg=estilo.COR_PRIMARIA, padx=25, pady=14)
        topo.pack(fill="x")

        linha = tk.Frame(topo, bg=estilo.COR_PRIMARIA)
        linha.pack(fill="x")
        self.label_usuario = tk.Label(linha, bg=estilo.COR_PRIMARIA, fg="white",
                                      font=(estilo.FONTE, 18, "bold"))
        self.label_usuario.pack(side="left")
        self.label_nivel = tk.Label(linha, bg=estilo.COR_DESTAQUE, fg=estilo.COR_TEXTO,
                                    font=(estilo.FONTE, 10, "bold"), padx=10, pady=2)
        self.label_nivel.pack(side="left", padx=12)
        self.label_ofensiva = tk.Label(linha, bg=estilo.COR_PRIMARIA, fg="white",
                                       font=(estilo.FONTE, 11, "bold"))
        self.label_ofensiva.pack(side="right")

        self.barra_xp = ttk.Progressbar(topo, style="XP.Horizontal.TProgressbar")
        self.barra_xp.pack(fill="x", pady=(14, 4))
        self.label_xp = tk.Label(topo, bg=estilo.COR_PRIMARIA, fg=estilo.COR_PRIMARIA_CLARA,
                                 font=(estilo.FONTE, 9))
        self.label_xp.pack(anchor="w")

    def criar_lista(self):
        cartao = estilo.criar_cartao(self.janela)
        cartao.pack(fill="both", expand=True, padx=20, pady=(14, 6))
        estilo.criar_titulo(cartao, "Meus hábitos").pack(anchor="w", pady=(0, 10))

        colunas = ("nome", "frequencia", "dificuldade", "xp", "status")
        titulos = ("Hábito", "Frequência", "Dificuldade", "XP", "Status")
        self.tabela = ttk.Treeview(cartao, columns=colunas, show="headings", height=6)
        for coluna, titulo in zip(colunas, titulos):
            self.tabela.heading(coluna, text=titulo)
            self.tabela.column(coluna, width=110, anchor="center")
        self.tabela.column("nome", width=240, anchor="w")
        self.tabela.heading("nome", anchor="w")
        # linhas alternadas e hábitos concluídos em verde
        self.tabela.tag_configure("impar", background="#F8F6FD")
        self.tabela.tag_configure("concluida", foreground=estilo.COR_SUCESSO)
        self.tabela.pack(fill="both", expand=True)
        self.tabela.bind("<<TreeviewSelect>>", self.preencher_formulario)

        self.label_vazio = tk.Label(self.tabela, text="Nenhum hábito ainda. Cadastre o primeiro logo abaixo!",
                                    bg=estilo.COR_CARTAO, fg=estilo.COR_TEXTO_CLARO, font=(estilo.FONTE, 10))

        botoes = tk.Frame(cartao, bg=estilo.COR_CARTAO)
        botoes.pack(fill="x", pady=(12, 0))
        estilo.criar_botao(botoes, "✔  Concluir", estilo.COR_SUCESSO, self.concluir).pack(side="left")
        estilo.criar_botao(botoes, "✖  Excluir", estilo.COR_PERIGO, self.excluir).pack(side="left", padx=8)
        estilo.criar_botao(botoes, "★  Ver progresso", estilo.COR_PRIMARIA,
                           self.abrir_progresso).pack(side="right")

    def criar_formulario(self):
        cartao = estilo.criar_cartao(self.janela)
        cartao.pack(fill="x", padx=20, pady=(6, 16))
        estilo.criar_titulo(cartao, "Novo hábito / editar").grid(row=0, column=0, columnspan=3,
                                                                  sticky="w", pady=(0, 10))

        for coluna, texto in enumerate(["Nome", "Frequência", "Dificuldade"]):
            tk.Label(cartao, text=texto, bg=estilo.COR_CARTAO, fg=estilo.COR_TEXTO_CLARO,
                     font=(estilo.FONTE, 9)).grid(row=1, column=coluna, sticky="w", padx=(0, 12))

        self.entrada_nome = ttk.Entry(cartao, font=(estilo.FONTE, 10))
        self.entrada_nome.grid(row=2, column=0, sticky="we", padx=(0, 12))

        self.combo_frequencia = ttk.Combobox(cartao, values=list(FREQUENCIAS), state="readonly",
                                             width=12, font=(estilo.FONTE, 10))
        self.combo_frequencia.current(0)
        self.combo_frequencia.grid(row=2, column=1, padx=(0, 12))

        self.combo_dificuldade = ttk.Combobox(cartao, values=list(DIFICULDADES), state="readonly",
                                              width=12, font=(estilo.FONTE, 10))
        self.combo_dificuldade.current(0)
        self.combo_dificuldade.grid(row=2, column=2)

        cartao.columnconfigure(0, weight=1)

        botoes = tk.Frame(cartao, bg=estilo.COR_CARTAO)
        botoes.grid(row=3, column=0, columnspan=3, sticky="w", pady=(14, 0))
        estilo.criar_botao(botoes, "+  Adicionar", estilo.COR_PRIMARIA, self.adicionar).pack(side="left")
        estilo.criar_botao(botoes, "Salvar alteração", estilo.COR_SECUNDARIA,
                           self.editar).pack(side="left", padx=8)
        estilo.criar_botao(botoes, "Limpar", estilo.COR_NEUTRA, self.limpar_formulario).pack(side="left")

    # ---------- atualização da tela ----------

    def atualizar_tela(self):
        hoje = date.today()
        limite = self.usuario.xp_para_proximo_nivel()

        self.label_usuario.config(text=self.usuario.nome)
        self.label_nivel.config(text=f"★ Nível {self.usuario.nivel}")
        self.label_ofensiva.config(text=f"Ofensiva: {self.usuario.historico.ofensiva(hoje)} dia(s)")
        self.barra_xp.config(maximum=limite, value=self.usuario.xp)
        self.label_xp.config(text=f"{self.usuario.xp} / {limite} XP para o próximo nível")

        for item in self.tabela.get_children():
            self.tabela.delete(item)
        for posicao, habito in enumerate(self.usuario.habitos):
            tags = []
            if posicao % 2 == 1:
                tags.append("impar")
            status = habito.status(hoje)
            if status == "Concluída":
                tags.append("concluida")
                status = "✔ Concluída"
            self.tabela.insert("", tk.END, tags=tags, values=(
                habito.nome,
                NOMES_FREQUENCIA[habito.frequencia()],
                NOMES_DIFICULDADE[habito.dificuldade],
                f"+{habito.calcular_xp()}",
                status,
            ))

        # mostra a mensagem no meio da tabela só quando não há hábitos
        if self.usuario.habitos:
            self.label_vazio.place_forget()
        else:
            self.label_vazio.place(relx=0.5, rely=0.55, anchor="center")

    def habito_selecionado(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Atenção", "Selecione um hábito na lista.")
            return None
        indice = self.tabela.index(selecao[0])
        return self.usuario.habitos[indice]

    def selecionar(self, habito):
        # deixa a linha do hábito selecionada depois que a tabela é recriada
        indice = self.usuario.habitos.index(habito)
        self.tabela.selection_set(self.tabela.get_children()[indice])

    def preencher_formulario(self, evento):
        selecao = self.tabela.selection()
        if not selecao:
            return
        habito = self.usuario.habitos[self.tabela.index(selecao[0])]
        self.entrada_nome.delete(0, tk.END)
        self.entrada_nome.insert(0, habito.nome)
        self.combo_frequencia.set(NOMES_FREQUENCIA[habito.frequencia()])
        self.combo_dificuldade.set(NOMES_DIFICULDADE[habito.dificuldade])

    def ler_formulario(self):
        nome = self.entrada_nome.get().strip()
        if nome == "":
            messagebox.showwarning("Atenção", "Digite o nome do hábito.")
            return None
        frequencia = FREQUENCIAS[self.combo_frequencia.get()]
        dificuldade = DIFICULDADES[self.combo_dificuldade.get()]
        return nome, frequencia, dificuldade

    def limpar_formulario(self):
        self.entrada_nome.delete(0, tk.END)
        self.combo_frequencia.current(0)
        self.combo_dificuldade.current(0)
        self.tabela.selection_remove(self.tabela.selection())

    # ---------- UC01: Gerenciar Hábitos ----------

    def adicionar(self):
        dados = self.ler_formulario()
        if dados is None:
            return
        nome, frequencia, dificuldade = dados
        habito = criar_habito(nome, dificuldade, frequencia)
        self.banco.inserir_habito(habito)
        self.usuario.adicionar_habito(habito)
        self.limpar_formulario()
        self.atualizar_tela()

    def editar(self):
        antigo = self.habito_selecionado()
        if antigo is None:
            return
        dados = self.ler_formulario()
        if dados is None:
            return
        nome, frequencia, dificuldade = dados
        # cria de novo porque a frequência pode ter mudado (diário <-> semanal)
        novo = criar_habito(nome, dificuldade, frequencia, antigo.id, antigo.ultima_conclusao)
        indice = self.usuario.habitos.index(antigo)
        self.usuario.habitos[indice] = novo
        self.banco.atualizar_habito(novo)
        self.limpar_formulario()
        self.atualizar_tela()

    def excluir(self):
        habito = self.habito_selecionado()
        if habito is None:
            return
        if messagebox.askyesno("Excluir", f"Excluir o hábito '{habito.nome}'?"):
            self.banco.excluir_habito(habito)
            self.usuario.remover_habito(habito)
            self.limpar_formulario()
            self.atualizar_tela()

    # ---------- UC02: Registrar Conclusão Diária ----------

    def concluir(self):
        habito = self.habito_selecionado()
        if habito is None:
            return
        xp, subiu = self.usuario.concluir(habito, date.today())
        if xp == 0:
            messagebox.showinfo("Já concluído", "Esse hábito já foi concluído neste ciclo.")
            return

        self.banco.salvar_conclusao(self.usuario, habito)
        mensagem = f"Parabéns! Você ganhou {xp} XP."
        if subiu:
            mensagem += f"\n\nVocê subiu para o nível {self.usuario.nivel}!"
            for recompensa in self.usuario.desbloquear_recompensas(self.catalogo):
                mensagem += f"\nNova recompensa: {recompensa.nome}"
        self.atualizar_tela()
        self.selecionar(habito)
        messagebox.showinfo("Recompensa", mensagem)

    # ---------- UC03: Visualizar Progresso ----------

    def abrir_progresso(self):
        hoje = date.today()
        limite = self.usuario.xp_para_proximo_nivel()
        historico = self.usuario.historico

        janela = tk.Toplevel(self.janela)
        janela.title("Meu progresso")
        janela.configure(bg=estilo.COR_FUNDO)

        # topo com nome, nível e barra de XP
        topo = tk.Frame(janela, bg=estilo.COR_PRIMARIA, padx=20, pady=14)
        topo.pack(fill="x")
        tk.Label(topo, text=self.usuario.nome, bg=estilo.COR_PRIMARIA, fg="white",
                 font=(estilo.FONTE, 16, "bold")).pack(anchor="w")
        tk.Label(topo, text=f"★ Nível {self.usuario.nivel}", bg=estilo.COR_DESTAQUE, fg=estilo.COR_TEXTO,
                 font=(estilo.FONTE, 10, "bold"), padx=10, pady=2).pack(anchor="w", pady=(6, 12))
        ttk.Progressbar(topo, style="XP.Horizontal.TProgressbar", maximum=limite,
                        value=self.usuario.xp).pack(fill="x")
        tk.Label(topo, text=f"{self.usuario.xp} / {limite} XP para o próximo nível",
                 bg=estilo.COR_PRIMARIA, fg=estilo.COR_PRIMARIA_CLARA,
                 font=(estilo.FONTE, 9)).pack(anchor="w", pady=(4, 0))

        # três cartões com números
        numeros = tk.Frame(janela, bg=estilo.COR_FUNDO)
        numeros.pack(fill="x", padx=16, pady=12)
        self.criar_numero(numeros, historico.ofensiva(hoje), "dias de ofensiva")
        self.criar_numero(numeros, historico.total_xp(), "XP ganho no total")
        self.criar_numero(numeros, len(historico.registros), "conclusões")

        # gráfico de barras com as conclusões dos últimos 7 dias
        cartao = estilo.criar_cartao(janela)
        cartao.pack(fill="x", padx=20)
        estilo.criar_titulo(cartao, "Conclusões nos últimos 7 dias").pack(anchor="w")
        grafico = tk.Canvas(cartao, width=400, height=140, bg=estilo.COR_CARTAO, highlightthickness=0)
        grafico.pack(pady=(8, 0))
        grafico.create_line(10, 110, 390, 110, fill=estilo.COR_BORDA, width=2)
        for i in range(7):
            dia = hoje - timedelta(days=6 - i)
            quantidade = historico.conclusoes_no_dia(dia)
            altura = min(quantidade * 25, 90)
            x = 25 + i * 54
            cor = estilo.COR_PRIMARIA
            if dia == hoje:
                cor = estilo.COR_DESTAQUE
            if quantidade > 0:
                grafico.create_rectangle(x, 110 - altura, x + 34, 110, fill=cor, outline="")
            grafico.create_text(x + 17, 101 - altura, text=str(quantidade),
                                font=(estilo.FONTE, 9, "bold"), fill=estilo.COR_TEXTO)
            grafico.create_text(x + 17, 126, text=dia.strftime("%d/%m"),
                                font=(estilo.FONTE, 8), fill=estilo.COR_TEXTO_CLARO)

        # recompensas: desbloqueadas em dourado, bloqueadas em cinza
        cartao = estilo.criar_cartao(janela)
        cartao.pack(fill="both", expand=True, padx=20, pady=12)
        estilo.criar_titulo(cartao, "Recompensas").pack(anchor="w", pady=(0, 8))
        for recompensa in self.catalogo:
            if recompensa in self.usuario.recompensas:
                texto = f"★  {recompensa.nome}"
                fundo, cor_texto = "#FFF4CC", "#8A6A00"
            else:
                texto = f"☆  {recompensa.nome}  (desbloqueia no nível {recompensa.nivel_necessario})"
                fundo, cor_texto = "#F0EEF5", estilo.COR_TEXTO_CLARO
            tk.Label(cartao, text=texto, bg=fundo, fg=cor_texto, font=(estilo.FONTE, 10),
                     anchor="w", padx=10, pady=4).pack(fill="x", pady=2)

    def criar_numero(self, pai, valor, legenda):
        cartao = estilo.criar_cartao(pai)
        cartao.pack(side="left", fill="x", expand=True, padx=4)
        tk.Label(cartao, text=str(valor), bg=estilo.COR_CARTAO, fg=estilo.COR_PRIMARIA,
                 font=(estilo.FONTE, 20, "bold")).pack()
        tk.Label(cartao, text=legenda, bg=estilo.COR_CARTAO, fg=estilo.COR_TEXTO_CLARO,
                 font=(estilo.FONTE, 9)).pack()
