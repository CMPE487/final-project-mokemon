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
    self._opponentName = args["opponentName"]
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
              command=lambda: self.backPressed()).pack()
    self._logLabel = tk.Label(self,text="Logs:\n")
    self._logLabel.pack()

  def backPressed(self):
    message = "battleLeft;"+self._battleKey+";"+self._side
    self._master.sendToServer(message)
    self._master.switch_frame(mpage.MainPage)

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

  def declareVictory(self,left=False):
    message = "You have defeated " + self._opponentName + "!"
    if left:
      message = "Opponent Left!\n" + message
    tk.messagebox.showinfo("Congratulations",message)
  def admitDefeat(self):
    tk.messagebox.showinfo("...","You have been defeated by " + self._opponentName + "!")
  
  # listener for Battle
  def listener(self,message):
    if message[0]=="turnUpdate":
      monsterInfo = message[1]
      opponentInfo = message[2]
      winner = int(message[3])
      log = message[4]
      self.updateMonsterInfo("my",monsterInfo)
      self.updateMonsterInfo("opponent",opponentInfo)
      self._logLabel["text"] += log
      self._isActive = True
      self._statusLabel["text"] = self._statusLabelActiveText
      if winner != -1:
        side = int(self._side)
        if winner == side:
          self.declareVictory()
        elif winner == 1-side:
          self.admitDefeat()
        self._master.switch_frame(mpage.MainPage)
    elif message[0] == "battleLeft":
      self.declareVictory(left=True)
      self._master.switch_frame(mpage.MainPage)