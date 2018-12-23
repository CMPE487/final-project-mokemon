class Player():
  def __init__(self,name,ip,conn):
    self._name = name
    self._ip = ip
    self._conn = conn
  
  def setTeam(self,team):
    # [monster1,..]
    self._team = team

  def getCurrentMonster(self):
    return self._team[0]

  # returns log
  def action(self,actionId,monster):
    return self._team[0]._actions[actionId](monster)

  def getCurrentMonsterActionName(self,actionId):
    return self._team[0]._attackNames[actionId]

  def getCurrentMonsterSpeed(self):
    return self._team[0]._speed

  def getCurrentMonsterInfo(self):
    return self._team[0]._name + "#" + \
      str(self._team[0]._currentHP) + "#" + \
      str(self._team[0]._maxHP)
  
  def getCurrentMonsterActionList(self):
    return "#".join(self._team[0]._attackNames)