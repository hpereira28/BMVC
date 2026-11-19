<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Foco+ | Pomodoro para estudantes</title>
    <link rel="stylesheet" type="text/css" href="/static/css/inicio.css">
    <script src="/static/js/inicio.js"></script>
</head>
<body class="foco">

    <header>
        <h1>🍅 Foco+</h1>
        <p>Cronômetro Pomodoro para estudar com mais foco</p>
    </header>

    <main>
        <section class="cartao">
            <h2>Como funciona</h2>
            <ol>
                <li>Escolha o que você vai estudar e anote na lista de tarefas.</li>
                <li>Inicie o cronômetro e foque por 25 minutos.</li>
                <li>Quando o tempo acabar, faça uma pausa curta de 5 minutos.</li>
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
            <h2>Tarefas de hoje</h2>
            <form onsubmit="adicionarTarefa(); return false;">
                <input id="nova-tarefa" type="text" placeholder="Ex.: Revisar herança e polimorfismo">
                <button type="submit">Adicionar</button>
            </form>
            <ul id="lista-tarefas"></ul>
            <p class="dica">Clique em uma tarefa para marcá-la como feita.</p>
        </section>
    </main>

    <footer>
        Projeto de Orientação a Objetos · Henrique Pereira e Eduardo Mariz de Sousa
    </footer>

</body>
</html>
