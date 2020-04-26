import sqlite3
from os.path import isfile
from flask import Flask, request, make_response
import json

def connect_db(dbname):
	db_is_created = isfile(dbname) # Existe ficheiro da base de dados?
	connection = sqlite3.connect('basedados.db')
	cursor = connection.cursor()
	if not db_is_created:
		with open('basedados.sql', 'r', encoding="utf8") as f:
			cursor.executescript(f.read())
			connection.commit()
	return connection, cursor


app = Flask(__name__)

@app.route('/utilizadores', methods = ["POST"])
@app.route('/utilizadores/ALL', methods = ["GET", "DELETE"])
@app.route('/utilizadores/ALL/<int:id>', methods = ["GET","DELETE"])
@app.route('/utilizadores/<int:id>', methods = ["GET", "DELETE", "PUT"])
def utilizadores(id = None):
	if request.method == "GET":
		if request.url == 'http://localhost:5000/utilizadores/' + str(id): # SHOW USER
			conn, cursor = connect_db('basedados.db')
			cursor.execute('SELECT * FROM utilizadores WHERE id=' + str(id))
			todos = cursor.fetchall()
			conn.close()
			if len(todos) == 0:
				r = make_response("User não encontrado")
				r.status_code = 404
				return r
			else:
				dados = {'id': todos[0][0], 'nome': todos[0][1], 'username': todos[0][2], 'password': todos[0][3]}			
				r = make_response(json.dumps(dados))
				r.status_code = 202
				return r
			
		if request.url == 'http://localhost:5000/utilizadores/ALL': # SHOW ALL USERS
			conn, cursor = connect_db('basedados.db')
			cursor.execute('SELECT * FROM utilizadores')
			registo = cursor.fetchone()	
			if not registo:
				r = make_response("Nao existem Users")
				r.status_code = 404
				return r
			else:
				todos = {}
				while registo:
					todos[registo[0]] = {'nome': registo[1], 'username': registo[2], 'password': registo[3]}
					registo = cursor.fetchone()
				conn.close()
				r = make_response(json.dumps(todos))
				r.status_code = 202
				return r
			
		if request.url == 'http://localhost:5000/utilizadores/ALL/' + str(id): # SHOW ALL ALBUNS_U <id_user>
			conn, cursor = connect_db('basedados.db')
			cursor.execute('SELECT * FROM listas_albuns WHERE id_user=' + str(id))
			registo = cursor.fetchone()
			if not registo:
				conn.close()
				r = make_response("Rates de User não encontrados")
				r.status_code = 404
				return r
			else:
				todos = {}
				while registo:
					conn2, cursor2 = connect_db('basedados.db')
					cursor2.execute('SELECT nome FROM albuns WHERE id=' + str(registo[1]))
					resposta = cursor2.fetchone()
					if not resposta:
						nomeAlbum = "Album Inexistente"
					else:
						nomeAlbum = resposta[0]
					cursor2.execute('SELECT sigla FROM rates WHERE id=' + str(registo[2]))
					sigla = cursor2.fetchone()					
					todos[nomeAlbum] = {'Rate': sigla[0]}
					registo = cursor.fetchone()
				conn.close()
				conn2.close()		
				r = make_response(json.dumps(todos))
				r.status_code = 202
				return r
			
	if request.method == "DELETE": # REMOVE ALL USERS
		if request.url == 'http://localhost:5000/utilizadores/ALL':
			conn, cursor = connect_db('basedados.db')
			cursor.execute('SELECT * FROM utilizadores')
			registo = cursor.fetchone()	
			if not registo:
				r = make_response("Nao existem Users")
				r.status_code = 404
				return r
			else:	
				cursor.execute('DELETE FROM utilizadores')
				conn.commit()
				cursor.execute('DELETE FROM listas_albuns')
				conn.commit()			
				conn.close()			
				r = make_response("Todos os Utilizadores e Rates de Utilizadores removidos!")
				r.status_code = 202
				return r
			
		if request.url == 'http://localhost:5000/utilizadores/ALL/'+ str(id): # REMOVE ALL ALBUNS_U
			conn, cursor = connect_db('basedados.db')
			cursor.execute('SELECT id_album FROM listas_albuns WHERE id_user=' + str(id))
			registo = cursor.fetchone()
			if not registo:
				r = make_response("User " + str(id) + " nao tem rates")
				r.status_code = 404
				return r
			else:			
				while registo:
					cursor.execute('DELETE FROM albuns WHERE id=' + str(registo[0]))
					conn.commit()
					registo = cursor.fetchone()
				conn.close()			
				r = make_response("Todos os Albuns rated pelo User %s removidos!" %id)
				r.status_code = 202
				return r	
		
		if request.url == 'http://localhost:5000/utilizadores/' + str(id): # REMOVE USER <user_id>
			conn, cursor = connect_db('basedados.db')
			cursor.execute('SELECT * FROM utilizadores WHERE id=' + str(id))
			registo = cursor.fetchone()
			if not registo:
				r = make_response("User " + str(id) + " nao existe!")
				r.status_code = 404
				return r
			else:						
				cursor.execute('DELETE FROM utilizadores WHERE id=' + str(id))
				conn.commit()
				conn.close()			
				r = make_response("Utilizador %s removido!" %id)
				r.status_code = 202
				return r			

	if request.method == "POST": # ADD USER
		dados = json.loads(request.data)
		executar = (dados['nome'],dados['username'],dados['password'])		
		conn, cursor = connect_db('basedados.db')
		cursor.execute('INSERT INTO utilizadores VALUES (NULL, ?, ?, ?)', executar)
		conn.commit()
		conn.close()		
		r = make_response("Utilizador %s inserido!" %dados['nome'])
		r.headers['location'] = '/alunos/id'
		r.status_code = 201
		return r
	
	if request.method == "PUT": # UPDATE USER
		conn, cursor = connect_db('basedados.db')
		cursor.execute('SELECT * FROM utilizadores WHERE id=' + str(id))
		registo = cursor.fetchone()
		if not registo:
			r = make_response("User " + str(id) + " nao existe!")
			r.status_code = 404
			return r
		else:			
			dados = json.loads(request.data)
			passNova = dados['password']
			print('UPDATE utilizadores SET password=' + passNova + ' WHERE id=' + str(id))
			cursor.execute('UPDATE utilizadores SET password=' + passNova + ' WHERE id=' + str(id))
			conn.commit()
			conn.close()		
			r = make_response("Utilizador %s actualizado!" %id)
			r.status_code = 202
			return r	
		
