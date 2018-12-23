import tkinter as tk
import frames.mainpage as mpage
from frames.battle import *
class InRoom(tk.Frame):
  def __init__(self, master,args=None):
    tk.Frame.__init__(self, master)
    self._master = master
    self._playerType = args["playerType"]
    tk.Label(self, text=args["title"]).grid(row = 0, column = 0, columnspan = 12, rowspan = 2, sticky = 'N')
    tk.Label(self, text="Player 1: ").grid(row = 2, column = 0, columnspan = 6, sticky = 'E')
    player1Text = self._master._username
    player2Text = " - "
    if self._playerType == "participant":
      player1Text = args["creatorName"]
      player2Text = self._master._username
      self._creatorIp = args["ip"]
      self.creatorName = args["creatorName"]
    self._player1Name = tk.Label(self, text=player1Text)
    self._player1Name.grid(row = 2, column = 6, columnspan = 6, sticky = 'W')
    tk.Label(self, text="Player 2: ").grid(row = 3, column = 0, columnspan = 6, sticky = 'E')
    self._player2Name = tk.Label(self, text=player2Text)
    self._player2Name.grid(row = 3, column = 6, columnspan = 6, sticky = 'W')
    self.readyButton = tk.Button(self, text="Ready", width = 18,
              command=lambda: 
                self.readyClick())
    self.readyButton.grid(row = 4, column = 0, columnspan = 6)
    tk.Button(self, text="Return to main menu", width = 18,
              command=lambda: 
                self.backButtonPressed()).grid(row = 4, column = 6, columnspan = 6)

  def backButtonPressed(self):
    # leave - destroy room message
    message = "leaveRoom;"
    message = message + self._playerType + ";"
    if self._playerType == "creator":
      message = message+self._master._ip
    else:
      message = message+self._master._ip
    self._master.sendToServer(message)

  # updates after frame change
  def updateAfterLoad(self):
    # check creator is already ready
    if self._playerType == "participant":
      message = "roomInfo;"+self._creatorIp
      self._master.sendToServer(message)
  
  # ready button click event
  def readyClick(self):
    # ready unready switch
    if self._playerType == "creator":
      if self._player1Name["text"].endswith(' | Ready'):
        self._player1Name["text"] = self._player1Name["text"][:-8]
        self.readyButton["text"] = "Ready"
      else:
        self._player1Name["text"] = self._player1Name["text"] + " | Ready"
        self.readyButton["text"] = "Unready"
    else:
      if self._player2Name["text"].endswith(' | Ready'):
        self._player2Name["text"] = self._player2Name["text"][:-8]
        self.readyButton["text"] = "Ready"
      else:
        self._player2Name["text"] = self._player2Name["text"] + " | Ready"
        self.readyButton["text"] = "Unready"
    message = "ready;"+self._master._ip+";"+self._playerType
    self._master.sendToServer(message)

  # update player2Name
  def playerCame(self,player2Name):
    self._player2Name["text"] = player2Name
  
  # update other player ready status
  def playerReady(self):
    # ready - unready toogle
    if self._playerType == "creator":
      if self._player2Name["text"].endswith(' | Ready'):
        self._player2Name["text"] = self._player2Name["text"][:-8]
      else:
        self._player2Name["text"] = self._player2Name["text"] + " | Ready"
    else:
      if self._player1Name["text"].endswith(' | Ready'):
        self._player1Name["text"] = self._player1Name["text"][:-8]
      else:
        self._player1Name["text"] = self._player1Name["text"] + " | Ready"
  
  # listener for InRoom
  def listener(self,message):
    if message[0]=="joinInfo":
      self.playerCame(message[1])
    elif message[0]=="readyNotification":
      self.playerReady()
    elif message[0]=="leaveRoom":
      self._master.switch_frame(mpage.MainPage)
    elif message[0]=="participantLeft":
      self._player2Name["text"] = " - "
    elif message[0]=="selectTeam":
      bKey = message[1]
      side = message[2]
      
    elif message[0]=="initBattle":
      # battle key
      bKey = message[1]
      side = message[2]
      monsterInfo = message[3]
      actionNames = message[4]
      opponentInfo = message[5]
      opponentName = self._player1Name["text"]
      if self._playerType == "creator":
        opponentName = self._player2Name["text"]
      if opponentName.endswith(' | Ready'):
        opponentName = opponentName[:-8]
      self._master.switch_frame(Battle,{
        "battleKey": bKey,
        "side": side,
        "monsterInfo": monsterInfo,
        "actionNames": actionNames,
        "opponentInfo": opponentInfo,
        "opponentName": opponentName
        })