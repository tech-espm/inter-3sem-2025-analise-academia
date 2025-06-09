# Vamos utilizar o pacote SQLAlchemy para acesso a banco de dados:
# https://docs.sqlalchemy.org
#
# Para isso, ele precisa ser instalado via pip (de preferência com o VS Code fechado):
# python -m pip install SQLAlchemy
#
# Além disso, o SQLAlchemy precisa de um driver do conexão ao banco. Isso depende do servidor
# (MySQL, Postgres, SQL Server, Oracle...) e do driver real. Vamos utilizar o driver MySQL-Connector,
# que também precisa ser instalado (de preferência com o VS Code fechado):
# python -m pip install mysql-connector-python
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from flask import jsonify, make_response
from config import conexao_banco

# Como criar uma comunicação com o banco de dados:
# https://docs.sqlalchemy.org/en/14/core/engines.html
#
# Detalhes específicos ao MySQL
# https://docs.sqlalchemy.org/en/14/dialects/mysql.html#module-sqlalchemy.dialects.mysql.mysqlconnector
#
# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
engine = create_engine(conexao_banco)

# A função text(), utilizada ao longo desse código, serve para encapsular um comando
# SQL qualquer, de modo que o SQLAlchemy possa entender!

def listarPessoas():
	try:
		# O with do Python é similar ao using do C#, ou o try with resources do Java.
		# Ele serve para limitar o escopo/vida do objeto automaticamente, garantindo
		# que recursos, como uma conexão com o banco, não sejam desperdiçados!
		with Session(engine) as sessao:
			pessoas = sessao.execute(text("SELECT id, nome, email FROM pessoa ORDER BY nome"))

			# Como cada registro retornado é uma tupla ordenada, é possível
			# utilizar a forma de enumeração de tuplas:
			for (id, nome, email) in pessoas:
				print(f'\nid: {id} / nome: {nome} / email: {email}')

			# Ou, se preferir, é possível retornar cada tupla, o que fica mais parecido
			# com outras linguagens de programação:
			#for pessoa in pessoas:
			#	print(f'\nid: {pessoa.id} / nome: {pessoa.nome} / email: {pessoa.email}')
	except Exception as e:
		print(f"Erro ao acessar o banco de dados: {e}")
		return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

def obterPessoa(id):
	try:
		with Session(engine) as sessao:
			parametros = {
				'id': id
			}

			# Mais informações sobre o método execute e sobre o resultado que ele retorna:
			# https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.execute
			# https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Result
			pessoa = sessao.execute(text("SELECT id, nome, email FROM pessoa WHERE id = :id"), parametros).first()

			if pessoa == None:
				print('Pessoa não encontrada!')
			else:
				print(f'\nid: {pessoa.id} / nome: {pessoa.nome} / email: {pessoa.email}')
	except Exception as e:
		print(f"Erro ao acessar o banco de dados: {e}")
		return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

def criarPessoa(nome, email):
	try:
		# É importante utilizar o método begin() para que a sessão seja comitada
		# automaticamente ao final, caso não ocorra uma exceção!
		# Isso não foi necessário nos outros exemplos porque nenhum dado estava sendo
		# alterado lá! Caso alguma exceção ocorra, rollback() será executado automaticamente,
		# e nenhuma alteração será persistida. Para mais informações de como explicitar
		# esse processo de commit() e rollback():
		# https://docs.sqlalchemy.org/en/14/orm/session_basics.html#framing-out-a-begin-commit-rollback-block
		with Session(engine) as sessao, sessao.begin():
			pessoa = {
				'nome': nome,
				'email': email
			}

			sessao.execute(text("INSERT INTO pessoa (nome, email) VALUES (:nome, :email)"), pessoa)

			# Para inserir, ou atualizar, vários registros ao mesmo tempo, a forma mais rápida
			# é passar uma lista como segundo parâmetro:
			# lista = [ ... ]
			# sessao.execute(text("INSERT INTO pessoa (nome, email) VALUES (:nome, :email)"), lista)
	except Exception as e:
		print(f"Erro ao acessar o banco de dados: {e}")
		return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

