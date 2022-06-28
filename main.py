from distutils.log import error
from msilib.schema import Error
from clases import *
from characterObjects import *
from data import preClass
from os import system
import sqlite3, os, random

loop=[ True, True ]#INICIO
op = 0#variable de entradas de usuario
#------------------------  base de datos-----------------
appPath = os.getcwd()
dbPath = appPath + '/saveData.db'#para agregar la ruta de la base de datos
#------------------------  base de datos---------------------



#------------------------  menu inicio  ---------------------
main = adventure(*parameters.values())
enemy = enemy(*main.listOfEnemys[0].values())#creacion de enemigo



while loop[0]:
	while op != '1' and op != '2':#control de input
		print('1._ Nueva Partida\n2._ Continuar')
		op = input('-->')
		
	if op == '1':#seleccion de clases por defecto --- nueva partida
		'''while loop[0]:#creacion y asignacion de clases al personaje principal
			op = input('Seleccion de Clase\n1._Guerrero-\n2._Maga-\n3._Asesina-\n4._No muerto-\n5._Cazador-\nEleccion: ')
			if op=='1' or op=='2' or op=='3' or op=='4' or op=='5':
				name=input('inserte el nombre de su personaje: ')
				mc = mainCharacter(name,*preClass[int(op)])
				loop[0]=False
			else:
				print('introduce un numero entre el 1 y el 5!\n')#fin de creacion de personaje'''

		#fines depurativos INICIO RAPIDO
		#mc = mainCharacter('admin!',*preClass[6])
		mc = mainCharacter('ADMIN',*preClass[1])
		#mc.status()
		loop[0] = False							
		#fines depurativos INICIO RAPIDO
	elif op == '2':# ------------------------cargar partida ------
		conex = sqlite3.connect(dbPath)# --- iniciar conexion ----
		cursor = conex.cursor()
		cursor.execute('SELECT * FROM SecoundTest LIMIT 3')
		importData = cursor.fetchall()
		saveI = 0#me ayuda a controlar que datos cargar :)
		conex.close()# -------------------   cerrar conexion -----

		for savedData in importData:
			print(saveI,'._ ','>nombre:', savedData[0], '>vida:', savedData[1], '>energia:', savedData[3],
			'>experiencia:',savedData[5], '/' ,savedData[6],'\n     ',
			'>ataque:', savedData[7] , '>defensa:', savedData[8],
			'>velocidad:', savedData[9], '>clase:',savedData[10],'\n     ',
			'nivel:', savedData[11], 'Zona:', savedData[12], 'dia nº:', savedData[14],
			'\n------------------------------------------------------------------')
			saveI = saveI + 1

	while loop[0]:
		try:#comprobacion de valor entero 
			op = int(input('numero de partida a cargar ->'))
			if op <= saveI and saveI >= 0:
				mc.reStat(*importData[op][0:11])
				main.reStat(*importData[op][11:15])
				loop[0] = False# salir del bucle
			else:
				print('algo salio mal')
		except ValueError or TypeError:
			print('se introdujo un valor errado')




#-----------------------------  fin de inicio  ---------------
mainMenuOptions=['0._ limpiar consola', '1._ Avanzar','2._ Inventario',
'3._ estado de la aventura', '4._ descansar', '5._ enemigo random :v'] 
while loop[1] and mc.life > 0:#------------------menu principal---------------

	print('')
	for options in mainMenuOptions:
		print('\n ',options)

	op = input('\n-->')
	if op == '0':
		system('cls')
		
	elif op == '1':
		main.advance(mc, enemy)

	elif op == '2':
		mc.inventory()

	elif op == '3':
		main.status()
		mc.status()

	elif op == '4':
		main.rest(mc)

	elif op == '5':
		#enemy.reStat(*main.randomEnemy(main.listOfEnemys))
		enemy.reStat(*main.listOfEnemys[4].values())
	
		battle(mc, enemy, main)
	# ------------------------- depuracion


	# ------------------------- depuracion



	else:
		print('opcion invalida')


print('tu progreso: ', mc.status(), main.status())


'''elif op == '9':#guardar partida en la base de datos
		conex = sqlite3.connect(dbPath)# --- iniciar conexion ---
		cursor = conex.cursor()
		export = mc.exportData(main)# exportar los datos a guardar
		cursor.execute("""INSERT INTO SecoundTest (name, life, maxLife, energy, maxEnergy,
		exp, maxExp, attack, defence, speed, class, level, world, avalibleEnemys, days)
		VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", export)
		conex.commit()#validar cambios
		conex.close()# --- cerrar conexion'''