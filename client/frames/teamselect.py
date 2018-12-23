import tkinter as tk
import frames.mainpage as mpage
from frames.battle import *
class TeamSelect(tk.Frame):
  def __init__(self, master,args=None):
    tk.Frame.__init__(self, master)
    self._master = master
    self._battleKey = args["battleKey"]
    self._side = args["side"]
    self._monsterSelected = False
    self._statusLabelActiveText = "Select a monster"
    self._statusLabelWaitingText = "Waiting for your opponent selection"
    self._statusLabel = tk.Label(self,text=self._statusLabelActiveText)
    
    
  # updates after frame change
  def updateAfterLoad(self):
    # get monster names and descriptions
    message = "monsterList;"
    self._master.sendToServer(message)
  
  def monsterSelect(self,monsterId):
    if not self._monsterSelected:
      self._monsterSelected = True
      self._statusLabel["text"] = self._statusLabelWaitingText
      message = "monsterSelect;"+self._battleKey+";"+self._side+";"+monsterId
      self._master.sendToServer(message)
      
  # listener for InRoom
  def listener(self,message):
    if message[0]=="monsterList":
      for i,monster in enumerate(message[1:]):
        info = monster.split("#")
        tk.Label(self, text=info[0]).pack() # name
        tk.Label(self, text=info[1]).pack() # description
        tk.Button(self, text="Ready", command=lambda: self.monsterSelect(str(i))).pack() # pokemon select
    elif message[0]=="initBattle":
      # battle key
      bKey = message[1]
      side = message[2]
      monsterInfo = message[3]
      actionNames = message[4]
      opponentInfo = message[5]
      opponentName = message[6]
      self._master.switch_frame(Battle,{
        "battleKey": bKey,
        "side": side,
        "monsterInfo": monsterInfo,
        "actionNames": actionNames,
        "opponentInfo": opponentInfo,
        "opponentName": opponentName
        })