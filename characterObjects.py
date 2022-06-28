from asyncio.windows_events import NULL
from msilib.schema import Error
from multiprocessing.sharedctypes import Value
from  data import itemList, skillList, tecniqueList, statList
import time, random
from os import system
class character():
    def __init__(self,na,li,att,de,sp,en,mana,skills):#atributos base de cada personaje, contruidos al momento de creacion del objeto
        self.name = na
        self.life = li
        self.maxLife = li
        self.energy = en
        self.maxEnergy = en
        self.attack = att
        self.defence = de
        self.speed = sp
        self.exp = 0 
        self.maxExp = 5
        self.lvl = 0
        self.items = itemList
        self.states = []
        self.mana = mana
        self.maxMana = mana
        self.skills = skills

    def status(self):
        print(self.name,'--> Puntos de Vida:',self.life,'/',self.maxLife ,
        'Ataque:',self.attack,'Defensa :',self.defence,'Velocidad:',
        self.speed,'Nivel:', self.calculateLvL(),'energia:',self.energy,'/',self.maxEnergy,
        '\nmana:',self.mana,'/',self.maxMana, self.skills)
        return True
    
    def raw(self):
        print(self.life,self.maxLife,self.name, self.attack, self.defence, self.speed, self.energy,self.maxEnergy)

    def wait(self):
        print(self.name,'se calma por un momento, recuperando energia')
        self.addSomeStat('energy', (self.maxEnergy * 0.5))
        self.addSomeStat('mana' ,(self.maxMana * 0.3))
        return False
    
    def guard(self):
        print(self.name,'toma una posicion defensiva y prepara la postura para recibir un impacto.')
        self.addState('En Guardia')
        self.addSomeStat('energy', -1)
        self.addSomeStat('mana', (self.maxMana * 0.1))
        return False

    def basicAttack(self, defender):
        print('\n',self.name, 'ataca a ', defender.name)
        defender.calculateDamage(self.attack * 0.5, self)
        self.addSomeStat('energy', -2)
        time.sleep(0.3)
        return False

    def calculateDamage(self, dmg,  attacker):
        r = random.randint(0, 99)
        if 'En Guardia' in self.states:#reducir daño 60 %   --- Guardia
            dmg = dmg * 0.4
        elif 'Cansado' in self.states:#aumentar daño en 50 %
            dmg = dmg * 1.5
        else :                      #  reducir 30%          ---  entrada de daño normal 
            dmg = dmg * 0.7
        if dmg < 1:
            dmg = 1
        #--------------- calculo de evasion ---------------------
        evadeProb = 2 + (self.speed - attacker.speed )
        #print('evade prob:',evadeProb,'random int',r)#depuracion
        if evadeProb >= r:
            print(self.name,' ha evitado el ataque!!!\n')#screen

        else:
            print(self.name,' recibe  >',round(dmg, 2),'<  puntos de daño\n')#screen
            self.life = self.life - dmg

    def calculateLvL(self):
        return round((self.maxLife+self.attack+self.defence+self.speed)/4, 2)#ACABO DE HACER UN CAMBIO AQUI, NO LO ROMPAS

    def useItem(self,itemName):#funcionara usando solamente el nombre del item, posteriormente se comprueba su cantidad
        if itemName == 'pocion de vida':
            self.addSomeStat('life', 10)
        elif itemName  == 'pocion de energia':
            self.addSomeStat('energy', 10)
        elif itemName == 'pocion de mana':
            self.addSomeStat('mana', 15)
            
        self.items[itemName] = self.items[itemName] - 1
        print(self.name,'ha utilizado: ',itemName)

    def addItem(self, itemName, x):
        if itemName in itemList:
            self.items[itemName] = self.items[itemName] + x
            #print(x, itemName,' al inventario!')

            
        
