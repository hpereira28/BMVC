// tarefas.js: validação do formulário e confirmação de exclusão

// não deixa enviar uma tarefa sem título
function validarTarefa(formulario) {
    const titulo = formulario.titulo.value.trim();
    if (titulo === "") {
        alert("Digite o título da tarefa.");
        return false; // cancela o envio do formulário
    }
    return true;
}

// pergunta antes de excluir
function confirmarExclusao() {
    return confirm("Tem certeza que deseja excluir esta tarefa?");
}
