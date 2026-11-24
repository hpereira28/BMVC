# esconde o aviso "Eventlet is deprecated" que aparece ao iniciar (ele não atrapalha o funcionamento)
import warnings
warnings.filterwarnings("ignore", message=r"\s*Eventlet is deprecated")

# o eventlet precisa vir antes de tudo: ele deixa o servidor atender várias conexões ao mesmo tempo
import eventlet
eventlet.monkey_patch()

from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response
import eventlet.wsgi
import socketio


app = Bottle()
sio = socketio.Server(async_mode='eventlet')  # servidor de WebSocket (Socket.IO)
ctl = Application(sio)


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')


#-----------------------------------------------------------------------------
# Suas rotas aqui:

@app.route('/', method='GET')
@app.route('/inicio', method='GET')
def action_inicio():
    return ctl.render('inicio')


# Login, cadastro e logout

@app.route('/entrar', method='GET')
def action_entrar():
    if request.query.get('novo'):
        return ctl.render('entrar', 'Conta criada! Agora é só entrar.')
    return ctl.render('entrar')


@app.route('/entrar', method='POST')
def action_autenticar():
    login = request.forms.getunicode('login', '')
    senha = request.forms.getunicode('senha', '')
    session_id = ctl.autenticar(login, senha)
    if session_id:
        # guarda o código da sessão no navegador por 1 hora
        # httponly=True: o JavaScript da página não consegue ler esse cookie
        response.set_cookie('session_id', session_id, httponly=True, max_age=3600)
        redirect('/tarefas')
    return ctl.render('entrar', 'Login ou senha incorretos.')


@app.route('/cadastro', method='GET')
def action_cadastro():
    return ctl.render('cadastro')


@app.route('/cadastro', method='POST')
def action_cadastrar():
    nome = request.forms.getunicode('nome', '')
    login = request.forms.getunicode('login', '')
    senha = request.forms.getunicode('senha', '')
    confirmacao = request.forms.getunicode('confirmacao', '')
    erro = ctl.cadastrar(nome, login, senha, confirmacao)
    if erro:
        return ctl.render('cadastro', erro)
    redirect('/entrar?novo=1')


@app.route('/sair', method='POST')
def action_sair():
    ctl.sair()
    response.delete_cookie('session_id')
    redirect('/inicio')


# CRUD de tarefas (páginas restritas: o controlador exige login)

@app.route('/tarefas', method='GET')
def action_tarefas():
    return ctl.render('tarefas')                      # Read (lista)


@app.route('/tarefas/nova', method='POST')
def action_nova_tarefa():
    # getunicode lê o texto do formulário com acentos certinhos
    titulo = request.forms.getunicode('titulo', '')
    materia = request.forms.getunicode('materia', '')
    pomodoros = request.forms.get('pomodoros')
    ctl.criar_tarefa(titulo, materia, pomodoros)      # Create
    redirect('/tarefas')


@app.route('/tarefas/editar/<id>', method='GET')
def action_editar_tarefa(id):
    return ctl.render('editar_tarefa', id)            # Read (uma tarefa)


@app.route('/tarefas/editar/<id>', method='POST')
def action_salvar_tarefa(id):
    titulo = request.forms.getunicode('titulo', '')
    materia = request.forms.getunicode('materia', '')
    pomodoros = request.forms.get('pomodoros')
    ctl.atualizar_tarefa(id, titulo, materia, pomodoros)  # Update
    redirect('/tarefas')


@app.route('/tarefas/excluir/<id>', method='POST')
def action_excluir_tarefa(id):
    ctl.excluir_tarefa(id)                            # Delete
    redirect('/tarefas')


@app.route('/tarefas/pomodoro/<id>', method='POST')
def action_pomodoro_tarefa(id):
    ctl.registrar_pomodoro(id)                        # Update (+1 pomodoro)
    redirect('/tarefas')


@app.route('/tarefas/concluir/<id>', method='POST')
def action_concluir_tarefa(id):
    ctl.alternar_tarefa(id)                           # Update (concluir/reabrir)
    redirect('/tarefas')


#-----------------------------------------------------------------------------
# Eventos do WebSocket:

@sio.event
def connect(sid, environ):
    ctl.cliente_conectou()          # alguém abriu uma página do Foco+


@sio.event
def disconnect(sid):
    ctl.cliente_desconectou()       # alguém fechou a página


#-----------------------------------------------------------------------------


if __name__ == '__main__':

    # junta o Bottle (páginas) com o Socket.IO (WebSocket) num servidor só
    servidor = socketio.WSGIApp(sio, app)
    print("Foco+ rodando em http://localhost:8080")
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8080)), servidor)
