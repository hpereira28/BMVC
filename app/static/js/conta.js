// conta.js: validação dos formulários de login e cadastro, e o "Mostrar senha"

// mostra ou esconde o texto dos campos de senha
function mostrarSenha(caixa) {
    const campos = document.querySelectorAll(".campo-senha");
    for (let i = 0; i < campos.length; i++) {
        if (caixa.checked) {
            campos[i].type = "text";
        } else {
            campos[i].type = "password";
        }
    }
}

// não deixa tentar entrar com campo vazio
function validarLogin(formulario) {
    if (formulario.login.value.trim() === "" || formulario.senha.value === "") {
        alert("Digite o login e a senha.");
        return false; // cancela o envio do formulário
    }
    return true;
}

// confere os campos antes de criar a conta
function validarCadastro(formulario) {
    const nome = formulario.nome.value.trim();
    const login = formulario.login.value.trim();
    const senha = formulario.senha.value;
    const confirmacao = formulario.confirmacao.value;

    if (nome === "" || login === "" || senha === "") {
        alert("Preencha todos os campos.");
        return false;
    }
    if (login.includes(" ")) {
        alert("O login não pode ter espaços.");
        return false;
    }
    if (senha.length < 4) {
        alert("A senha precisa ter pelo menos 4 caracteres.");
        return false;
    }
    if (senha !== confirmacao) {
        alert("As senhas não são iguais.");
        return false;
    }
    return true;
}
