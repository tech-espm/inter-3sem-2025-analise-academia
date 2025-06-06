from flask import Flask, render_template, json, request, Response
import config
import requests
from datetime import datetime, timedelta
import banco

app = Flask(__name__)

@app.get('/dashboard')
def dashboard():
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/dashboard.html', hoje=hoje)

@app.get('/')
def index():
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/index.html', hoje=hoje)

@app.get('/sobre')
def sobre():
    return render_template('index/sobre.html', titulo='Sobre Nós')

@app.get('/tempoReal')
def tempoReal():
    return render_template('index/tempoReal.html', titulo='Monitoramento em Tempo Real')

@app.get('/login')
def login():
    return render_template('index/login.html', titulo='Login', esconder_layout=True)

@app.get('/cadastrar')
def cadastrar():
    return render_template('index/cadastrar.html', titulo='Cadastrar', esconder_layout=True)

@app.get('/adm-log')
def admLog():
    return render_template('index/adm-log.html', titulo="Adm Logs")

@app.get('/consolidado')
def consolidado():
    data_inicial = (datetime.today() + timedelta(days=-19)).strftime('%Y-%m-%d')
    data_final = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/consolidado.html', titulo="Consolidado", data_inicial=data_inicial, data_final=data_final)

@app.get('/graficos')
def graficos():
    data_inicial = (datetime.today() + timedelta(days=-19)).strftime('%Y-%m-%d')
    data_final = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/graficos.html', titulo="Gráficos", data_inicial=data_inicial, data_final=data_final)

@app.route("/obterDadosConsolidadoOcupacaoMaxima")
def obterDadosConsolidadoOcupacaoMaxima():
    data_inicial = request.args.get('data_inicial')
    data_final = request.args.get('data_final')
    id_sensor = request.args.get('id_sensor')

    if not data_inicial or not data_final or not id_sensor:
        return json.jsonify({"erro": "Parâmetros obrigatórios não informados."}), 400

    # Obter o maior id do banco
    maior_id = banco.obterIdMaximo("pca")

    resultado = requests.get(f'{config.url_api}?sensor=pca&id_inferior={maior_id}')
    dados_novos = resultado.json()

	# Inserir os dados novos no banco
    if dados_novos and len(dados_novos) > 0:
        banco.inserirDadosPCA(dados_novos)

    consolidadoOcupacaoMaxima = banco.listarConsolidadoOcupacaoMaxima(data_inicial, data_final, id_sensor)

    return json.jsonify({
        'consolidadoOcupacaoMaxima': consolidadoOcupacaoMaxima,
    })

@app.route("/obterDadosConsolidadoDiaMes")
def obterDadosConsolidadoDiaMes():
    data_inicial = request.args.get('data_inicial')
    data_final = request.args.get('data_final')

    if not data_inicial or not data_final:
        return json.jsonify({"erro": "Parâmetros obrigatórios não informados."}), 400

    # Obter o maior id do banco
    maior_id = banco.obterIdMaximo("passagem")

    resultado = requests.get(f'{config.url_api}?sensor=passage&id_inferior={maior_id}')
    dados_novos = resultado.json()

	# Inserir os dados novos no banco
    if dados_novos and len(dados_novos) > 0:
        banco.inserirDadosPCA(dados_novos)

    consolidadoDiaMes = banco.listarConsolidadoDiaMes(data_inicial, data_final)

    return json.jsonify({
        'consolidadoDiaMes': consolidadoDiaMes,
    })

@app.get('/obterTempoReal')
def obterTempoReal():
    # Obter o maior id do banco
    maior_id = banco.obterIdMaximo("pca")

    resultado = requests.get(f'{config.url_api}?sensor=pca&id_inferior={maior_id}')
    dados_novos = resultado.json()

	# Inserir os dados novos no banco
    if dados_novos and len(dados_novos) > 0:
        banco.inserirDadosPCA(dados_novos)

    # Obter o maior id do banco
    maior_id = banco.obterIdMaximo("passagem")

    resultado = requests.get(f'{config.url_api}?sensor=passage&id_inferior={maior_id}')
    dados_novos = resultado.json()

	# Inserir os dados novos no banco
    if dados_novos and len(dados_novos) > 0:
        banco.inserirDadosPassagem(dados_novos)

	# Trazer os dados do banco
    dados = banco.listarDadosTempoReal()

    return json.jsonify(dados)

@app.post('/criar')
def criar():
    dados = request.json
    print(dados['id'])
    print(dados['nome'])
    return Response(status=204)

if __name__ == '__main__':
    app.run(host=config.host, port=config.port)