#tony por favor , por favor usa estos metodos para mutar objetos porfavor la conchetumadre! -----------
    
    def addSomeStat(self, stat, amount):
        if stat == 'energy':
            self.energy = self.energy + amount
                
        elif stat == 'mana':
            self.mana = self.mana + amount
        
        elif stat == 'life':
            self.life = self.life + amount

        if self.energy > self.maxEnergy:#nivelacion por sobrepasar maximo de la skill
            self.energy = self.maxEnergy
        if self.mana > self.maxMana:
             self.mana = self.maxMana
        if self.life > self.maxLife:
            self.life = self.maxLife
        self.activeStates()

    def addState(self, state):
        if state != NULL:
            self.states.append(state)
            print(self.name,' esta: ',state)
        if state == 'Debilitado':#debo terminar el metodo export
            pass


    def activeStates(self):#escanea el objeto y segun ciertas condiciones, evalua condiciones de debuffs
        if self.energy <= self.maxEnergy * 0.25 and 'Cansado' not in self.states:
            self.addState('Cansado')

        elif self. energy > self.maxEnergy * 0.25 and 'Cansado' in self.states:
            self.states.remove('Cansado')

#tony por favor , por favor usa estos metodos para mutar objetos porfavor la conchetumadre! -----------

    def cleaner(self):
        listOfOneTurnBuffs =['En Guardia']#estados que duran un turno
        for x in listOfOneTurnBuffs:#recorrerlos
            if x in self.states:#si existe alguno al momento de iniciar el turno, eliminarlo
                self.states.remove(x)
            
    def resetToInitialState(self, maxLife, att, deff, speed, maxMana, maxEnergy):
        self.maxLife = maxLife
        self.attack = att
        self.defence = deff
        self.speed = speed
        self.maxMana = maxMana
        self.maxEnergy = maxEnergy
        
# ------------------ uso de skills
    def skillsAndTecniquesAvalible(self, showSkills):#comprueba si el objeto posee tecnicas asi como sus requerimientos de mana
        ready = []
        i = 0
        for x in skillList:
            if x['type'] == 'magic':
                if x['manaCost'] <= self.mana and x['name'] in self.skills :
                    ready.append(x['name'])
            elif x['type'] == 'tecnique':
                if x['energyCost'] <= self.energy and x['name'] in self.skills :
                    ready.append(x['name'])

        if showSkills:
            for y in ready:
                print(i,'._ ', y)
                i=i+1

        if ready == []:
            return False
        else:
            return ready


    def useSkill(self, defender):#disponible en el menu del jugador
        ready = self.skillsAndTecniquesAvalible(True)
        if ready == False:
            print('En Terminos de Habilidades, no Hay Habilidades Disponibles')#screen
            return True
        try:
            op = int(input('\n-->'))
            self.tecniqueSumary(ready[op],defender)
            return False

        except:
            print('dato invalido :(')#screen
            return True


    def tecniqueSumary(self, select, defender):
        for skill in skillList:
            if skill['name'] == select:

                i = 0# luego de localizar la skill, sigue el uso
                for strikes in skill['scaling']:
                    print(self.name, skill['message'][i])#screen
                    if skill['type'] == 'magic':
                        dmg = self.maxMana * skill['scaling'][i]
                        self.addSomeStat('mana', -skill['manaCost'])

                    elif skill['type'] == 'tecnique':
                        dmg =  self.attack * skill['scaling'][i]
                        self.addSomeStat('energy', -skill['energyCost'])

                    defender.calculateDamage(dmg, self)
                    i = i + 1

# ------------------ uso de skills

