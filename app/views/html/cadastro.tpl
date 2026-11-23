<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Foco+ | Criar conta</title>
    <link rel="stylesheet" type="text/css" href="/static/css/inicio.css">
    <link rel="stylesheet" type="text/css" href="/static/css/conta.css">
    <script src="/static/js/conta.js"></script>
</head>
<body class="foco">

    % include('app/views/html/cabecalho.tpl', estudante=estudante, subtitulo='Crie a sua conta de estudante')

    <main class="estreito">
        <section class="cartao">
            <h2>Criar conta</h2>

            % if mensagem:
            <p class="mensagem">{{mensagem}}</p>
            % end

            <form class="form-conta" action="/cadastro" method="post" onsubmit="return validarCadastro(this)">
                <label>Nome
                    <input name="nome" type="text" maxlength="60">
                </label>
                <label>Login (sem espaços)
                    <input name="login" type="text" maxlength="30">
                </label>
                <label>Senha (pelo menos 4 caracteres)
                    <input class="campo-senha" name="senha" type="password" maxlength="50">
                </label>
                <label>Confirme a senha
                    <input class="campo-senha" name="confirmacao" type="password" maxlength="50">
                </label>
                <label class="mostrar">
                    <input type="checkbox" onclick="mostrarSenha(this)"> Mostrar senha
                </label>
                <button type="submit">Criar conta</button>
            </form>

            <p class="dica">Já tem conta? <a href="/entrar">Entre aqui</a>.</p>
        </section>
    </main>

    <footer>
        Projeto de Orientação a Objetos · Henrique Pereira e Eduardo Mariz de Sousa
    </footer>

</body>
</html>
