# Foco+ (BMVC)

Aplicação web feita com o framework **BMVC** (arquitetura MVC com o servidor **Bottle**).
O **Foco+** ajuda estudantes a estudar com a técnica **Pomodoro**: tem um **cronômetro** com os modos
Foco (25 min), Pausa curta (5 min) e Pausa longa (15 min), **contas de estudante com login**, e um
**CRUD completo de tarefas de estudo** em que cada estudante vê e altera só as próprias tarefas.

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

Depois abra http://localhost:8080 no navegador, clique em **Criar conta** e depois em **Entrar**.

## Modelos

`Estudante` (`app/models/estudante.py`): a conta de um estudante.

| Atributo | O que guarda |
|---|---|
| `nome` | nome do estudante |
| `login` | nome de usuário (único, sem espaços) |
| `senha_hash` | a senha transformada em código (hash SHA-256), para não guardar a senha de verdade |

Métodos: `confere_senha(senha)` e `primeiro_nome()`.

`Tarefa` (`app/models/tarefa.py`): uma tarefa de estudo.

| Atributo | O que guarda |
|---|---|
| `id` | número da tarefa |
| `dono` | login do estudante dono da tarefa |
| `titulo` | o que vai ser estudado |
| `materia` | a matéria da tarefa |
| `pomodoros` | quantos pomodoros a tarefa deve levar |
| `feitos` | quantos pomodoros já foram feitos |
| `concluida` | se a tarefa já terminou |

Métodos: `registrar_pomodoro()`, `alternar_concluida()`, `progresso()` (porcentagem) e `status()`
("A fazer", "Em andamento" ou "Concluída").

Os dados ficam salvos em arquivos JSON na pasta `app/controllers/db/`, criados ao rodar:
`estudantes.json` (classe `EstudanteRecord`) e `tarefas.json` (classe `TarefaRecord`).

## Controle de acesso (login)

1. Em **Criar conta** (`/cadastro`) o estudante escolhe nome, login e senha.
2. Em **Entrar** (`/entrar`) o `EstudanteRecord` confere o login e a senha e cria um `session_id`
   (código aleatório gerado com `uuid`), que fica guardado num **cookie** do navegador por 1 hora.
3. A cada página, o controlador lê o cookie e descobre quem está logado (`estudante_logado()`).
4. As páginas de tarefas são **restritas**: sem login, o método `exigir_login()` manda para `/entrar`.
5. Cada tarefa tem um **dono**: um estudante não vê, não edita e não exclui tarefas de outro.
6. **Sair** (`/sair`) apaga a sessão e o cookie.

## Rotas

| Rota | O que faz | Acesso |
|---|---|---|
| `GET /` e `/inicio` | cronômetro (e as tarefas pendentes, se estiver logado) | público |
| `GET /cadastro` e `POST /cadastro` | página e envio do cadastro | público |
| `GET /entrar` e `POST /entrar` | página e envio do login | público |
| `POST /sair` | logout | público |
| `GET /tarefas` | **Read**: lista as tarefas do estudante | restrito |
| `POST /tarefas/nova` | **Create**: cadastra uma tarefa | restrito |
| `GET /tarefas/editar/<id>` | **Read**: mostra uma tarefa no formulário de edição | restrito |
| `POST /tarefas/editar/<id>` | **Update**: salva as alterações | restrito |
| `POST /tarefas/pomodoro/<id>` | **Update**: soma 1 pomodoro feito | restrito |
| `POST /tarefas/concluir/<id>` | **Update**: marca como concluída ou reabre | restrito |
| `POST /tarefas/excluir/<id>` | **Delete**: exclui a tarefa | restrito |
| `GET /helper` | página de ajuda original do BMVC | público |

## Páginas, CSS e JS

| Template | CSS e JS |
|---|---|
| `inicio.tpl`: cronômetro e tarefas pendentes | `inicio.css`, `inicio.js` (cronômetro) |
| `entrar.tpl` e `cadastro.tpl`: login e criação de conta | `inicio.css`, `conta.css`, `conta.js` |
| `tarefas.tpl` e `editar_tarefa.tpl`: CRUD de tarefas | `inicio.css`, `tarefas.css`, `tarefas.js` |
| `cabecalho.tpl`: cabeçalho usado em todas as páginas (com Entrar ou "Olá, nome" e Sair) | |

- `conta.js`: valida o login e o cadastro (campos vazios, login com espaço, senha curta, senhas diferentes)
  e tem o "Mostrar senha".
- `tarefas.js`: não deixa salvar tarefa sem título e pede confirmação antes de excluir.
- `inicio.js`: cronômetro Pomodoro.

## Estrutura (MVC)

```
├── route.py                        # rotas (recebem as requisições HTTP)
└── app/
    ├── models/
    │   ├── estudante.py            # modelo Estudante
    │   └── tarefa.py               # modelo Tarefa
    ├── controllers/
    │   ├── application.py          # controlador: páginas, login e ações do CRUD
    │   ├── estudante_record.py     # EstudanteRecord: contas e sessões
    │   ├── tarefa_record.py        # TarefaRecord: salva e lê as tarefas no JSON
    │   └── db/                     # estudantes.json e tarefas.json (criados ao rodar)
    ├── views/html/
    │   ├── cabecalho.tpl
    │   ├── inicio.tpl
    │   ├── entrar.tpl
    │   ├── cadastro.tpl
    │   ├── tarefas.tpl
    │   └── editar_tarefa.tpl
    └── static/
        ├── css/inicio.css, css/conta.css, css/tarefas.css
        └── js/inicio.js, js/conta.js, js/tarefas.js
```

Relação entre as classes: o `Application` **compõe** um `TarefaRecord` e um `EstudanteRecord`
(cria os dois no `__init__`). O `EstudanteRecord` guarda a lista de objetos `Estudante` e o
`TarefaRecord` guarda a lista de objetos `Tarefa`.

## Rodando com Docker (opcional)

```bash
docker build -t bmvci .
docker run -d -p 8080:8080 -v $(pwd):/bmeta bmvci
```
