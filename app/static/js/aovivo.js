// aovivo.js: recebe as novidades do servidor pelo WebSocket e atualiza o mural sem recarregar a página

document.addEventListener("DOMContentLoaded", function () {
    const socket = io(); // conecta no servidor do Foco+ (o Socket.IO usa WebSocket)
    const status = document.getElementById("status-conexao");

    socket.on("connect", function () {
        status.innerText = "● ao vivo";
        status.classList.add("online");
    });

    socket.on("disconnect", function () {
        status.innerText = "desconectado";
        status.classList.remove("online");
    });

    // o servidor manda o evento "mural" sempre que alguém faz alguma coisa
    socket.on("mural", function (dados) {
        document.getElementById("conectados").innerText = dados.conectados;
        document.getElementById("pomodoros-hoje").innerText = dados.pomodoros_hoje;

        const lista = document.getElementById("lista-atividades");
        lista.innerHTML = ""; // apaga a lista antiga

        if (dados.atividades.length === 0) {
            const vazio = document.createElement("li");
            vazio.className = "dica";
            vazio.innerText = "Nenhuma atividade ainda. Entre, crie uma tarefa ou registre um pomodoro!";
            lista.appendChild(vazio);
        }

        for (let i = 0; i < dados.atividades.length; i++) {
            const atividade = dados.atividades[i];
            const item = document.createElement("li");
            item.innerText = atividade.hora + " · " + atividade.nome + " " + atividade.texto;
            lista.appendChild(item);
        }

        // o cartão "pisca" para mostrar que chegou novidade
        const cartao = document.getElementById("ao-vivo");
        cartao.classList.add("piscar");
        setTimeout(function () {
            cartao.classList.remove("piscar");
        }, 800);
    });
});
