# Foco+ (BMVC)

Página web feita com o framework **BMVC** (arquitetura MVC com o servidor **Bottle**).
O **Foco+** ajuda estudantes a estudar com a técnica **Pomodoro**: explica como a técnica funciona,
tem um **cronômetro** com os modos Foco (25 min), Pausa curta (5 min) e Pausa longa (15 min),
e uma **lista de tarefas** do dia.

Projeto da disciplina de **Orientação a Objetos**, Engenharia de Software.

## Como rodar

Instale o Bottle (só na primeira vez):

```bash
pip install bottle
```

Na pasta do projeto, rode:

```bash
python route.py
```

Depois abra http://localhost:8080 no navegador.

## Rotas

| Rota | O que faz |
|---|---|
| `/` e `/inicio` | Página do Foco+ (`app/views/html/inicio.tpl`) |
| `/helper` | Página de ajuda original do BMVC |
| `/static/<arquivo>` | Entrega os arquivos estáticos (CSS, JS e imagens) |

## Estrutura (MVC)

```
├── route.py                        # rotas
└── app/
    ├── controllers/
    │   └── application.py          # controlador: escolhe qual página mostrar
    ├── models/                     # modelos (a página é estática)
    ├── views/html/
    │   └── inicio.tpl              # view: HTML da página
    └── static/
        ├── css/inicio.css          # estilos
        └── js/inicio.js            # cronômetro e lista de tarefas
```

Caminho de uma requisição: o navegador acessa `/inicio` → o `route.py` chama `ctl.render('inicio')` →
o controlador `Application` executa o método `inicio()` → que devolve o template `inicio.tpl` →
a página carrega o `inicio.css` e o `inicio.js` pela rota `/static`.

## Rodando com Docker (opcional)

```bash
docker build -t bmvci .
docker run -d -p 8080:8080 -v $(pwd):/bmeta bmvci
```
