from flask import Flask, app, render_template, request, redirect, url_for
from controller import gerarProva, getGraficos, tratarProva, corrigirProva, cadastrarUsuario, realizarLogin
import ast

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@app.route('/cadastrar', methods=["POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirma_senha = request.form.get("confirmar_senha")

        if not senha == confirma_senha:
            return redirect(url_for('cadastrar'))
        cadastrarUsuario(nome, email, senha)

    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/logar', methods=["POST"])
def logar():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        usuario = realizarLogin(email, senha)
        if not 'id' in usuario:
            return redirect(url_for('login'))

    return redirect(url_for('home', usuario=usuario))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        usuario = ast.literal_eval(request.form['usuario'])
    else:
        usuario = ast.literal_eval(request.args['usuario'])

    dados = getGraficos(usuario)

    return render_template('home.html', usuario=usuario, dados=dados)


@app.route('/prova', methods=["GET", "POST"])
def prova():
    if request.method == "POST":
        usuario = ast.literal_eval(request.form["usuario"])
        prova = request.form["prova"]
        ano = request.form["ano"]
        fase = request.form["fase"]
        nQuestoes = request.form["qtdquestoes"]
        materia = request.form.getlist("materia")
        prova_gerada = gerarProva(
            prova=prova, ano=ano, fase=fase, nQuestoes=nQuestoes, materia=materia)
        prova_gerada = tratarProva(prova_gerada)
    return render_template('questoes.html', prova=prova_gerada, usuario=usuario)


@app.route('/correcao', methods=["POST"])
def correcao():
    usuario = ast.literal_eval(request.form["usuario"])
    prova = ast.literal_eval(request.form["prova"])
    gabaritos = prova["gabaritos"]
    respostas_usuario = []
    for g in gabaritos:
        questao_id = g["questao_id"]
        resp = request.form.get(f"resposta_{questao_id}")
        respostas_usuario.append(
            {"questao_id": questao_id, "alternativa": resp})

    prova_corrigida = corrigirProva(usuario, gabaritos, respostas_usuario)

    return render_template('correcao.html', prova=prova, respostas_usuario=respostas_usuario, correcao=prova_corrigida, usuario=usuario)


app.run()
