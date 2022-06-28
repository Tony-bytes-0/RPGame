from asyncio.windows_events import NULL
from  data import itemList, skillList, tecniqueList
import time, random
from os import system
class character():
    def __init__(self,na,li,att,de,sp,en,mana,skills,tecniques):#atributos base de cada personaje, contruidos al momento de creacion del objeto
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
        self.tecniques = tecniques

    def status(self):
        print(self.name,'--> Puntos de Vida:',self.life,'/',self.maxLife ,
        'Ataque:',self.attack,'Defensa :',self.defence,'Velocidad:',
        self.speed,'Nivel:', self.calculateLvL(),'energia:',self.energy,'/',self.maxEnergy,
        '\nmana:',self.mana,'/',self.maxMana, self.skills, self.tecniques)
        return True
    
    def raw(self):
        print(self.life,self.maxLife,self.name, self.attack, self.defence, self.speed, self.energy,self.maxEnergy)

    def wait(self):
        print(self.name,'se calma por un momento, recuperando energia')
        self.addSomeStat('energy', (self.maxEnergy * 0.5))
        self.addSomeStat('mana' ,(self.maxMana * 0.2))
        return False
    
    def guard(self):
        print(self.name,'toma una posicion defensiva y prepara la postura para recibir un impacto.')
        self.addState('En Guardia')
        self.addSomeStat('energy', -1)
        self.addSomeStat('mana', (self.maxMana * 0.1))
        return False

    def basicAttack(self, defender):
        print('\n',self.name, 'ataca a ', defender.name)
        defender.calculateDamage((  (self.attack * 0.5) - (defender.defence * 0.5)  +   1), self)
        self.addSomeStat('energy', -2)
        time.sleep(0.3)
        return False

    def calculateDamage(self, dmg,  attacker):
        r = random.randint(0, 99)
        if 'En Guardia' in self.states:#reducir daño 60 %
            dmg = dmg * 0.6
        elif 'Cansado' in self.states:#aumentar daño en 50 %
            dmg = dmg * 1.5
        if dmg < 1:
            dmg = 1
        #--------------- calculo de evasion ---------------------
        evadeProb = 2 + (attacker.speed - self.speed)
        print('evade prob:',evadeProb,'random int',r)#depuracion
        if evadeProb >= r:
            print(self.name,' ha evitado el ataque!!!')#screen
         #--------------- calculo de evasion ---------------------
        else:
            print(self.name,' recibe  >',round(dmg, 2),'<  puntos de daño!!!')#screen
            self.life = self.life - dmg

    def calculateLvL(self):
        return round((self.maxLife+self.attack+self.defence+self.speed)/4)

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
# ------------------ magias
    def tecniqueSumary(self, select, defender):#recibe un str con el nombre de la skill y la ejecuta
        totalDamage = 0
        if select == 'Golpe Chispa' and self.mana >= 5:# escalado: 50% poder magico - 50% ataque - penetracion 40%
            damage = (self.maxMana * 0.35 + self.attack * 0.15) - (defender.defence * 0.6)
            print('Envolviendo su Puño con Una Pequeña Flama Magica; ',self.name,' Lanza un Puñetazo!')#screen
            defender.calculateDamage(damage, self)
            self.addSomeStat('mana', -5)
        
        elif select == 'Rafaga de Viento' and self.mana >=9:# escalado: 70% poder magico - penetracion 35%
            damage = (self.maxMana * 0.6 ) - (defender.defence * 0.6)
            print('Enfocando su energia en la palma de su mano: ',self.name,' Dispara una Rafaga de Viento!')#screen
            defender.calculateDamage(damage, self)
            self.addSomeStat('mana', -9)
