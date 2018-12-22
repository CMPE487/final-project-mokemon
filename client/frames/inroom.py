import tkinter as tk
import frames.mainpage as mpage

class InRoom(tk.Frame):
  def __init__(self, master,args=None):
    tk.Frame.__init__(self, master)
    self._master = master
    self._playerType = args["playerType"]
    tk.Label(self, text=args["title"]).pack(side="top", 
              fill="x", pady=10)
    tk.Label(self, text="Player 1: ").pack(side="top", 
              fill="x", pady=10)
    player1Text = self._master._username
    player2Text = " - "
    if self._playerType == "participant":
      player1Text = args["creatorName"]
      player2Text = self._master._username
      self._creatorIp = args["ip"]
      self.creatorName = args["creatorName"]
    self._player1Name = tk.Label(self, text=player1Text)
    self._player1Name.pack(side="top", fill="x", pady=10)
    tk.Label(self, text="Player 2: ").pack(side="top", 
              fill="x", pady=10)
    self._player2Name = tk.Label(self, text=player2Text)
    self._player2Name.pack(side="top", fill="x", pady=10)
    self.readyButton = tk.Button(self, text="Ready",
              command=lambda: 
                self.readyClick())
    self.readyButton.pack()
    tk.Button(self, text="Return to main menu",
              command=lambda: 
                self.backButtonPressed()).pack()

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
    # if args["playerType"] == "participant":
    #   # get room info
    #   message = "roomInfo;"+self._creatorIp
    #   self._master.sendToServer(message)
    pass
  
  # ready button click event
  def readyClick(self):
    # TODO ready unready switch
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
    # TODO update ui

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