# Para mais informações:
# https://docs.sqlalchemy.org/en/14/tutorial/dbapi_transactions.html

def obterIdMaximo(tabela):
	try:
		with Session(engine) as sessao:
			registro = sessao.execute(text(f"SELECT MAX(id) id FROM {tabela}")).first()

			if registro == None or registro.id == None:
				return 0
			else:
				return registro.id
	except Exception as e:
		print(f"Erro ao acessar o banco de dados: {e}")
		return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

def inserirDadosPCA(registros):
	try:
		with Session(engine) as sessao, sessao.begin():
			for registro in registros:
				sessao.execute(text("INSERT INTO pca (id, data, id_sensor, delta, pessoas, luminosidade, umidade, temperatura) VALUES (:id, :data, :id_sensor, :delta, :pessoas, :luminosidade, :umidade, :temperatura)"), registro)
	except Exception as e:
		print(f"Erro ao acessar o banco de dados: {e}")
		return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)
 
def inserirDadosPassagem(registros):
	try:
		with Session(engine) as sessao, sessao.begin():
			for registro in registros:
				sessao.execute(text("INSERT INTO passagem (id, data, id_sensor, delta, bateria, entrada, saida) VALUES (:id, :data, :id_sensor, :delta, :bateria, :entrada, :saida)"), registro)
	except Exception as e:
		print(f"Erro ao acessar o banco de dados: {e}")
		return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

def listarDadosTempoReal():
	try:
		with Session(engine) as sessao:
			registros = sessao.execute(text("""
				(select id_sensor, pessoas, date_format(data, '%d/%m/%Y %H:%i:%s') data from pca where id_sensor = 1 order by id desc limit 1)
				union all
				(select id_sensor, pessoas, date_format(data, '%d/%m/%Y %H:%i:%s') data from pca where id_sensor = 2 order by id desc limit 1)
				union all
				(select id_sensor, pessoas, date_format(data, '%d/%m/%Y %H:%i:%s') data from pca where id_sensor = 3 order by id desc limit 1)
				union all
				(select id_sensor, pessoas, date_format(data, '%d/%m/%Y %H:%i:%s') data from pca where id_sensor = 4 order by id desc limit 1)
				union all
				(select id_sensor, pessoas, date_format(data, '%d/%m/%Y %H:%i:%s') data from pca where id_sensor = 5 order by id desc limit 1)
				union all
				(select id_sensor, pessoas, date_format(data, '%d/%m/%Y %H:%i:%s') data from pca where id_sensor = 6 order by id desc limit 1)
				union all
				(select id_sensor, pessoas, date_format(data, '%d/%m/%Y %H:%i:%s') data from pca where id_sensor = 7 order by id desc limit 1)
				union all
				(select id_sensor, pessoas, date_format(data, '%d/%m/%Y %H:%i:%s') data from pca where id_sensor = 8 order by id desc limit 1)
				;
			"""))
			dados = []
			for registro in registros:
				dados.append({
					"id_sensor": registro.id_sensor,
					"pessoas": registro.pessoas,
					"data": registro.data
				})
			return dados
	except Exception as e:
		print(f"Erro ao acessar o banco de dados: {e}")
		return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

