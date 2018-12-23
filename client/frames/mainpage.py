import traceback
import tkinter as tk
from tkinter import simpledialog
from frames.inroom import InRoom
from frames.intournament import InTournament
from collections import OrderedDict
class MainPage(tk.Frame):
  def __init__(self, master):
    tk.Frame.__init__(self, master)
    self._master = master
    self._rooms = OrderedDict() # ip
    self._label = tk.Label(self, text="Welcome to Mokemon!")
    self._label.grid(row = 0, column = 0, columnspan = 12, rowspan = 2, sticky = 'N')
    # create room
    self.getUsername()
    tk.Label(self,text="Room Title: ").grid(row = 2, column = 0, columnspan = 4, sticky = 'E')
    self._roomTitle = tk.StringVar(self, value=self._master._username + "'s Room")
    self._roomTitleEntry = tk.Entry(self, textvariable=self._roomTitle)
    self._roomTitleEntry.grid(row = 2, column = 4,columnspan = 4)
    self._createRoomButton = tk.Button(self, text="Create Room", width = 14)
    self._createRoomButton.bind('<Button-1>', self.createRoom)
    self._createRoomButton.grid(row = 2, column = 8, columnspan = 4, sticky = 'W')
    # create tournament
    tk.Label(self,text="Tournament Title: ").grid(row = 3, column = 0, columnspan = 4, sticky = 'E')
    self._tournamentTitle = tk.StringVar(self, value=self._master._username + "'s Tournament")
    self._tournamentTitleEntry = tk.Entry(self, textvariable=self._tournamentTitle)
    self._tournamentTitleEntry.grid(row = 3, column = 4, columnspan = 4)
    self._createTournamentButton = tk.Button(self, text="Create Tournament", width = 14)
    self._createTournamentButton.bind('<Button-1>', lambda event: master.switch_frame(InTournament))
    self._createTournamentButton.grid(row = 3, column = 8, columnspan = 4, sticky = 'W')
    # room list
    tk.Label(self,text="Room List: ").grid(row = 4, column = 0, columnspan = 6)
    self._roomList = tk.Listbox(self, name='roomList')
    self._roomList.grid(row = 5, column = 0, columnspan = 6)
    self._roomList.bind('<<ListboxSelect>>', self.roomClick)
    # tournament list
    tk.Label(self,text="Tournament List: ").grid(row = 4, column = 6, columnspan = 6)
    self._tournamentList = tk.Listbox(self, name='tournamentListb')
    self._tournamentList.grid(row = 5, column = 6, columnspan = 6)
    self._tournamentList.bind('<<ListboxSelect>>', self.tournamentClick)

  # updates after frame change
  def updateAfterLoad(self):
    self._master.sendToServer("mainscreen")
    
  # create room button click event
  def createRoom(self, event):
    roomTitle = self._roomTitle.get()
    message = "createRoom;"+roomTitle+";"+self._master._username
    self._master.sendToServer(message)
    self._master.switch_frame(InRoom,{"playerType": "creator","title": roomTitle})
  
  # room list item select event
  def roomClick(self,event):
    try:
      w = event.widget
      index = int(w.curselection()[0])
      value = w.get(index)
      ip = list(self._rooms.keys())[index]
      roomInfo = self._rooms[ip] # (title,creatorName)
      message = "joinRoom;"+ip+";"+self.master._username
      self._master.sendToServer(message)
      self._master.switch_frame(InRoom,{
        "playerType": "participant",
        "ip": ip,
        "creatorName":roomInfo[1],
        "title":roomInfo[0]})
    except Exception as e:
      traceback.print_exc()
  
  # tournament list item select event
  def tournamentClick(self,event):
    try:
      w = event.widget
      index = int(w.curselection()[0])
      value = w.get(index)
      print('You selected item %d: "%s"' % (index, value))
    except Exception as e:
      traceback.print_exc()
  
  # get username from user
  def getUsername(self):
    while self._master._username == "" or self._master._username == None:
      self._master._username = simpledialog.askstring("Mokemon", "Enter Username", parent=self)
    # print(self._master._username)
  
  # add new room
  def addRoom(self,creatorIP,title,creatorName):
    print("room id: ",tk.END," , ",creatorName," , ",title)
    self._rooms[creatorIP] = (title,creatorName)
    self._roomList.insert(tk.END, title+" - "+creatorName)

  # listener for MainPage
  def listener(self,message):
    if message[0]=="listRooms":
      for room in message[1:]:
        roomInfo = room.split("#")
        creatorIP = roomInfo[0]
        title = roomInfo[1]
        creatorName = roomInfo[2]
        self.addRoom(creatorIP,title,creatorName)
    elif message[0]=="removeRoom":
      creatorIP = message[1]
      index = list(self._rooms.keys()).index(creatorIP)
      print("delete index: ",index)
      self._roomList.delete(index)
      self._rooms.pop(creatorIP,None)