@app.route('/bandas', methods = ["POST"])
@app.route('/bandas/<int:id>', methods = ["GET", "DELETE"])
@app.route('/bandas/ALL', methods = ["GET", "DELETE"])	
@app.route('/bandas/ALL/<int:id>', methods = ["GET"])	
def bandas(id = None):
	if request.method == "GET":
		if request.url == 'http://localhost:5000/bandas/' + str(id): # SHOW BANDA
			conn, cursor = connect_db('basedados.db')
			cursor.execute('SELECT * FROM bandas WHERE id=' + str(id))
			registo = cursor.fetchone()
			if not registo:
				r = make_response("Banda " + str(id) + " nao existe!")
				r.status_code = 404
				return r
			else:				
				cursor.execute('SELECT * FROM bandas WHERE id=' + str(id))
				todos = cursor.fetchall()
				conn.close()
				dados = {'id': todos[0][0], 'nome': todos[0][1], 'ano': todos[0][2], 'genero': todos[0][3]}			
				r = make_response(json.dumps(dados))
				r.status_code = 202
				return r	
			
		if request.url == 'http://localhost:5000/bandas/ALL': # SHOW ALL BANDAS
			conn, cursor = connect_db('basedados.db')
			cursor.execute('SELECT * FROM bandas')
			resposta = cursor.fetchone()
			if not resposta:
				r = make_response("Nao existem bandas!")
				r.status_code = 404
				return r
			else:
				todos = {}
				while resposta:
					todos[resposta[0]] = {'nome': resposta[1], 'ano': resposta[2], 'genero': resposta[3]}
					resposta = cursor.fetchone()
				conn.close()				
				r = make_response(json.dumps(todos))
				r.status_code = 202
				return r	

		if request.url == 'http://localhost:5000/bandas/ALL/' + str(id): # SHOW ALL ALBUNS_B <id_banda>
			conn, cursor = connect_db('basedados.db')			
			cursor.execute('SELECT * FROM bandas WHERE id=' + str(id))
			resposta = cursor.fetchone()
			if not resposta:
				r = make_response("Banda " + str(id) + " nao existe.")
				r.status_code = 404
				return r
			else:			
				cursor.execute('SELECT * FROM albuns WHERE id_banda=' + str(id))
				todos = cursor.fetchone()
				albuns_B = {}
				if not todos:
					r = make_response("Banda " + str(id) + " nao tem albuns!")
					r.status_code = 404
					return r
				else:
					while todos:
						albuns_B[todos[0]] = {'id_banda': todos[1], 'nome': todos[2], 'ano': todos[3]}
						todos = cursor.fetchone()
					conn.close()			
					r = make_response(json.dumps(albuns_B))
					r.status_code = 202
					return r		
			
	if request.method == "POST": # ADD BANDA
		dados = json.loads(request.data)
		executar = (dados['nome'],dados['ano'],dados['genero'])		
		conn, cursor = connect_db('basedados.db')
		nomeBanda = "'" + dados['nome'] + "'"
		cursor.execute('SELECT * FROM bandas WHERE nome=' + nomeBanda)
		resposta = cursor.fetchone()
		if resposta:
			r = make_response("Banda " + dados['nome'] + " ja existe.")
			r.status_code = 401
			return r
		else:
			cursor.execute('INSERT INTO bandas VALUES (NULL, ?, ?, ?)', executar)
			conn.commit()
			conn.close()		
			r = make_response("Banda %s inserida!" %dados['nome'])
			r.headers['location'] = '/bandas/id'
			r.status_code = 201
			return r
		
	if request.method == "DELETE":
		if request.url == 'http://localhost:5000/bandas/ALL': # REMOVE ALL BANDAS
			conn, cursor = connect_db('basedados.db')			
			cursor.execute('SELECT * FROM bandas')
			resposta = cursor.fetchone()
			if not resposta:
				r = make_response("Nao existem bandas.")
				r.status_code = 401
				return r
			else:						
				cursor.execute('DELETE FROM bandas')
				conn.commit()
				conn.close()			
				r = make_response("Todos as bandas removidos!")
				r.status_code = 202
				return r
			
		if request.url == 'http://localhost:5000/bandas/' + str(id): # REMOVE BANDA <id_banda>
			conn, cursor = connect_db('basedados.db')
			
			cursor.execute('SELECT * FROM bandas WHERE id=' + str(id))
			todos = cursor.fetchone()
			if not todos:
				r = make_response("Banda " + str(id) + " nao existe!")
				r.status_code = 404
				return r
			else:			
				cursor.execute('DELETE FROM bandas WHERE id=' + str(id))
				conn.commit()
				conn.close()
				r = make_response("Banda %s removida!" %id)
				r.status_code = 202
				return r				

