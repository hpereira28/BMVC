from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response


app = Bottle()
ctl = Application()


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


# CRUD de tarefas

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


if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True)
