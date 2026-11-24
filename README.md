# Foco+ (BMVC)

Aplicação web feita com o framework **BMVC** (arquitetura MVC com o servidor **Bottle**).
O **Foco+** ajuda estudantes a estudar com a técnica **Pomodoro**: tem um **cronômetro** com os modos
Foco (25 min), Pausa curta (5 min) e Pausa longa (15 min), **contas de estudante com login**, um
**CRUD completo de tarefas de estudo** em que cada estudante vê e altera só as próprias tarefas, e uma
**Sala de estudos ao vivo**, atualizada em tempo real por **WebSocket**.

Projeto da disciplina de **Orientação a Objetos**, Engenharia de Software.

## Como rodar

Instale as bibliotecas (só na primeira vez):

```bash
pip install -r requirements.txt
```

São três: `bottle` (servidor das páginas), `python-socketio` (WebSocket) e `eventlet` (deixa o servidor
atender várias conexões ao mesmo tempo).

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

## Tempo real (WebSocket)

As páginas **Início** e **Minhas tarefas** têm o cartão **"Sala de estudos ao vivo"**, que mostra:
quantas pessoas estão conectadas agora, quantos pomodoros todos os estudantes fizeram hoje e as últimas
atividades (ex.: "14:32 · Henrique fez um pomodoro de POO"). Tudo muda **sozinho, sem recarregar a página**.

Como funciona:

1. Ao abrir a página, o `aovivo.js` conecta no servidor com `io()` (biblioteca Socket.IO, que usa WebSocket).
2. Quando alguém entra, cria uma tarefa, faz um pomodoro ou conclui uma tarefa, o controlador chama
   `avisar()`, que guarda a atividade no `Mural` e faz `sio.emit('mural', ...)`.
3. O `emit` manda o evento **para todos os navegadores conectados ao mesmo tempo**.
4. No navegador, o `aovivo.js` recebe o evento com `socket.on('mural', ...)` e redesenha o cartão.
5. Ao abrir ou fechar uma página, os eventos `connect` e `disconnect` (no `route.py`) atualizam o número
   de conectados.

Para testar: abra o Foco+ em **dois navegadores** (ou numa janela anônima), com duas contas diferentes.
O que um faz aparece na hora no outro.

O mural mostra só a **matéria** da tarefa, nunca o título, para manter as tarefas de cada um privadas.
Ele fica em memória: reiniciando o servidor, o mural começa vazio.

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
| `aovivo.tpl`: cartão "Sala de estudos ao vivo", usado no início e nas tarefas | `inicio.css`, `aovivo.js` (WebSocket) |

- `conta.js`: valida o login e o cadastro (campos vazios, login com espaço, senha curta, senhas diferentes)
  e tem o "Mostrar senha".
- `tarefas.js`: não deixa salvar tarefa sem título e pede confirmação antes de excluir.
- `inicio.js`: cronômetro Pomodoro.
- `aovivo.js`: conecta no WebSocket e atualiza o mural ao vivo.

## Estrutura (MVC)

```
├── route.py                        # rotas HTTP, eventos do WebSocket e o servidor
└── app/
    ├── models/
    │   ├── estudante.py            # modelo Estudante
    │   ├── tarefa.py               # modelo Tarefa
    │   └── atividade.py            # modelo Atividade (o que aparece no mural)
    ├── controllers/
    │   ├── application.py          # controlador: páginas, login, CRUD e avisos do WebSocket
    │   ├── estudante_record.py     # EstudanteRecord: contas e sessões
    │   ├── tarefa_record.py        # TarefaRecord: salva e lê as tarefas no JSON
    │   ├── mural.py                # Mural: últimas atividades e pomodoros do dia
    │   └── db/                     # estudantes.json e tarefas.json (criados ao rodar)
    ├── views/html/
    │   ├── cabecalho.tpl
    │   ├── aovivo.tpl
    │   ├── inicio.tpl
    │   ├── entrar.tpl
    │   ├── cadastro.tpl
    │   ├── tarefas.tpl
    │   └── editar_tarefa.tpl
    └── static/
        ├── css/inicio.css, css/conta.css, css/tarefas.css
        └── js/inicio.js, js/conta.js, js/tarefas.js, js/aovivo.js
```

Relação entre as classes: o `Application` **compõe** um `TarefaRecord`, um `EstudanteRecord` e um `Mural`
(cria os três no `__init__`), e se **associa** ao servidor de WebSocket (`sio`), que é criado no `route.py`
e passado para ele. O `EstudanteRecord` guarda objetos `Estudante`, o `TarefaRecord` guarda objetos
`Tarefa` e o `Mural` guarda objetos `Atividade`.

## Rodando com Docker (opcional)

```bash
docker build -t bmvci .
docker run -d -p 8080:8080 -v $(pwd):/bmeta bmvci
```