class mainCharacter(character):#mc personaje principal
    def __init__(self,na,li,att,de,sp,chClass,en,mana,skills):
        super().__init__(na,li,att,de,sp, en, mana, skills)
        self.chClass = chClass
        self.log = True
        self.skills = skills

    def status(self):#estado_mc
        print(self.name,'--> Puntos de Vida:',round(self.life,2),'/',self.maxLife,
        '\nNivel:' ,self.calculateLvL(), 'experiencia:',self.exp,'/',self.maxExp,
        '\nClase:',self.chClass,'----- energia :' ,self.energy,'/',self.maxEnergy,
        '\nPoder Magico:', self.mana,'/',self.maxMana,
        '\nAtaque:',self.attack,'\nDefensa :',self.defence,
        '\nVelocidad:',self.speed,'\nEstado:',self.states,
        '\nHabilidades : ',self.skills
        )
        return True

    def gainExp(self, amount):# --- ganar experiencia ---
        self.exp = self.exp + amount
        print('has ganado', amount , ' puntos de experiencia')

        if self.exp >= self.maxExp:# --- subir de nivel ---
            print('------------------- Subes de Nivel! -------------------')
            amount = 4

            while amount > 0:
                i = 0
                for stat in statList:#Screen
                    print(i,'._ ' , stat)
                    i = i+1
                print('puntos disponibles: ', amount)
                try:
                    attribute = int(input('caracteristica a mejorar? -->'))
                    attribute = statList[attribute]
                    skillPoints = int(input('cantidad a agregar? -->'))
                    amount = amount - skillPoints
                    self.addStat(attribute,  skillPoints )#trabajando aqui
                except:
                    print('alguno de los datos introducidos no fue valido :(')
                

                
            self.maxExp = self.maxExp + (self.maxExp * 0.30)
            self.exp = 0

    def addStat(self, attribute, amount):# --- aqui es donde se agregan las estadisticas ---

        if attribute == 'Vida':
            self.life = self.life +  amount
            self.maxLife = self.maxLife +  amount
        elif attribute == 'Ataque':
            self.attack = self.attack +  amount
        elif attribute == 'Defensa':
            self.defence =self.defence +  amount
        elif attribute == 'Velocidad':
            self.speed =self.speed + amount 
        elif attribute == 'Energia':
            self.maxEnergy =self.maxEnergy + amount 
        elif attribute == 'Mana':    
            self.maxMana =self.maxMana + amount
        else:
            print('>>> datos introducidos erroneamente al subir stats <<<', attribute, amount)
           

 
    def reStat(self, na, li, maxLi, en, maxEn, exp, maxExp, att, de, sp, chClass, mana, maxMana):# cambios en las estadisticas
        self.name = na
        self.life = li
        self.maxLife = maxLi
        self.energy = en
        self.maxEnergy = maxEn
        self.exp = exp
        self.maxExp = maxExp
        self.attack = att
        self.defence = de
        self.speed = sp
        self.chClass = chClass
        self.mana = mana
        self.maxMana = maxMana
    
    def showInventory(self):
        avalibleItems = []
        i = 0
        j = 0
        for item, cuantity in self.items.items():#lee cada clave y valor por separado del objeto en cuestion
            add=[]
            if cuantity > 0 :#mientras halla existencias del item, se mostrara en pantalla
                add.extend([i, item, cuantity])
                avalibleItems.append(add)
                i = i + 1
        print('Items Disponibles')#screen
        for i in avalibleItems:
                print(avalibleItems[j][0],'.__', avalibleItems[j][1], ' x ', avalibleItems[j][2])
                j = j + 1

        return avalibleItems#lista formato 3 espacios: index - nombre - cantidad que listo sos tony

    def inventory(self):
        j = 0
        avalibleItems = self.showInventory()
        try:
            op = int(input('x._ para Cancelar\nusar objeto nº -->'))
            if op != 'x':
                selectedItem = avalibleItems[op]
                self.useItem(selectedItem[1])
                return False
        except:
                print('valor invalido')
                return True
        else:
            print('no se utilizaron objetos')
            return True



    def turn(self,enemy):#------------------------------------aqui esta el menu del turno del personaje------------------
        loop=True
        menu = ['0._ limpiar consola','1._ Atacar','2._ Guardia',
        '3._ Habilidades' ,'4._Estado','5._ Esperar','6._ Objetos']
        self.cleaner()
        if self.energy <= 0:
            print(self.name,' esta demasiado cansado para actuar')
            self.wait()            
        else:
            while loop:
                time.sleep(0.3)#delay
                print()
                op = input(str(menu)+'\n---> ')
                print('\n')
                if op =='0':
                    system('cls')
                elif   op=='1':
                    loop = self.basicAttack(enemy)
                elif op == '2':
                    loop = self.guard()
                elif op == '3':
                    loop = self.useSkill(enemy)
                elif op == '4':
                    loop = self.status()
                elif op == '5':
                    loop = self.wait()
                elif op == '6':
                    loop = self.inventory()
                else:
                    print('\n opcion invalida. papuh')
                self.activeStates()


    def removeStatusAfterBattle(self):
        listOfBattleAlongBuffs =['Debilitado']
        for x in listOfBattleAlongBuffs:#recorrer
            if x in self.states:#si existe alguno al final del combate, eliminarlo
                self.states.remove(x)