@app.route('/albuns', methods = ["POST"])
@app.route('/albuns/ALL', methods = ["GET", "DELETE"])
@app.route('/albuns/ALL/RATE', methods = ["GET", "DELETE"])
@app.route('/albuns/RATE/<int:id>', methods = ["PUT"])
@app.route('/albuns/<int:id>', methods = ["POST","GET", "DELETE"])
@app.route('/albuns/ALL/<int:id>', methods = ["GET", "DELETE"])
def albuns(id = None):
	if request.method == "PUT": # UPDATE <id_user> <id_album> <rate>
		conn, cursor = connect_db('basedados.db')
		dados = json.loads(request.data)		
		cursor.execute('SELECT id FROM rates WHERE sigla=' + dados['rate'])
		rateID = cursor.fetchone()
		cursor.execute('SELECT * FROM listas_albuns WHERE id_album=' + str(id) +' AND id_user= '+dados['id_user'])
		existe = cursor.fetchone()
		if not existe:
			r = make_response('Rate de album'+ str(id)+' do user' +dados['id_user']+ ' nao existe!')
			r.status_code = 404
			return r		
		else:
			cursor.execute('UPDATE listas_albuns SET id_rate= '+str(rateID[0])+' WHERE id_album=' + str(id) +' AND id_user= '+dados['id_user'])
			conn.commit()
			conn.close()		
			r = make_response("Rate de album %s actualizado!" %id)
			r.status_code = 202
			return r
	
	if request.method == "GET":
		if request.url == 'http://localhost:5000/albuns/' + str(id): # SHOW ALBUM
			conn, cursor = connect_db('basedados.db')
			cursor.execute('SELECT * FROM albuns WHERE id=' + str(id))
			todos = cursor.fetchall()
			if not todos:
				r = make_response('Album '+ str(id)+ ' nao existe!')
				r.status_code = 404
				return r
			else:
				cursor.execute('SELECT nome FROM bandas WHERE id=' + str(todos[0][1]))
				nomeBanda = cursor.fetchone()
				if not nomeBanda:
					r = make_response('Album '+ str(todos[0][0])+ ' nao existe!')
					r.status_code = 404
					return r
				else:
					dados = {}
					conn.close()
					dados[todos[0][0]] = {'Banda': nomeBanda[0], 'Nome': todos[0][2], 'Ano': todos[0][3]}			
					r = make_response(json.dumps(dados))
					r.status_code = 202
					return r			
		
		if request.url == 'http://localhost:5000/albuns/ALL/RATE': # SHOW ALL ALBUNS RATE
			dados = json.loads(request.data) 
			conn, cursor = connect_db('basedados.db')
			cursor.execute('SELECT id FROM rates WHERE sigla=' + dados['rate'])
			rateID = cursor.fetchone()			
			cursor.execute('SELECT * FROM listas_albuns WHERE id_rate=' + str(rateID[0]))
			resultado = cursor.fetchone()
			if not resultado:
				r = make_response('Nenhum album com rate '+dados['rate'])
				r.status_code = 404
				return r
			else:
				albunsRate = {}
				while resultado:
					albunsRate[resultado[0]] = {'rate': resultado[2]}
					resultado = cursor.fetchone()
				conn.close()			
				r = make_response(json.dumps(albunsRate))
				r.status_code = 202
				return r
				
		if request.url == 'http://localhost:5000/albuns/ALL': # SHOW ALL ALBUNS
			conn, cursor = connect_db('basedados.db')
			cursor.execute('SELECT * FROM albuns')
			todos = cursor.fetchall()
			conn.close()
			r = make_response(json.dumps(todos))
			r.status_code = 202
			return r
			
		if request.url == 'http://localhost:5000/albuns/ALL/' + str(id): # SHOW ALL ALBUNS_B <id_banda>
			conn, cursor = connect_db('basedados.db')
			cursor.execute('SELECT * FROM albuns WHERE id_banda=' + str(id))
			todos = cursor.fetchall()
			conn.close()			
			r = make_response(json.dumps(todos))
			r.status_code = 202
			return r
		
	if request.method == "DELETE":
		if request.url == 'http://localhost:5000/albuns/ALL': # REMOVE ALL ALBUNS
			conn, cursor = connect_db('basedados.db')
			cursor.execute('DELETE FROM albuns')
			conn.commit()
			conn.close()			
			r = make_response("Todos os albuns removidos!")
			r.status_code = 202
			return 
			
		if request.url == 'http://localhost:5000/albuns/ALL/RATE': # REMOVE REMOVE ALL ALBUNS RATE
			dados = json.loads(request.data) 
			conn, cursor = connect_db('basedados.db')
			print(dados['rate'])
			print('SELECT id FROM rates WHERE sigla = ' + dados['rate'])
			cursor.execute('SELECT id FROM rates WHERE sigla=' + dados['rate'])
			rateID = cursor.fetchone()
			cursor.execute('DELETE FROM albuns WHERE id=' + str(rateID[0]))
			conn.commit()
			conn.close()			
			r = make_response("Removidos Todos os albuns com rate " + dados['rate'])
			r.status_code = 202
			return r		
			
		if request.url == 'http://localhost:5000/albuns/' + str(id): # REMOVE ALBUM <album_id>
			conn, cursor = connect_db('basedados.db')
			cursor.execute('DELETE FROM albuns WHERE id=' + str(id))
			conn.commit()
			conn.close()			
			r = make_response("Album %s removido!" %id)
			r.status_code = 202
			return r							
			
		if request.url == 'http://localhost:5000/albuns/ALL/'+str(id): # REMOVE ALL ALBUNS_B
			conn, cursor = connect_db('basedados.db')
			cursor.execute('DELETE FROM albuns WHERE id_banda=' + str(id))
			conn.commit()
			conn.close()			
			r = make_response("Todos os Albuns de %s removidos!" %id)
			r.status_code = 202
			return r
			
	if request.method == "POST":
		if request.url == 'http://localhost:5000/albuns': #ADD ALBUM <id_banda> <nome> <ano album>
			dados = json.loads(request.data)
			executar = (dados['id_banda'],dados['nome'],dados['ano album'])			
			conn, cursor = connect_db('basedados.db')
			cursor.execute('INSERT INTO albuns VALUES (NULL, ?, ?, ?)', executar)
			conn.commit()
			conn.close()			
			r = make_response("Album %s inserido!" %dados['nome'])
			r.headers['location'] = '/albuns/id' # 123 para exemplo
			r.status_code = 201
			return r
				
		if request.url == 'http://localhost:5000/albuns/' + str(id): #ADD <id_user> <id_album> <rate>	
			dados = json.loads(request.data) 
			conn, cursor = connect_db('basedados.db')
			cursor.execute('SELECT id FROM rates WHERE sigla=' + dados['rate'])
			rateID = cursor.fetchone()
			print(rateID[0])
			print('INSERT INTO listas_albuns (id_user,id_album,id_rate) VALUES (' + dados['id_user'] + ',' + str(id) + ',' + str(rateID[0]) +')' )
			cursor.execute('INSERT INTO listas_albuns (id_user,id_album,id_rate) VALUES (' + dados['id_user'] + ',' + str(id) + ',' + str(rateID[0]) +')' )
			conn.commit()
			conn.close()			
			r = make_response("Rate inserida!")
			r.headers['location'] = '/albuns/' + str(id)
			r.status_code = 201
			return r
			
			
if __name__ == '__main__':
	conn, cursor = connect_db('basedados.db')
	app.run(debug = True)
	conn.close()	
	
	