# ------------------ Tecnicas
        elif select == 'Doble Golpe':
            damage = ((self.attack * 0.5) - (defender.defence * 0.5)  +   1)
            print(self.name, 'golpea realizando un ataque rapido  ' , end='')
            defender.calculateDamage(damage, self)
            print('para rematar con un segundo golpe!  ', end='')
            defender.calculateDamage(damage, self)
        
        elif select == 'Tornado Infernal':
            print(self.name, ' Empuña sus armas y comienza un frenesi de giros incesantes que cortan contra ',
            defender.name,'\ntratando de conectar repetidos impactos')
            for x in [0.2, 0.1 , 0.5 , 0.1 , 0.3 , 0.2, 0.1]:
                damage = x * self.attack
                defender.calculateDamage(damage, self)
                totalDamage = totalDamage + damage
            print('daño total: ',totalDamage)
                

        else:
            print('no paso nada aqui en el metodo de usar skills uwu')#depuracion
           
        if select in ['Rafaga de Viento', 'Golpe Chispa']:#skills que restan uno de energia
            self.addSomeStat('energy', -1)
        
        elif select in ['Doble Golpe']:                 #tecnicas que gastan cinco de energia
            self.addSomeStat('energy', -5)
        
# ------------------ uso de skills
    def skillsAndTecniquesAvalible(self):#comprueba si el objeto posee tecnicas asi como sus requerimientos de mana
        all = {}
        all.update(skillList)
        all.update(tecniqueList)
        ready = []
        i = 0
        for x in all.keys():
            #print('habilidad de turno: ', x) a veces quiero imprimir las skill al recorrerlas xd
            if x in self.skills and self.mana >= skillList[str(x)]:#condiciones de uso
                print(i ,'._', x)
                ready.append(x)


            elif x in self.tecniques and self.energy >= tecniqueList[str(x)]:#condiciones de uso
                print(i ,'._', x)
                ready.append(x)

        if ready != []:
            return ready
        
        else:
            return False


    '''    def tecniquesAvalible(self):
        ready = self.skillsAndTecniquesAvalible()
        i = 0
        for x in tecniqueList.keys():
            if x in self.tecniques and self.energy >= tecniqueList[str(x)]:#condiciones de uso
                print(i ,'._', x)
                ready.append(x)'''

    def useSkill(self, defender):#disponible en el menu del jugador
        ready = self.skillsAndTecniquesAvalible()
        if ready == False:
            print('En Terminos de Habilidades, no Hay Habilidades Disponibles')
            return True

        try:
            op = int(input('\n-->'))
            self.tecniqueSumary(ready[op], defender)
            return False
        except:
            print('opcion invalida')
            return True
# ------------------ uso de skills

class mainCharacter(character):#mc personaje principal
    def __init__(self,na,li,att,de,sp,chClass,en,mana,skills, tecniques):
        super().__init__(na,li,att,de,sp, en, mana, skills, tecniques)
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
        '\nHabilidades : ',self.skills,
        '\nTecnicas : ',self.tecniques
        )
        return True

    def gainExp(self, amount):# --- ganar experiencia ---
        self.exp = self.exp + amount
        print('has ganado', amount , ' puntos de experiencia')

        if self.exp >= self.maxExp:# --- subir de nivel ---
            print('------------------- Subes de Nivel! -------------------')
            self.addStat( 2 )
            self.maxExp = self.maxExp + (self.maxExp * 0.30)
            self.exp = 0

    def addStat(self, amount):# --- aqui es donde se agregan las estadisticas ---
        def changueAtt(self, attribute, skillPoints):
            if attribute == 0:
                self.life = self.life +  skillPoints
                self.maxLife = self.maxLife +  skillPoints
            elif attribute == 1:
                self.attack = self.attack +  skillPoints
            elif attribute == 2:
                self.defence =self.defence +  skillPoints
            elif attribute == 3:
                self.speed =self.speed + skillPoints 
            elif attribute == 4:
                self.maxEnergy =self.maxEnergy + skillPoints 
            elif attribute == 5:    
                self.maxMana =self.maxMana + skillPoints    

        while amount > 0:#bucle para agregar puntos
             stats = [ 'Vida', 'Ataque', 'Defensa', 'Velocidad', 'Energia','Mana']
             i = 0
             for stat in stats:#mensaje en pantalla
                 print(i,'._ ' , stat)
                 i = i+1

             try:
                 attribute = int(input('caracteristica a mejorar? -->'))
                 print('puntos disponibles: ', amount)
                 skillPoints = int(input('cantidad a agregar? -->'))

                 if skillPoints <= amount:#agregar skillPoints
                     changueAtt(self, attribute, skillPoints)
                     amount = amount - skillPoints

                 else:
                     print('introduzca un numero entre 0 y ', amount)

             except TypeError or NameError or ValueError:
                 print(' algo salio mal :( ')
             except :
                print('ocurrio un error no capturable')
    
    def reStat(self, na, li, maxLi, en, maxEn, exp, maxExp, att, de, sp, chClass):# cambios en las estadisticas
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
        if self.energy <= 1:
            print(self.name,' esta demasiado cansado para actuar')
            self.wait()

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
    # ----------- no utilizable dentro del juego --------------
    def exportData(self, adventure):
        exportedEnemys = ",".join(adventure.avalibleEnemys)
        world = adventure.world
        return tuple([self.name, self.life, self.maxLife, self.energy, self.maxEnergy,
		self.exp, self.maxExp,self.attack, self.defence, self.speed, self.chClass,
        adventure.level, world, exportedEnemys, adventure.days])