class enemy(character):
    def __init__(self,na,li,att,de,sp,en, ap, mana, skills):
        super().__init__(na,li,att,de,sp, en, mana, skills)
        self.aptitude = ap

    def reStat(self,na,li,att,de,sp,en, ap, mana, skills):
        self.name = na
        self.life = li
        self.maxLife = li
        self.attack = att
        self.defence = de
        self.speed = sp
        self.energy = en
        self.maxEnergy = en
        self.mana = mana
        self.maxMana = mana
        self.items = itemList
        self.aptitude = ap  #comportamiento del enemigo: 
        self.skills = skills

        #items extra:
        if self.name == 'goblin':  
            self.addItem('pocion de vida', 1)

    def turn(self, player):
        op = random.randint(0,9)# tirada de dados del 0 al 9, basicamente
        self.cleaner()
        #print('esta es la tirada de dados del turno del enemigo:',op) #Depuracion Screen
        time.sleep(0.3)

        if 'dumb' in self.aptitude:# 90% atacar 10% esperar
            if self.energy >= 2:
                if op <=8:
                    self.basicAttack(player)
                else:
                    self.wait()
            else:
                self.wait()
#-----------------------------------------------------------
        elif 'normal' in self.aptitude:# con mas del 50% de vida: 60% atacar  20% defender 10% items
            if self.energy >= 2:        # menos de la       mitad: 60% curarse 20% defender 10% items
                if op <= 6 and self.life >= (self.maxLife * 0.5):
                    self.basicAttack(player)
                elif op <= 6 and self.life < (self.maxLife * 0.5) and self.items['pocion de vida'] > 1:
                    self.useItem('pocion de vida')              
                elif op == 7 or op == 8:
                    self.guard()
                elif op == 9 and self.energy < (self.maxEnergy * 0.9):
                    self.useItem('pocion de energia')
                else:
                    self.basicAttack(player)

            elif self.energy >=1:
                self.guard()
            else:
                self.wait()
#-----------------------------------------------------------
        elif 'magicNormal' in self.aptitude:# 100% tratar de lanzar skills / curarse
            if self.energy >= 1:#mientras halla 1 de energia
                if op <= 9 and self.skillsAndTecniquesAvalible(False) != False:
                    self.tecniqueSumary(random.choice(self.skillsAndTecniquesAvalible(False)), player) #usar skill aleatoria
                elif op <= 7 and self.life <= (self.maxLife * 0.5) and self.items['pocion de vida'] > 0:
                    self.useItem('pocion de vida')
                else:
                    self.guard()

            else:
                self.wait()
#----------------------------------------------------------- 
        elif 'great' in self.aptitude:# 40% skill - 30% basico - 20% guardia - 10% curarse (si falta vida)
            print(op)
            if self.energy >= 1 and self.skillsAndTecniquesAvalible(False) != False :#mientras halla 1 energia y skill disponible
                if op <= 3:
                    self.tecniqueSumary(random.choice(self.skillsAndTecniquesAvalible(False)), player) #usar skill aleatoria
                elif op <= 6  and self.life >= (self.maxLife * 0.5):
                    self.basicAttack(player)
                elif op <= 8:
                    self.guard()
                elif op == 9 and self.life != self.maxLife:
                    self.useItem('pocion de energia')

            elif self.energy >= 2:
                self.basicAttack(player)

            else:
                self.wait()
                
                    
                

                    
                    



