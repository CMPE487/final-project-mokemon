import traceback
import tkinter as tk
import frames.mainpage as mpage
class Battle(tk.Frame):
  def __init__(self, master,args=None):
    tk.Frame.__init__(self, master)
    self._master = master
    # battle id
    self._battleKey = args["battleKey"]
    self._side = args["side"]
    # opponent info
    tk.Label(self,text="Opponent: "+args["opponentName"]).pack()
    self._opponentMonsterNameLabel = tk.Label(self,text="-")
    self._opponentMonsterNameLabel.pack()
    self._opponentMonsterHPLabel = tk.Label(self,text="-")
    self._opponentMonsterHPLabel.pack()
    self.updateMonsterInfo("opponent",args["opponentInfo"])
    # monster info
    self._monsterNameLabel = tk.Label(self,text="-")
    self._monsterNameLabel.pack()
    self._monsterHPLabel = tk.Label(self,text="-")
    self._monsterHPLabel.pack()
    self.updateMonsterInfo("my",args["monsterInfo"])
    tk.Label(self,text=self._master._username).pack()
    # action is not selected if true, otherwise false
    self._isActive = True
    self._statusLabelActiveText = "Select an action"
    self._statusLabelWaitingText = "Waiting for your opponent action"
    self._statusLabel = tk.Label(self,text=self._statusLabelActiveText)
    self._statusLabel.pack()
    # get action names
    actionNames = args["actionNames"].split("#")
    tk.Button(self, text=actionNames[0],command=lambda: self.action("0")).pack()
    tk.Button(self, text=actionNames[1],command=lambda: self.action("1")).pack()
    tk.Button(self, text=actionNames[2],command=lambda: self.action("2")).pack()
    tk.Button(self, text="Return to main page",
              command=lambda: master.switch_frame(mpage.MainPage)).pack()
    self._logLabel = tk.Label(self,text="Logs:\n")
    self._logLabel.pack()

  def updateMonsterInfo(self,side,monsterInfo):
    info = monsterInfo.split("#")
    if side == "opponent":
      self._opponentMonsterNameLabel["text"] = info[0]
      self._opponentMonsterHPLabel["text"] = "HP: "+info[1]+"/"+info[2]
    else:
      self._monsterNameLabel["text"] = info[0]
      self._monsterHPLabel["text"] = "HP: "+info[1]+"/"+info[2]

  def action(self,actionId):
    if self._isActive:
      self._isActive = False
      self._statusLabel["text"] = self._statusLabelWaitingText
      message = "battle;"+self._battleKey+";"+self._side+";"+actionId
      self._master.sendToServer(message)

  # listener for Battle
  def listener(self,message):
    if message[0]=="turnUpdate":
      monsterInfo = message[1]
      opponentInfo = message[2]
      self.updateMonsterInfo("my",monsterInfo)
      self.updateMonsterInfo("opponent",opponentInfo)
      log = message[3]
      self._logLabel["text"] += log
      self._isActive = True
      self._statusLabel["text"] = self._statusLabelActiveText
      # TODO announce winner 
      # already ready 
      # back
      # connection lost      
    