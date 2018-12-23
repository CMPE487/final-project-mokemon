import traceback
import tkinter as tk
import frames.mainpage as mpage
from frames.animatedGif import AnimatedGIF

class Battle(tk.Frame):
  def __init__(self, master,args=None):
    tk.Frame.__init__(self, master)  
    self._master = master
    # battle id
    self._battleKey = args["battleKey"]
    self._side = args["side"]
    self._opponentName = args["opponentName"]
    # opponent info
    tk.Label(self,text="Opponent: "+args["opponentName"]).grid(row = 0, column = 0, columnspan = 12, sticky = 'E')#, sticky = 'S'
    self._opponentMonsterNameLabel = tk.Label(self,text="-", width = 10, bg = "blue")
    self._opponentMonsterNameLabel.grid(row = 1, column = 6, columnspan = 2, sticky = 'EN')
    self._opponentMonsterImage = AnimatedGIF(self, "./resources/"+args["opponentImage"])
    self._opponentMonsterImage.grid(row = 1, column = 8, columnspan = 4, sticky = 'EW')
    self._opponentMonsterImage.start_animation()
    self._opponentMonsterHPLabel = tk.Label(self,text="-", width = 10, bg = "red")
    self._opponentMonsterHPLabel.grid(row = 5, column = 6, columnspan = 6, sticky = 'E')
    self.updateMonsterInfo("opponent",args["opponentInfo"])
    # monster info
    self._monsterHPLabel = tk.Label(self,text="-", width = 10, bg = "red")
    self._monsterHPLabel.grid(row = 6, column = 0, columnspan = 6, sticky = 'W')
    self._monsterImage = AnimatedGIF(self, "./resources/"+args["monsterImage"])
    self._monsterImage.grid(row = 7, column = 0, columnspan = 4, rowspan = 4, sticky = 'EW')
    self._monsterImage.start_animation()
    self._monsterNameLabel = tk.Label(self, text="-", width = 10, bg = "blue")
    self._monsterNameLabel.grid(row = 10, column = 4, columnspan = 2, sticky = 'WS')
    self.updateMonsterInfo("my",args["monsterInfo"])
    # action is not selected if true, otherwise false
    self._isActive = True
    self._statusLabelActiveText = "Select an action " + self._master._username
    self._statusLabelWaitingText = "Waiting for your opponent action"
    self._statusLabel = tk.Label(self,text=self._statusLabelActiveText)
    self._statusLabel.grid(row = 12, column = 0, columnspan = 6, sticky = 'EW')
    # get action names
    actionNames = args["actionNames"].split("#")
    self._firstActionButton = tk.Button(self, text=actionNames[0], width = 10)
    self._firstActionButton.bind("<Button-1>", lambda event: self.action("0"))
    self._firstActionButton.grid(row = 11, column = 0, columnspan = 2)#, sticky = 'S'
    self._secondActionButton = tk.Button(self, text=actionNames[1], width = 10)
    self._secondActionButton.bind("<Button-1>", lambda event: self.action("1"))
    self._secondActionButton.grid(row = 11, column = 2, columnspan = 2)#, sticky = 'S'
    self._thirdActionButton = tk.Button(self, text=actionNames[2], width = 10)
    self._thirdActionButton.bind("<Button-1>", lambda event: self.action("2"))
    self._thirdActionButton.grid(row = 11, column = 4, columnspan = 2)#, sticky = 'S'
    self._logLabel = tk.Label(self,text="Logs:\n", width = 40, bg = "green", relief = tk.SUNKEN, bd = 5, anchor = 'n')
    self._logLabel.grid(row = 0, column = 12, columnspan = 6, rowspan = 12, sticky = 'NSWE')
    self._retreatButton = tk.Button(self, text="Return to main page", width = 20, background = "red3")
    self._retreatButton.bind("<Button-1>", self.backPressed)
    self._retreatButton.grid(row = 12, column = 16, columnspan = 2, sticky = 'E')

  def backPressed(self, event):
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

  def action(self, actionId):
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
    m = "You have been defeated by " + self._opponentName + "!"
    tk.messagebox.showinfo("...",m)
  
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