def listarConsolidadoOcupacaoMaxima(data_inicial, data_final, id_sensor):
	try:
		with Session(engine) as sessao:
			parametros = {
				'data_inicial': data_inicial + ' 00:00:00',
				'data_final': data_final + ' 23:59:59',
				'id_sensor': id_sensor,
			}


			registros = sessao.execute(text("""
				select tmp.id_sensor, tmp.dia, tmp.hora, tmp.pessoas, u.pessoas ultimo_pessoas from
				(
					select id_sensor, date_format(date(data), '%Y-%m-%d') diaISO, date_format(date(data), '%d/%m') dia, extract(hour from data) hora, cast(max(pessoas) as signed) pessoas, max(id) id_ultimo
					from pca
					where data between :data_inicial and :data_final
					and id_sensor = :id_sensor
					group by id_sensor, diaISO, dia, hora
					order by id_sensor, diaISO, hora
				) tmp
				inner join pca u on u.id = tmp.id_ultimo
			"""), parametros)
			dados = []
			for registro in registros:
				dados.append({
					"id_sensor": registro.id_sensor,
					"dia": registro.dia,
					"hora": registro.hora,
					"pessoas": registro.pessoas,
					"ultimo_pessoas": registro.ultimo_pessoas
				})
			return dados
	except Exception as e:
		print(f"Erro ao acessar o banco de dados: {e}")
		return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

def listarConsolidadoDiaMesHora(data_inicial, data_final):
	try:
		with Session(engine) as sessao:
			parametros = {
				'data_inicial': data_inicial + ' 00:00:00',
				'data_final': data_final + ' 23:59:59'
			}

			registros = sessao.execute(text("""
				select date_format(date(data), '%d/%m/%Y') dia, extract(hour from data) hora, cast(sum(entrada) as signed) entrada
				from passagem
				where data between :data_inicial and :data_final
				and id_sensor = 2
				group by dia, hora
			"""), parametros)
			dados = []
			for registro in registros:
				dados.append({
					"dia": registro.dia,
					"hora": registro.hora,
					"entrada": registro.entrada
				})
			return dados
	except Exception as e:
		print(f"Erro ao acessar o banco de dados: {e}")
		return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

def listarConsolidadoDiaMes(data_inicial, data_final):
	try:
		with Session(engine) as sessao:
			parametros = {
				'data_inicial': data_inicial + ' 00:00:00',
				'data_final': data_final + ' 23:59:59'
			}

			registros = sessao.execute(text("""
				select date_format(date(data), '%Y-%m-%d') diaISO, date_format(date(data), '%d/%m') dia, cast(sum(entrada) as signed) entrada
				from passagem
				where data between :data_inicial and :data_final
				and id_sensor = 2
				group by diaISO, dia
				order by diaISO
			"""), parametros)
			dados = []
			for registro in registros:
				dados.append({
					"dia": registro.dia,
					"entrada": registro.entrada
				})
			return dados
	except Exception as e:
		print(f"Erro ao acessar o banco de dados: {e}")
		return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

def listarUsoMedioZonaDia(data_inicial, data_final):
	try:
		with Session(engine) as sessao:
			parametros = {
				'data_inicial': data_inicial + ' 00:00:00',
				'data_final': data_final + ' 23:59:59'
			}

			registros = sessao.execute(text("""
				select id_sensor, avg(pessoas)
				from pca
    			where extract(hour from data) > 6 and data between '2025-03-03 00:00:00' and '2025-03-14 23:59:59'
    			group by id_sensor;
			"""), parametros)
			dados = []
			for registro in registros:
				dados.append({
					"zona": registro.id_sensor,
					"dia": registro.dia,
					"media_pessoas": float(registro.media_pessoas) if registro.media_pessoas else 0.0
				})
			return dados
	except Exception as e:
		print(f"Erro ao acessar o banco de dados: {e}")
		return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

def listarUsoMedioHora(data_inicial, data_final):
	try:
		with Session(engine) as sessao:
			parametros = {
				'data_inicial': data_inicial + ' 00:00:00',
				'data_final': data_final + ' 23:59:59'
			}

			registros = sessao.execute(text("""
				select hour(data) as hora, avg(pessoas) as media_pessoas
				from pca
				where data between :data_inicial and :data_final
				group by hour(data)
				order by hora;
			"""), parametros)
			dados = []
			for registro in registros:
				dados.append({
					"hora": registro.hora,
					"media_pessoas": float(registro.media_pessoas) if registro.media_pessoas else 0.0
				})
			return dados
	except Exception as e:
		print(f"Erro ao acessar o banco de dados: {e}")
		return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)


