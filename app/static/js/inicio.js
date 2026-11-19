// inicio.js: cronômetro Pomodoro e lista de tarefas

let segundos = 25 * 60;
let intervalo = null;
let ciclos = 0;
let modo = "foco";

// ---------- cronômetro ----------

function atualizarVisor() {
    const minutos = Math.floor(segundos / 60);
    const resto = segundos % 60;
    document.getElementById("visor").innerText =
        String(minutos).padStart(2, "0") + ":" + String(resto).padStart(2, "0");
}

function mudarModo(novoModo) {
    pausar();
    modo = novoModo;
    const legenda = document.getElementById("legenda");

    if (modo === "foco") {
        segundos = 25 * 60;
        legenda.innerText = "Hora de focar!";
    } else if (modo === "curta") {
        segundos = 5 * 60;
        legenda.innerText = "Pausa curta: descanse um pouco";
    } else {
        segundos = 15 * 60;
        legenda.innerText = "Pausa longa: você merece!";
    }

    document.body.className = modo; // o CSS troca a cor da página
    atualizarVisor();
}

function iniciar() {
    if (intervalo !== null) {
        return; // já está rodando
    }
    document.getElementById("visor").classList.add("rodando");
    intervalo = setInterval(function () {
        segundos--;
        atualizarVisor();
        if (segundos === 0) {
            tempoEsgotado();
        }
    }, 1000);
}

function pausar() {
    clearInterval(intervalo);
    intervalo = null;
    document.getElementById("visor").classList.remove("rodando");
}

function zerar() {
    mudarModo(modo);
}

function tempoEsgotado() {
    pausar();
    if (modo === "foco") {
        ciclos++;
        document.getElementById("ciclos").innerText = ciclos;
        if (ciclos % 4 === 0) {
            alert("4 ciclos concluídos! Faça uma pausa longa.");
            mudarModo("longa");
        } else {
            alert("Ciclo concluído! Faça uma pausa curta.");
            mudarModo("curta");
        }
    } else {
        alert("A pausa acabou. Hora de voltar a focar!");
        mudarModo("foco");
    }
}

// ---------- lista de tarefas ----------

function adicionarTarefa() {
    const campo = document.getElementById("nova-tarefa");
    const texto = campo.value.trim();
    if (texto === "") {
        alert("Digite o nome da tarefa.");
        return;
    }

    const item = document.createElement("li");
    item.innerText = texto;
    item.onclick = function () {
        item.classList.toggle("feita"); // clique para marcar ou desmarcar
    };

    document.getElementById("lista-tarefas").appendChild(item);
    campo.value = "";
}
