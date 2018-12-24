import tkinter as tk
import frames.mainpage as mpage
from frames.battle import *
from functools import partial
import math
from PIL import Image, ImageTk

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
    print(monsterId)
    if not self._monsterSelected:
      self._monsterSelected = True
      self._statusLabel["text"] = self._statusLabelWaitingText
      message = "monsterSelect;"+self._battleKey+";"+self._side+";"+monsterId
      self._master.sendToServer(message)
      
  # listener for InRoom
  def listener(self,message):
    if message[0]=="monsterList":
      self._monsterIdList = []
      self._labels = []
      rows = int(math.sqrt(len(message)-1))
      cols = int((len(message)-1)/rows)
      k = 0
      l = 0
      for i,monster in enumerate(message[1:]):
        info = monster.split("#")
        tk.Label(self, text=info[0]).grid(row = 4*k, column = l) # name
        tk.Label(self, text=info[1]).grid(row = 4*k+1, column = l) # description
        icon = ImageTk.PhotoImage(Image.open("./resources/" + info[2] + "/icon.png").copy().convert('RGBA'))
        # print("./resources/" + info[2] + "/icon.png")
        self._labels.append(tk.Label(self, image=icon)) # icon)
        self._labels[i].photo = icon
        self._labels[i].grid(row = 4*k+2, column = l)
        tk.Button(self, text="Select", command=lambda i=i: self.monsterSelect(str(i))).grid(row = 4*k+3, column = l) # pokemon select
        l += 1
        if l == cols:
          l = 0
          k += 1
    elif message[0]=="initBattle":
      # battle key
      bKey = message[1]
      side = message[2]
      monsterInfo = message[3]
      monsterImage = message[4]
      actionNames = message[5]
      opponentInfo = message[6]
      opponentImage = message[7]
      opponentName = message[8]
      self._master.switch_frame(Battle,{
        "battleKey": bKey,
        "side": side,
        "monsterInfo": monsterInfo,
        "monsterImage": monsterImage,
        "actionNames": actionNames,
        "opponentInfo": opponentInfo,
        "opponentImage": opponentImage,
        "opponentName": opponentName
        })