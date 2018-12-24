class Dragonub():
  def __init__(self):
    self._name = "Dragonub"
    self._description = "Dragoooo gono nub"
    self._attackNames = ["Normal","Dharo", "Pharo"]
    self._image = "licky_front"
    self._imageBack = "licky_back"
    self._attack = 25
    self._armor = 10
    self._maxHP = 100
    self._speed = 10
    self._currentHP = self._maxHP
    self._actions = [self.attack1,self.attack2,self.attack3]

  def generateLog(self,attackId,damage,opponentName,opponentHP):
    return self._name + " used "+ self._attackNames[attackId] +" and dealt "+ str(damage) \
      + " damage to " + opponentName + " and "+ str(opponentHP)+ " HP left.\n"

  def attack1(self,monster):
    attackId = 0
    damage = max(self._attack - monster._armor,0)
    monster._currentHP = max(monster._currentHP-damage,0)
    return self.generateLog(attackId,damage,monster._name,monster._currentHP)
  
  def attack2(self,monster):
    attackId = 1
    damage = max(self._attack - monster._armor,0)
    monster._currentHP = max(monster._currentHP-damage,0)
    return self.generateLog(attackId,damage,monster._name,monster._currentHP)
  
  def attack3(self,monster):
    attackId = 2
    damage = max(self._attack - monster._armor,0)
    damage = 1001
    monster._currentHP = max(monster._currentHP-damage,0)
    return self.generateLog(attackId,damage,monster._name,monster._currentHP)