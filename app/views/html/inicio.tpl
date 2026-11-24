<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Foco+ | Pomodoro para estudantes</title>
    <link rel="stylesheet" type="text/css" href="/static/css/inicio.css">
    <script src="/static/js/inicio.js"></script>
    <!-- biblioteca do Socket.IO (WebSocket) e o nosso script do mural ao vivo -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.5/socket.io.min.js"></script>
    <script src="/static/js/aovivo.js"></script>
</head>
<body class="foco">

    % include('app/views/html/cabecalho.tpl', estudante=estudante, subtitulo='Cronômetro Pomodoro para estudar com mais foco')

    <main>
        <section class="cartao">
            <h2>Como funciona</h2>
            <ol>
                <li>Crie a sua conta e cadastre o que você vai estudar em "Minhas tarefas".</li>
                <li>Inicie o cronômetro e foque por 25 minutos.</li>
                <li>Quando o tempo acabar, registre o pomodoro na tarefa e faça uma pausa curta de 5 minutos.</li>
                <li>A cada 4 ciclos de foco, faça uma pausa longa de 15 minutos.</li>
            </ol>
        </section>

        <section class="cartao centro">
            <h2>Cronômetro</h2>
            <div class="modos">
                <button class="modo modo-foco" onclick="mudarModo('foco')">Foco</button>
                <button class="modo modo-curta" onclick="mudarModo('curta')">Pausa curta</button>
                <button class="modo modo-longa" onclick="mudarModo('longa')">Pausa longa</button>
            </div>
            <p id="legenda">Hora de focar!</p>
            <div id="visor" class="visor">25:00</div>
            <button onclick="iniciar()">Iniciar</button>
            <button onclick="pausar()">Pausar</button>
            <button onclick="zerar()">Zerar</button>
            <p>Ciclos de foco concluídos: <strong id="ciclos">0</strong></p>
        </section>

        <section class="cartao">
            % if estudante:
            <h2>Suas tarefas pendentes</h2>
                % if pendentes:
                <ul class="pendentes">
                    % for tarefa in pendentes:
                    <li>
                        <strong>{{tarefa.titulo}}</strong>
                        <span>{{tarefa.materia}} · {{tarefa.feitos}} de {{tarefa.pomodoros}} pomodoros</span>
                    </li>
                    % end
                </ul>
                % else:
                <p class="dica">Nenhuma tarefa pendente. Cadastre uma em "Minhas tarefas".</p>
                % end
            <a class="link-botao" href="/tarefas">Gerenciar tarefas</a>
            % else:
            <h2>Suas tarefas</h2>
            <p class="dica">Entre na sua conta para cadastrar e acompanhar as suas tarefas de estudo.</p>
            <a class="link-botao" href="/entrar">Entrar</a>
            <a class="link-botao secundario" href="/cadastro">Criar conta</a>
            % end
        </section>

        % include('app/views/html/aovivo.tpl')
    </main>

    <footer>
        Projeto de Orientação a Objetos · Henrique Pereira e Eduardo Mariz de Sousa
    </footer>

</body>
</html>