class enemy(character):
    def __init__(self,na,li,att,de,sp,en, ap, mana, skills, tecniques):
        super().__init__(na,li,att,de,sp, en, mana, skills, tecniques)
        self.aptitude = ap

    def reStat(self,na,li,att,de,sp,en, ap, mana, skills, tecniques):
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
        self.tecniques = tecniques

        #items extra:
        if self.name == 'goblin':  
            self.addItem('pocion de vida', 1)

    def turn(self, player):
        op = random.randint(0,9)#tirada de dados del 0 al 9, basicamente
        print(op)
        time.sleep(0.3)

        if 'dumb' in self.aptitude:# 90% atacar 10% esperar
            if self.energy >= 2:
                if op <=8:
                    self.basicAttack(player)
            else:
                self.wait()
#-----------------------------------------------------------
        elif 'normal' in self.aptitude:# con mas del 50% de vida: 60% atacar  20% defender 20% items
            if self.energy >= 1:        # menos de la       mitad: 60% curarse 20% defender 20% items
                if op <= 6 and self.life >= (self.maxLife * 0.5):
                    self.basicAttack(player)

                elif op <= 6 and self.life < (self.maxLife * 0.5):
                    self.useItem('pocion de vida')
                
                elif op == 7 or op == 8:
                    self.guard()

                elif op == 9 and self.energy < (self.maxEnergy * 0.9):
                    self.useItem('pocion de energia')
                    print(self.name, ' Trata de usar un item, pero no le es posible')
                else:
                    self.basicAttack(player)
            else:
                self.wait()
#-----------------------------------------------------------
        elif 'magicNormal' in self.aptitude:# 60% tratar de lanzar skills / curarse
            
            if self.energy >= 1:#mientras halla 1 de energia
                if op <= 7 and self.skillsAndTecniquesAvalible() != False:
                    self.tecniqueSumary(random.choice(self.skillsAndTecniquesAvalible()), player) #usar skill aleatoria
                   
                elif op <= 7 and self.life <= (self.maxLife * 0.5):
                    self.useItem('pocion de energia')
                
                elif op == 8:
                    self.guard()

            if self.energy >= 2:
                self.basicAttack(player)

            else:
                self.wait()
#----------------------------------------------------------- 
        elif 'great' in self.aptitude:# 40% skill - 30% basico - 20% guardia - 10% curarse (si falta vida)
            print(op)
            if self.energy >= 1 and self.skillsAndTecniquesAvalible() != False :#mientras halla 1 energia y skill disponible
                if op <= 3:
                    self.tecniqueSumary(random.choice(self.skillsAndTecniquesAvalible()), player) #usar skill aleatoria
                   
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
                
                    
                

                    
                    



