<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Foco+ | Entrar</title>
    <link rel="stylesheet" type="text/css" href="/static/css/inicio.css">
    <link rel="stylesheet" type="text/css" href="/static/css/conta.css">
    <script src="/static/js/conta.js"></script>
</head>
<body class="foco">

    % include('app/views/html/cabecalho.tpl', estudante=estudante, subtitulo='Entre para ver as suas tarefas')

    <main class="estreito">
        <section class="cartao">
            <h2>Entrar</h2>

            % if mensagem:
            <p class="mensagem">{{mensagem}}</p>
            % end

            % if estudante:
            <p class="dica">Você já está logado como <strong>{{estudante.login}}</strong>.
                <a href="/tarefas">Ir para minhas tarefas</a></p>
            % end

            <form class="form-conta" action="/entrar" method="post" onsubmit="return validarLogin(this)">
                <label>Login
                    <input name="login" type="text" maxlength="30">
                </label>
                <label>Senha
                    <input class="campo-senha" name="senha" type="password" maxlength="50">
                </label>
                <label class="mostrar">
                    <input type="checkbox" onclick="mostrarSenha(this)"> Mostrar senha
                </label>
                <button type="submit">Entrar</button>
            </form>

            <p class="dica">Ainda não tem conta? <a href="/cadastro">Crie a sua aqui</a>.</p>
        </section>
    </main>

    <footer>
        Projeto de Orientação a Objetos · Henrique Pereira e Eduardo Mariz de Sousa
    </footer>

</body>
</html>
