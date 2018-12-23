class Mika():
  def __init__(self):
    self._name = "Mika"
    self._description = "Mika mika"
    self._attackNames = ["Normal","Bam", "Dum"]
    self._attack = 25
    self._armor = 10
    self._maxHP = 100
    self._speed = 10
    self._currentHP = self._maxHP
    self._actions = [self.attack1,self.attack2,self.attack3]

  def attack1(self,monster):
    print("attack 1")
    damage = max(self._attack - monster._armor,0)
    monster._currentHP = max(monster._currentHP-damage,0)
    return self._name + " dealt "+ str(damage) + " damage to " + \
      monster._name + " and "+ str(monster._currentHP)+ " HP left.\n"
  
  def attack2(self,monster):
    print("attack 2")
    damage = max(self._attack - monster._armor,0)
    monster._currentHP = max(monster._currentHP-damage,0)
    return self._name + " dealt "+ str(damage) + " damage to " + \
      monster._name + " and "+ str(monster._currentHP)+ " HP left.\n"
  
  def attack3(self,monster):
    print("attack 3")
    damage = max(self._attack - monster._armor,0)
    monster._currentHP = max(monster._currentHP-damage,0)
    return self._name + " dealt "+ str(damage) + " damage to " + \
      monster._name + " and "+ str(monster._currentHP)+ " HP left.\n"