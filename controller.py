from datetime import datetime
import requests
import json


def gerarProva(prova, ano, fase, materia, nQuestoes):
    body = {"prova": prova, "ano": ano, "fase": fase,
            "materia": materia, "numero_questoes": nQuestoes}

    req = requests.post("http://localhost:8090/api/v1/gerarprova", json=body)
    return req.json()


def tratarProva(prova):
    gabaritos = prova["gabaritos"]
    questoes = prova["questoes"]
    respostas = prova["respostas"]

    for q in questoes:
        img = q["imagem"]
        if img:
            q["enunciado"] = q["enunciado"].replace(
                "\L", f"<img src='../static/img/{img}.jpg'/>")

    for res in respostas:
        for r in res:

            img = r["imagem"]
            if img:
                r["enunciado"] = r["enunciado"].replace(
                    "\L", f"<img src='../static/img/{img}.jpg'/>")

    return {"gabaritos": gabaritos, "questoes": questoes, "respostas": respostas}


def corrigirProva(usuario, gabaritos, respostas_usuario):
    body = {"usuario": usuario['id'], "gabaritos": gabaritos,
            "respostas_usuario": respostas_usuario}

    req = requests.post(
        "http://localhost:8090/api/v1/corrigirprova", json=body)
    return req.json()


def cadastrarUsuario(nome, email, senha):

    body = {"nome": nome, "email": email,
            "senha": senha}

    req = requests.post(
        "http://localhost:8080/api/v1/inserir/usuario", json=body)
    return req.json()


def realizarLogin(email, senha):
    body = {"email": email,
            "senha": senha}

    req = requests.post(
        "http://localhost:8080/api/v1/login", json=body)
    return req.json()


def getGraficos(usuario):

    dados = getAcertos(usuario)
    acertos = [i['materia'] for i in dados if i['acerto']]
    erros = [i['materia'] for i in dados if not i['acerto']]
    acertosData = [datetime.strptime(
        i['data'], '%a, %d %b %Y %H:%M:%S %Z') for i in dados if i['acerto']]
    errosData = [datetime.strptime(i['data'], '%a, %d %b %Y %H:%M:%S %Z')
                 for i in dados if not i['acerto']]
    provasRealizadas = len(list(set([datetime.strptime(
        i['data'], '%a, %d %b %Y %H:%M:%S %Z') for i in dados])))

    materias = ["BIOLOGIA", "FILOSOFIA - SOCIOLOGIA", "FISICA", "GEOGRAFIA",
                "HISTORIA", "INGLES", "MATEMATICA", "PORTUGUES", "QUIMICA"]
    meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    acertosMateria = [acertos.count(i) for i in materias]
    errosMateria = [erros.count(i) for i in materias]

    acertosMes = [i.month for i in acertosData]
    errosMes = [i.month for i in errosData]

    acertosMesCount = [acertosMes.count(i) for i in meses]
    errosMesCount = [errosMes.count(i) for i in meses]

    acertosDia = len(
        [i for i in acertosData if i.date() == datetime.now().date()])
    errosDia = len([i for i in errosData if i.date() == datetime.now().date()])

    acertos = len(acertos)
    erros = len(erros)
    graficos = {"acertos": acertos, "erros": erros, "provasRealizadas": provasRealizadas, "acertosMateria": acertosMateria,
                "errosMateria": errosMateria, "acertosMes": acertosMesCount, "errosMes": errosMesCount, "acertosDia": acertosDia, "errosDia": errosDia}
    return graficos


def getAcertos(usuario):
    body = {"usuario": usuario['id']}

    req = requests.post(
        "http://localhost:8090/api/v1/dadosgraficos", json=body)
    return req.json()
