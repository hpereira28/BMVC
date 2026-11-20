<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Foco+ | Minhas tarefas</title>
    <link rel="stylesheet" type="text/css" href="/static/css/inicio.css">
    <link rel="stylesheet" type="text/css" href="/static/css/tarefas.css">
    <script src="/static/js/tarefas.js"></script>
</head>
<body class="foco">

    <header>
        <h1>🍅 Foco+</h1>
        <p>Organize o que você vai estudar</p>
        <nav>
            <a href="/inicio">Cronômetro</a>
            <a href="/tarefas">Minhas tarefas</a>
        </nav>
    </header>

    <main class="largo">
        <section class="cartao">
            <h2>Nova tarefa</h2>
            <form class="form-tarefa" action="/tarefas/nova" method="post" onsubmit="return validarTarefa(this)">
                <label>Título
                    <input name="titulo" type="text" placeholder="Ex.: Revisar herança" maxlength="80">
                </label>
                <label>Matéria
                    <input name="materia" type="text" placeholder="Ex.: Orientação a Objetos" maxlength="40">
                </label>
                <label>Pomodoros
                    <input name="pomodoros" type="number" min="1" max="20" value="2">
                </label>
                <button type="submit">Adicionar</button>
            </form>
        </section>

        <section class="cartao">
            <h2>Minhas tarefas</h2>
            % if tarefas:
            <table>
                <thead>
                    <tr>
                        <th>Tarefa</th>
                        <th>Matéria</th>
                        <th>Pomodoros</th>
                        <th>Status</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    % for tarefa in tarefas:
                    <tr class="{{'feita' if tarefa.concluida else ''}}">
                        <td>{{tarefa.titulo}}</td>
                        <td>{{tarefa.materia}}</td>
                        <td>
                            {{tarefa.feitos}} de {{tarefa.pomodoros}}
                            <div class="barra"><div class="preenchida" style="width: {{tarefa.progresso()}}%"></div></div>
                        </td>
                        <td>{{tarefa.status()}}</td>
                        <td class="acoes">
                            <form action="/tarefas/pomodoro/{{tarefa.id}}" method="post">
                                <button type="submit" title="Registrar um pomodoro feito">+1 🍅</button>
                            </form>
                            <form action="/tarefas/concluir/{{tarefa.id}}" method="post">
                                <button type="submit">{{'Reabrir' if tarefa.concluida else 'Concluir'}}</button>
                            </form>
                            <a class="link-botao" href="/tarefas/editar/{{tarefa.id}}">Editar</a>
                            <form action="/tarefas/excluir/{{tarefa.id}}" method="post"
                                  onsubmit="return confirmarExclusao()">
                                <button type="submit" class="perigo">Excluir</button>
                            </form>
                        </td>
                    </tr>
                    % end
                </tbody>
            </table>
            % else:
            <p class="dica">Nenhuma tarefa cadastrada ainda. Use o formulário acima!</p>
            % end
        </section>
    </main>

    <footer>
        Projeto de Orientação a Objetos · Henrique Pereira e Eduardo Mariz de Sousa
    </footer>

</body>
</html>
