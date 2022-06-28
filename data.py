preClass=[('Life','Attack','Defence','Speed','Magic Power'),
(10, 3, 5, 1,'Guerrero', 6, 1 , [], ['Doble Golpe']),

(6, 1, 2, 5,'Maga', 5, 10, ['Golpe Chispa'], []),

(5, 6, 1, 7,'Asesina', 6, 4, [], ['Punto Ciego']),

(15, 2, 2, 3,'No Muerto', 4, 8, [], []),

(6, 5, 5, 3,'Cazador', 10, 1, [], ['Inhabilitar']),

(100, 20, 10, 10, 'admin', 100, 10, ['Golpe Chispa'], [])]
statList = [ 'Vida', 'Ataque', 'Defensa', 'Velocidad', 'Energia','Mana']


parameters = { 'advanceEnergyCost': 2, 'encounter':4, 'itemDrop':5 ,
'posibleDrops':{'pocion de vida':1, 'pocion de energia':1}, 
'evadeFightProbability':3}

itemList = {'pocion de vida': 1, 'pocion de energia': 1, 'pocion de mana': 0}

skillList = {'Golpe Chispa': 5, 'Rafaga de Viento': 9}

tecniqueList = {'Doble Golpe': 5, 'Punto Ciego':6, 'Tiro Bajo':4,'Tornado Infernal': 20}


zones = {'Camino del Hierro Negro': 15}

bosses = [
	{'name':'Cazador de aventureros', 'life': 20,
	'attack': 7, 'defence': 7,
	'speed': 15, 'energy': 25,
	'aptitude':['great'], 'mana':0,
	'skills':[],'tecnique':['Tornado Infernal']}
 ]
#----------------------------------------------------------------------------


plainsEnemys = [
	{'name':'goblin', 'life': 5, 'att': 5, 'def': 3, 'sp': 5,'en': 4, 'aptitude':'normal','mana':0,'sk':'','tecnique':'Doble Golpe'},
	{'name':'rata', '  life': 3, 'att': 3, 'def': 1, 'sp': 8,'en': 4, 'aptitude':'dumb','mana':0,'sk':'','tecnique':''},
	{'name':'slime',   'life': 5, 'att': 3, 'def': 1, 'sp': 3,'en': 4, 'aptitude':'dumb','mana':0,'sk':'','tecnique':''},
	{'name':'zombie',  'life': 14, 'att': 2, 'def': 1,'sp': 1,'en': 2, 'aptitude':'dumb','mana':0,'sk':'','tecnique':''},

	{'name':'aprendiz magico','life': 8 , 'att': 1 , 'def':2,'sp': 10,'en':6,
	'ap':'magicNormal', 'mana':7, 'skills':'Golpe Chispa','tecnique':''}
]

# ------------------------ CAMINO DEL HIERRO NEGRO ------------------------------
blackIronPathParameters = {'world':'Camino del Hierro Negro','advanceCost':2, 'encounter': 4, 
'dropChance': 4, 'posibleDrops': {'pocion de vida':1, 'pocion de energia':1, 'pocion de mana':1}, 
'evadeFight': 2}
blackIronPath = [
	{'name':'Luchador Vagabundo', 'life': 8, 
	'att': 10, 	'def': 10, 
	'sp': 10,	'en': 10, 
	'mana':0, 'aptitude':['dumb'],'skills':[]},

	{'name':'Esgrimista', 'life': 10, 
	'att': 16, 	'def': 4, 
	'sp': 16,	'en': 10, 
	'mana':0, 'aptitude':['dumb'],'skills':['Doble Golpe']},

	{'name':'Arquero', 'life': 8, 
	'att': 15, 	'def': 5, 
	'sp': 10, 	'en': 22, 
	'mana':0, 'aptitude':['dumb'],'skills':[]},

	{'name':'Caballero Desterrado', 'life': 32,
	'att': 8, 'def': 18, 
	'sp': 10, 'en': 15, 
	'mana':0, 'aptitude':['great'],'skills':[]},

	{'name':'Individuo Encapuchado', 'life': 14, 
	'att': 2,  'def': 10, 
	'sp': 20,  'en':10 ,
	'mana':18, 'aptitude':['magicNormal'],'skills':['Rafaga de Viento']}
]
#{'name':'', 'life': , 'att': , 'def': , 'sp': ,'en': ,'mana':,'ap':[],'sk':[]}
bossDialogues = ['''estuve esperandote . . .         
	como aventurero, tu deber es enfrentar adversidades 
	para viajeros como tu 
	yo soy la adversidad'''
]
'''create table test ( 
name varchar(20),
life INTEGER,
maxLife INTEGER,
energy INTEGER,
maxEnergy INTEGER,
exp INTEGER,
maxExp INTEGER,
attack INTEGER,
defence INTEGER,
speed INTEGER,
class varchar(60),
states varchar(500),
mana INTEGER,
maxMana INTEGER,
skills varchar(900),
tecniques varchar(900),
level INTEGER,
world varchar(60),
avalibleEnemys varchar(200),
days INTEGER
); SON PUTOS 19 CAMPOS LETS FUCKING GO

def oldStatusBar(player,enemy, turn):
	print(f'\n------------------------------- Barra de Status -------------------------------------------',#screen
		  '\npuntos de vida de ->{}<-: {}/{}  -  energia: {} / {} - Mana:{} / {} - estado:{}'.format( player.name, round(player.life,2), player.maxLife, player.energy, player.maxEnergy,player.mana,player.maxMana, player.states) ,
		  '\npuntos de vida de ->{}<-: {}/{}  -  energia: {} / {} - Mana:{} / {} - estado:{}\nturno: {}\n'.format(enemy.name, round(enemy.life,  2) , enemy.maxLife, enemy.energy, enemy.maxEnergy, enemy.mana,enemy.maxMana, enemy.states,turn),
		  f'---------------------------------------------------------------------------------------------\n\n\n\n')#tengo que hacer un salto de pagina
'''