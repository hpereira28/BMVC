<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Foco+ | Editar tarefa</title>
    <link rel="stylesheet" type="text/css" href="/static/css/inicio.css">
    <link rel="stylesheet" type="text/css" href="/static/css/tarefas.css">
    <script src="/static/js/tarefas.js"></script>
</head>
<body class="foco">

    % include('app/views/html/cabecalho.tpl', estudante=estudante, subtitulo='Editar tarefa')

    <main>
        <section class="cartao">
            <h2>Editar: {{tarefa.titulo}}</h2>
            <form class="form-tarefa" action="/tarefas/editar/{{tarefa.id}}" method="post"
                  onsubmit="return validarTarefa(this)">
                <label>Título
                    <input name="titulo" type="text" value="{{tarefa.titulo}}" maxlength="80">
                </label>
                <label>Matéria
                    <input name="materia" type="text" value="{{tarefa.materia}}" maxlength="40">
                </label>
                <label>Pomodoros
                    <input name="pomodoros" type="number" min="1" max="20" value="{{tarefa.pomodoros}}">
                </label>
                <div>
                    <button type="submit">Salvar</button>
                    <a class="link-botao secundario" href="/tarefas">Cancelar</a>
                </div>
            </form>
            <p class="dica">Pomodoros já feitos nesta tarefa: {{tarefa.feitos}}</p>
        </section>
    </main>

    <footer>
        Projeto de Orientação a Objetos · Henrique Pereira e Eduardo Mariz de Sousa
    </footer>

</body>
</html>
