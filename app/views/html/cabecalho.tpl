    <header>
        <h1>🍅 Foco+</h1>
        <p>{{subtitulo}}</p>
        <nav>
            <a href="/inicio">Cronômetro</a>
            <a href="/tarefas">Minhas tarefas</a>
            % if estudante:
            <span class="ola">Olá, {{estudante.primeiro_nome()}}!</span>
            <form class="form-sair" action="/sair" method="post">
                <button type="submit">Sair</button>
            </form>
            % else:
            <a href="/entrar">Entrar</a>
            <a href="/cadastro">Criar conta</a>
            % end
        </nav>
    </header>
