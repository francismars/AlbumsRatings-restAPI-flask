import requests
import json

while(True):
	comando = input(">")
	parametros = comando.split()
	if parametros[0].upper() == "HELP":
		print("Lista de Comandos:\n")
		print("- ADD USER <nome> <username> <password>")
		print("- ADD BANDA <nome> <ano> <genero>")
		print("- ADD ALBUM <id_banda> <nome> <ano album>")
		print("- ADD <id_user> <id_album> <rate>")
		print("- SHOW\REMOVE USER <id_user>")
		print("- SHOW\REMOVE BANDA <id_banda>")
		print("- SHOW\REMOVE ALBUM <id_album>")
		print("- SHOW\REMOVE ALL <USERS | BANDAS | ALBUNS>")
		print("- SHOW\REMOVE ALL ALBUNS_B <id_banda>")
		print("- SHOW\REMOVE ALL ALBUNS_U <id_user>")
		print("- SHOW\REMOVE ALL ALBUNS <rate>")
		print("- UPDATE ALBUM <id_user> <id_album> <rate>")
		print("- UPDATE USER <id_user> <password>")
		
	elif parametros[0].upper() == "ADD":
		if len(parametros) == 5:
			
			if parametros[1].upper() == "USER": # <nome> <username> <password>	
				dados = {'nome': parametros[2], 'username': parametros[3], 'password': parametros[4]}
				r = requests.post('http://localhost:5000/utilizadores', json = dados)
				print ("\n# - # - #\n")
				print ("Codigo: " + str(r.status_code))
				print ("Resposta: " + r.content.decode())
				print ('\n# - # - #\n')
			
			if parametros[1].upper() == "BANDA": # <nome> <ano> <genero>
				try: 
					ano = int(parametros[3])
					if 2020 > ano > 0:
						if parametros[4] in ["pop", "rock", "indy", "metal", "trance"]:
							dados = {'nome': parametros[2], 'ano': parametros[3], 'genero': parametros[4]}
							r = requests.post('http://localhost:5000/bandas', json = dados)
							print ("\n# - # - #\n")
							print ("Codigo: " + str(r.status_code))
							print ("Resposta: " + r.content.decode())
							print ('\n# - # - #\n')
						else:
							print ("Introduza Genero válido: pop|rock|indy|metal|trance")
					else:
						print ("Ano tem de ser entre 0 e 2020.")
				except ValueError:
					print ("Introduza Ano valido.")

			if parametros[1].upper() == "ALBUM": # <id_banda> <nome> <ano album>
				try: 
					id_banda = int(parametros[2])
					if id_banda > 0:
						try: 
							ano = int(parametros[4])
							if 2020 > ano > 0:					
								dados = {'id_banda': parametros[2], 'nome': parametros[3], 'ano album': parametros[4]}
								r = requests.post('http://localhost:5000/albuns', json = dados)
								print ("\n# - # - #\n")
								print ("Codigo: " + str(r.status_code))
								print ("Resposta: " + r.content.decode())
								print ('\n# - # - #\n')							
							else:
								print ("Ano tem de ser entre 0 e 2020.")
						except ValueError:
							print ("Introduza Ano valido.")
					else:
						print ("ID tem de ser maior que 0.")
				except ValueError:
					print ("Introduza ID valido.")
					
		if len(parametros) == 4: # <id_user> <id_album> <rate>
			try: 
				id_user = int(parametros[1])
				if id_user > 0:
					try: 
						id_album = int(parametros[2])
						if id_album > 0:				
							if parametros[3].upper() in ['"M"', '"MM"', '"S"', '"B"', '"MB"']:
								dados = {'id_user': parametros[1], 'rate': parametros[3].upper()}
								r = requests.post('http://localhost:5000/albuns/' + parametros[2], json = dados)
								print ("\n# - # - #\n")
								print ("Codigo: " + str(r.status_code))
								print ("Resposta: " + r.content.decode())
								print ('\n# - # - #\n')		
							else:
								print ("Introduza Rate válido: M|MM|S|B|MB")
						else:
							print ("ID do Album tem de ser maior que 0.")						
					except ValueError:
						print ("Introduza ID de Album valido.")
				else:
					print ("ID do User tem de ser maior que 0.")					
			except ValueError:
					print ("Introduza ID de User valido.")
					
	elif parametros[0].upper() == "SHOW":
	
		if parametros[1].upper() == "USER":	# <id_user>
			try: 
				id_user = int(parametros[2])
				if id_user > 0:					
					r = requests.get('http://localhost:5000/utilizadores/' + parametros[2])
					print ("\n# - # - #\n")
					print ("Codigo: " + str(r.status_code))
					print ("Resposta: " + r.content.decode())
					print ('\n# - # - #\n')						
				else:
					print ("ID do User tem de ser maior que 0.")					
			except ValueError:
					print ("Introduza ID de User valido.")			
			
		if parametros[1].upper() == "BANDA": # <id_banda>
			try: 
				id_user = int(parametros[2])
				if id_user > 0:		
					r = requests.get('http://localhost:5000/bandas/' + parametros[2])
					print ("\n# - # - #\n")
					print ("Codigo: " + str(r.status_code))
					print ("Resposta: " + r.content.decode())
					print ('\n# - # - #\n')						
				else:
					print ("ID do Banda tem de ser maior que 0.")					
			except ValueError:
					print ("Introduza ID de Banda valido.")
					
		if parametros[1].upper() == "ALBUM": # <id_album>
			try: 
				id_user = int(parametros[2])
				if id_user > 0:				
					r = requests.get('http://localhost:5000/albuns/' + parametros[2])
					print ("\n# - # - #\n")
					print ("Codigo: " + str(r.status_code))					
					print ("Resposta: " + r.content.decode())
					print ('\n# - # - #\n')						
				else:
					print ("ID do Album tem de ser maior que 0.")					
			except ValueError:
					print ("Introduza ID de Album valido.")		
			
		if parametros[1].upper() == "ALL":	
			
			if parametros[2].upper() == "USERS":	
				r = requests.get('http://localhost:5000/utilizadores/ALL')
				print ("\n# - # - #\n")
				print ("Codigo: " + str(r.status_code))					
				print ("Resposta: " + r.content.decode())
				print ('\n# - # - #\n')
				
			if parametros[2].upper() == "BANDAS":	
				r = requests.get('http://localhost:5000/bandas/ALL')
				print ("\n# - # - #\n")
				print ("Codigo: " + str(r.status_code))					
				print ("Resposta: " + r.content.decode())
				print ('\n# - # - #\n')	
				
			if parametros[2].upper() == "ALBUNS":
				
				if len(parametros) == 4: # SHOW ALL ALBUNS <rate>
					if parametros[3].upper() in ['"M"', '"MM"', '"S"', '"B"', '"MB"']:					
						dados = {'rate': parametros[3]}
						r = requests.get('http://localhost:5000/albuns/ALL/RATE', json = dados)
						print ("\n# - # - #\n")
						print ("Codigo: " + str(r.status_code))					
						print ("Resposta: " + r.content.decode())
						print ('\n# - # - #\n')						
					else:
						print ("Introduza Rate válido: M|MM|S|B|MB")
						
				if len(parametros) == 3: # SHOW ALL ALBUNS
					r = requests.get('http://localhost:5000/albuns/ALL')
					print ("\n# - # - #\n")
					print ("Codigo: " + str(r.status_code))					
					print ("Resposta: " + r.content.decode())
					print ('\n# - # - #\n')	
					
			if parametros[2].upper() == "ALBUNS_U":	# SHOW ALL ALBUNS_U <id_user>
				try: 
					id_user = int(parametros[3])
					if id_user > 0:	
						r = requests.get('http://localhost:5000/utilizadores/ALL/'+ parametros[3])
						print ("\n# - # - #\n")
						print ("Codigo: " + str(r.status_code))					
						print ("Resposta: " + r.content.decode())
						print ('\n# - # - #\n')	
					else:
						print ("ID do User tem de ser maior que 0.")					
				except ValueError:
					print ("Introduza ID de User valido.")				
						
				
			if parametros[2].upper() == "ALBUNS_B":	# SHOW ALL ALBUNS_B <id_banda>
				try: 
					id_banda = int(parametros[3])
					if id_banda > 0:		
						r = requests.get('http://localhost:5000/bandas/ALL/'+ parametros[3])
						print ("\n# - # - #\n")
						print ("Codigo: " + str(r.status_code))					
						print ("Resposta: " + r.content.decode())
						print ('\n# - # - #\n')	
					else:
						print ("ID do Banda tem de ser maior que 0.")					
				except ValueError:
						print ("Introduza ID de Banda valido.")						
						
	elif parametros[0].upper() == "REMOVE":
	
		if parametros[1].upper() == "USER": # REMOVE USER <user_id>
			try: 
				id_user = int(parametros[2])
				if id_user > 0:					
					r = requests.delete('http://localhost:5000/utilizadores/' + parametros[2])
					print ("\n# - # - #\n")
					print ("Codigo: " + str(r.status_code))
					print ("Resposta: " + r.content.decode())
					print ('\n# - # - #\n')						
				else:
					print ("ID do User tem de ser maior que 0.")					
			except ValueError:
					print ("Introduza ID de User valido.")			
			
		if parametros[1].upper() == "BANDA": # REMOVE BANDA <banda_id>		
			try: 
				id_user = int(parametros[2])
				if id_user > 0:		
					r = requests.delete('http://localhost:5000/bandas/' + parametros[2])
					print ("\n# - # - #\n")
					print ("Codigo: " + str(r.status_code))
					print ("Resposta: " + r.content.decode())
					print ('\n# - # - #\n')						
				else:
					print ("ID do Banda tem de ser maior que 0.")					
			except ValueError:
					print ("Introduza ID de Banda valido.")
								
			
		if parametros[1].upper() == "ALBUM": # REMOVE ALBUM <id_album>
			try: 
				id_user = int(parametros[2])
				if id_user > 0:				
					r = requests.delete('http://localhost:5000/albuns/' + parametros[2])
					print ("\n# - # - #\n")
					print ("Codigo: " + str(r.status_code))					
					print ("Resposta: " + r.content.decode())
					print ('\n# - # - #\n')						
				else:
					print ("ID do Album tem de ser maior que 0.")					
			except ValueError:
					print ("Introduza ID de Album valido.")				
				
		if parametros[1].upper() == "ALL":		
		
			if parametros[2].upper() == "USERS": # REMOVE ALL USERS	
				r = requests.delete('http://localhost:5000/utilizadores/ALL')
				print ("\n# - # - #\n")
				print ("Codigo: " + str(r.status_code))					
				print ("Resposta: " + r.content.decode())
				print ('\n# - # - #\n')		
				
			if parametros[2].upper() == "BANDAS": # REMOVE ALL BANDAS
				r = requests.delete('http://localhost:5000/bandas/ALL')
				print ("\n# - # - #\n")
				print ("Codigo: " + str(r.status_code))					
				print ("Resposta: " + r.content.decode())
				print ('\n# - # - #\n')	
				
			if parametros[2].upper() == "ALBUNS":				
				if len(parametros) == 4: # REMOVE ALL ALBUNS <rate>
					if parametros[3].upper() in ['"M"', '"MM"', '"S"', '"B"', '"MB"']:					
						dados = {'rate': parametros[3]}
						r = requests.delete('http://localhost:5000/albuns/ALL/RATE', json = dados)
						print ("\n# - # - #\n")
						print ("Codigo: " + str(r.status_code))					
						print ("Resposta: " + r.content.decode())
						print ('\n# - # - #\n')						
					else:
						print ("Introduza Rate válido: M|MM|S|B|MB")					
					
				if len(parametros).upper() == 3: # REMOVE ALL ALBUNS
					r = requests.delete('http://localhost:5000/albuns/ALL')
					print ("\n# - # - #\n")
					print ("Codigo: " + str(r.status_code))					
					print ("Resposta: " + r.content.decode())
					print ('\n# - # - #\n')	
					
			if parametros[2].upper() == "ALBUNS_B": # REMOVE ALL ALBUNS_B <id_banda>
				try: 
					id_user = int(parametros[3])
					if id_user > 0:		
						r = requests.delete('http://localhost:5000/albuns/ALL/'+parametros[3])
						print ("\n# - # - #\n")
						print ("Codigo: " + str(r.status_code))					
						print ("Resposta: " + r.content.decode())
						print ('\n# - # - #\n')	
					else:
						print ("ID do Banda tem de ser maior que 0.")					
				except ValueError:
						print ("Introduza ID de Banda valido.")					
				
			if parametros[2].upper() == "ALBUNS_U": # REMOVE ALL ALBUNS_U <id_user>
				r = requests.delete('http://localhost:5000/utilizadores/ALL/'+parametros[3])
				print ("\n# - # - #\n")
				print ("Codigo: " + str(r.status_code))					
				print ("Resposta: " + r.content.decode())
				print ('\n# - # - #\n')					

				
	elif parametros[0].upper() == "UPDATE":
			if parametros[1].upper() == "USER": # USER <id_user> <password>
				dados = {'password': parametros[3]}
				r = requests.put('http://localhost:5000/utilizadores/' + parametros[2], json = dados)
				print ("\n# - # - #\n")
				print ("Codigo: " + str(r.status_code))
				print ("Resposta: " + r.content.decode())
				print ('\n# - # - #\n')
			
			if parametros[1].upper() == "ALBUM": # ALBUM <id_user> <id_album> <rate>
				try: 
					id_user = int(parametros[2])
					if id_user > 0:
						try: 
							id_album = int(parametros[3])
							if id_album > 0:				
								if parametros[4].upper() in ['"M"', '"MM"', '"S"', '"B"', '"MB"']:
									dados = {'id_user': parametros[2], 'rate': parametros[4].upper()}
									r = requests.put('http://localhost:5000/albuns/RATE/' + parametros[3], json = dados)
									print ("\n# - # - #\n")
									print ("Codigo: " + str(r.status_code))
									print ("Resposta: " + r.content.decode())
									print ('\n# - # - #\n')		
								else:
									print ("Introduza Rate válido: M|MM|S|B|MB")
							else:
								print ("ID do Album tem de ser maior que 0.")						
						except ValueError:
							print ("Introduza ID de Album valido.")
					else:
						print ("ID do User tem de ser maior que 0.")					
				except ValueError:
						print ("Introduza ID de User valido.")	
				
				
	
	else:
		print("- Comando não reconhecido. Escreva HELP para lista de comandos")