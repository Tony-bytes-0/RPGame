from distutils.log import error
from msilib.schema import Error
from clases import *
from characterObjects import *
from data import preClass
from os import system
import sqlite3, os, random

loop=[ True, True ]#	INICIO
op = 0#	variable de entradas de usuario
main = adventure(*parameters.values())#creacion de personaje principal
enemy = enemy(*main.listOfEnemys[0].values())#creacion de enemigo

#------------------------  menu inicio  ---------------------
while loop[0]:#creacion y asignacion de clases al personaje principal
	op = input('Seleccion de Clase\n1._Guerrero-\n2._Maga-\n3._Asesina-\n4._No muerto-\n5._Cazador-\nEleccion: ')
	if op=='1' or op=='2' or op=='3' or op=='4' or op=='5':
		name=input('inserte el nombre de su personaje: ')
		mc = mainCharacter(name,*preClass[int(op)])
		loop[0]=False
	else:
		print('introduce un numero entre el 1 y el 5!\n')#fin de creacion de personaje

#	---- fines depurativos INICIO RAPIDO ----
#mc = mainCharacter('ADMIN',*preClass[6])
#mc.status()			
#	---- fines depurativos INICIO RAPIDO ----

#-----------------------------  fin de inicio  ---------------
mainMenuOptions=['0._ limpiar consola', '1._ Avanzar','2._ Inventario',
'3._ Estado', '4._ descansar', '5._ enemigo random'] 
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
	elif op == '6':
		mc.useSkill(enemy)

	# ------------------------- depuracion

	else:
		print('opcion invalida')

print('tu progreso: ', mc.status(), main.status())


