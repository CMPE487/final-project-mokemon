from components.player import Player
class Battle():
  def __init__(self,title):
    self._title = title
    self._players = [None, None]
    self._turn = self.Turn()

  def setPlayer1(self,name,ip,conn):
    self._players[0] = Player(name,ip,conn)
  
  def setPlayer2(self,name,ip,conn):
    self._players[1] = Player(name,ip,conn)

  def setAction(self,side,actionId):
    side = int(side)
    self._turn._actionReceived[side] = True
    self._turn._actionIdList[side] = int(actionId)
  
  def checkTeamsSelected(self):
    return len(self._players[0]._team)>0 and len(self._players[1]._team)>0

  def sendToPlayer(self,playerId,message):
    self._players[playerId]._conn.sendall(str.encode(message))

  def turnUpdate(self):
    # check which action is first
    order = [1, 0]
    log = "Turn " + str(self._turn._number) + "\n"
    if self._players[0].getCurrentMonsterSpeed() > \
      self._players[1].getCurrentMonsterSpeed():
      order = [0, 1]
    for current in order:
      log += self._players[current].action(self._turn._actionIdList[current], \
        self._players[1-current].getCurrentMonster())
    self.newTurn()
    winner = self.checkBattleEnd()
    return log, winner

  def checkBattleEnd(self):
    winner = -1
    for i in range(2):
      if self._players[i].getCurrentMonsterCurrentHP()<=0:
        winner = 1-i
    return winner
    
  def newTurn(self):
    self._turn._number += 1
    self._turn._actionReceived = [False, False]
    self._turn._actionIdList = [0,0]
    
  def turnReady(self):
    return all(self._turn._actionReceived)
    
  class Turn():
    def __init__(self):
      self._number = 1
      self._actionReceived = [False, False]
      self._actionIdList = [0,0]