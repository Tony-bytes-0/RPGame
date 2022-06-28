from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from os import system
import random, time, sys
from characterObjects import enemy
from data import *
#----------------------------------definicion de funciones
def slowText (text):
	for char in text:
		print(char, end='')
		sys.stdout.flush()
		#time.sleep(0.1) activame

def statusBar(player,enemy, turn):
	print(f'\n------------------------------- Barra de Status -------------------------------------------',#screen
		  '\npuntos de vida de ->{}<-: {}/{}  -  energia: {} / {} - Mana:{} / {} - estado:{}'.format( player.name, round(player.life,2), player.maxLife, player.energy, player.maxEnergy,player.mana,player.maxMana, player.states) ,
		  '\npuntos de vida de ->{}<-: {}/{}  -  energia: {} / {} - Mana:{} / {} - estado:{}\nturno: {}\n'.format(enemy.name, round(enemy.life,  2) , enemy.maxLife, enemy.energy, enemy.maxEnergy, enemy.mana,enemy.maxMana, enemy.states,turn),
		  f'---------------------------------------------------------------------------------------------\n\n\n\n')#tengo que hacer un salto de pagina

def lifeCheck(player,enemy):
	if player.life <= 0:
		print('has muerto!\n>>>G A M E  O V E R<<<')
		return False
	elif enemy.life <= 0:
		print(f'>>>{enemy.name} ha muerto!<<<')
		return False
	else:
		return True

def whoMovesFirst(player,enemy):
	if player.speed > enemy.speed:
		return [player, enemy]
	else:
		return [enemy, player]
#------------------------------------------------------------    menu de combate{
def battle(player, enemy, main):
	system('cls')
	keepGoing = True
	turn = 1

	print(f'\n\n\ncomienza el combate entre >>> {player.name} y {enemy.name} <<<\n\n\n')
	try:
		start = input('1._ Prepararse para la batalla\n\n2._ Tratar de escapar!\n-->')#screen
		if start == '1':
			pass
		elif start == '2':
			keepGoing = main.evadeFight()
	except:
		print('error al seleccionar opcion')#screen


	time.sleep(1)

	while keepGoing:
		time.sleep(1)
		opponent = whoMovesFirst(player, enemy)#turno del personaje mas rapido
		opponent[0].turn(opponent[1])
		keepGoing = lifeCheck(player, enemy)

		if keepGoing:#comprobacion de vida -- turno dos
			opponent[1].turn(opponent[0])#turno del personaje mas lento
			keepGoing = lifeCheck(player, enemy)

		if keepGoing:#mientras el combate siga, muestrame los datos
			statusBar(player, enemy, turn)
		turn = turn + 1
		final = input('\nintro para continuar\n')
		system('cls')

	if player.life > 0 and enemy.life <= 0:
		player.gainExp( enemy.calculateLvL() )
		itemDroped = main.dropAfterBattle()
		if itemDroped != False:
			print('consigues un objeto luego de la batalla: ', itemDroped)
			player.addItem(*itemDroped )
#	-------------------------------------------------------final de la batalla
		



class adventure():#---------------------------------------weas de la aventura
	def __init__(self, energyCost, encounterProb, drop, drops, evade):
		self.level = 0
		self.world = 'Pradera'
		self.listOfEnemys = plainsEnemys
		self.days = 0
		# --- declaracion de los parametros de dificultad del nivel ---
		self.advanceEnergyCost = energyCost
		self.enemyEncounterProbability = encounterProb
		self.dropChance = drop
		self.posibleDrops = drops
		self.evadeFightProbability = evade

	def advance(self, player, enemy):
		encounter = random.randint(0, 9)
		if encounter <= self.enemyEncounterProbability:
			system('cls')
			enemy.reStat(*self.randomEnemy(self.listOfEnemys))
			battle(player, enemy, self)
			final = input('presionar intro para continuar\n')
			system('cls')
			
		if player.energy >= self.advanceEnergyCost:#energia suficiente para avanzar
			self.level = self.level + 1
			player.addSomeStat('energy', -self.advanceEnergyCost)
			print('se ha avanzado un nivel, energia restante:', player.energy)
			self.zoneCheck(player, enemy)
		
		else:
			print('no tienes suficiente energia para abrirte paso a travez del entorno')

	def status(self):
		print('estado de la aventura: --- Zona:', self.world, '--- nivel:' ,self.level)

	def rest(self,player):
		player.addSomeStat('energy', (player.maxEnergy - player.energy))
		player.addSomeStat('mana', (player.maxMana - player.mana))
		self.days = self.days + 1
		print(f'{player.name} descansa y recupera su energia a cambio de un dia')

	def randomEnemy(self, listOfEnemys):
		x =list(random.choice(listOfEnemys).values())
		print(x)
		return x

	def evadeFight(self):
		x = random.randint(0,9)
		if x <= self.evadeFightProbability:
			print('Escapaste con algunos problemas')
			return False
		else:
			print('Fallaste al Evitar el Enfrentamiento')
			return True
	
	def dropAfterBattle(self):
		items = list(self.posibleDrops)#lista de drops
		prob = random.randint(0,9)#probabilidad de dropeo de main.adventure
		x = random.randint(1,2)#cantidad del item (1/2)

		if prob <= self.dropChance:
			prob = random.choice(items)
			return prob, x
		else:
			return False

	# --- fuera del juego ---
	def reStat(self, enemys, world, advanceEnergyCost, encounter, dropProb, posibleDrops, evadeFight ):
		self.listOfEnemys = enemys
		self.world = world
		self.advanceEnergyCost = advanceEnergyCost
		self.enemyEncounterProbability = encounter
		self.dropChance = dropProb
		self.posibleDrops = posibleDrops
		self.evadeFightProbability = evadeFight
	def raw(self):
		print('parametros de adventure:\n',self.enemyEncounterProbability, self.posibleDrops)
	# --- fuera del juego ---
	
	def zoneCheck(self, player, enemy):
		if self.level == 15:
			self.evadeFightProbability = 0
			slowText(bossDialogues[0])
			enemy.reStat(*bosses[0].values())
			battle(player, enemy, self)
			print('''\n notas un cambio en el entorno luego de avanzar por un rato\n
			el entorno se vuelve continuamente mas hostil\n
			>>> entrando al Camino del Hierro Negro <<<\n''')
			self.reStat(blackIronPath, *blackIronPathParameters)

		elif self.level == 30:
			print('hasta aqui he prorgamado, 15 dias. flojoMan')
			
			#cambiar variables del entorno








