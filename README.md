# Foco+ (BMVC)

Aplicação web feita com o framework **BMVC** (arquitetura MVC com o servidor **Bottle**).
O **Foco+** ajuda estudantes a estudar com a técnica **Pomodoro**: tem um **cronômetro** com os modos
Foco (25 min), Pausa curta (5 min) e Pausa longa (15 min), e um **CRUD completo de tarefas de estudo**,
onde cada tarefa conta quantos pomodoros já foram feitos.

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

## Modelo

`Tarefa` (`app/models/tarefa.py`): uma tarefa de estudo.

| Atributo | O que guarda |
|---|---|
| `id` | número da tarefa |
| `titulo` | o que vai ser estudado |
| `materia` | a matéria da tarefa |
| `pomodoros` | quantos pomodoros a tarefa deve levar |
| `feitos` | quantos pomodoros já foram feitos |
| `concluida` | se a tarefa já terminou |

Métodos: `registrar_pomodoro()`, `alternar_concluida()`, `progresso()` (porcentagem) e `status()`
("A fazer", "Em andamento" ou "Concluída").

As tarefas ficam salvas no arquivo `app/controllers/db/tarefas.json`, criado pela classe `TarefaRecord`
(`app/controllers/tarefa_record.py`) na primeira tarefa cadastrada.

## CRUD

| Operação | Rota | O que faz |
|---|---|---|
| **Create** | `POST /tarefas/nova` | cadastra uma tarefa |
| **Read** | `GET /tarefas` | lista todas as tarefas |
| **Read** | `GET /tarefas/editar/<id>` | mostra uma tarefa no formulário de edição |
| **Update** | `POST /tarefas/editar/<id>` | salva as alterações da tarefa |
| **Update** | `POST /tarefas/pomodoro/<id>` | soma 1 pomodoro feito |
| **Update** | `POST /tarefas/concluir/<id>` | marca como concluída ou reabre |
| **Delete** | `POST /tarefas/excluir/<id>` | exclui a tarefa |

## Páginas

| Rota | Template | CSS e JS |
|---|---|---|
| `/` e `/inicio` | `inicio.tpl`: cronômetro e tarefas pendentes | `inicio.css`, `inicio.js` (cronômetro) |
| `/tarefas` | `tarefas.tpl`: cadastro e lista de tarefas | `inicio.css`, `tarefas.css`, `tarefas.js` |
| `/tarefas/editar/<id>` | `editar_tarefa.tpl`: edição de uma tarefa | `inicio.css`, `tarefas.css`, `tarefas.js` |
| `/helper` | `helper.tpl`: página de ajuda original do BMVC | `helper.css`, `helper.js` |

O `tarefas.js` valida o formulário (não deixa salvar tarefa sem título) e pede confirmação antes de excluir.

## Estrutura (MVC)

```
├── route.py                        # rotas (recebem as requisições HTTP)
└── app/
    ├── models/
    │   └── tarefa.py               # modelo Tarefa
    ├── controllers/
    │   ├── application.py          # controlador: escolhe a página e trata as ações
    │   ├── tarefa_record.py        # TarefaRecord: salva e lê as tarefas no JSON
    │   └── db/                     # arquivo tarefas.json (criado ao rodar)
    ├── views/html/
    │   ├── inicio.tpl
    │   ├── tarefas.tpl
    │   └── editar_tarefa.tpl
    └── static/
        ├── css/inicio.css, css/tarefas.css
        └── js/inicio.js, js/tarefas.js
```

Caminho de uma requisição: o navegador envia o formulário para `/tarefas/nova` → o `route.py` lê os campos e
chama `ctl.criar_tarefa(...)` → o controlador `Application` valida e chama o `TarefaRecord` → que cria o objeto
`Tarefa` e salva no JSON → a rota redireciona para `/tarefas`, que mostra a lista atualizada.

Relação entre as classes: o `Application` **compõe** um `TarefaRecord` (cria no `__init__`),
e o `TarefaRecord` guarda a lista de objetos `Tarefa`.

## Rodando com Docker (opcional)

```bash
docker build -t bmvci .
docker run -d -p 8080:8080 -v $(pwd):/bmeta bmvci
```
