import random
import math
class Mika():
  def __init__(self):
    self._name = "Mika"
    self._description = "Mika mika"
    self._attackNames = ["Normal","Bam", "Dum"]
    self._image = "licky_front"
    self._imageBack = "licky_back"
    self._attack = 40
    self._armor = 10
    self._maxHP = 100
    self._speed = 10
    self._critx2 = 40
    self._critx3 = 30
    self._currentHP = self._maxHP
    self._actions = [self.attack1,self.attack2,self.attack3]

  def generateLog(self,attackId,damage,opponentName,opponentHP):
    return self._name + " used "+ self._attackNames[attackId] +" and dealt \n"+ str(damage) \
      + " damage to " + opponentName + " and "+ str(opponentHP)+ " HP left.\n"

  def attack1(self,monster):
    attackId = 0
    damage = max(self._attack - monster._armor,0)
    damage = math.floor(damage)
    monster._currentHP = max(monster._currentHP-damage,0)
    return self.generateLog(attackId,damage,monster._name,monster._currentHP)
  
  def attack2(self,monster):
    attackId = 1
    damage = max(self._attack - monster._armor,0)/3*2
    r = random.random()*100
    if r < self._critx2:
      damage *= 2
    damage = math.floor(damage)
    monster._currentHP = max(monster._currentHP-damage,0)
    return self.generateLog(attackId,damage,monster._name,monster._currentHP)
  
  def attack3(self,monster):
    attackId = 2
    damage = max(self._attack - monster._armor,0) / 3 * 2
    r = random.random()*100
    if r < self._critx3:
      damage *= 3
    damage = math.floor(damage)
    monster._currentHP = max(monster._currentHP-damage,0)
    return self.generateLog(attackId,damage,monster._name,monster._currentHP)