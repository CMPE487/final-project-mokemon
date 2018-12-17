import traceback
import tkinter as tk
from tkinter import simpledialog
from frames.inroom import InRoom
from frames.intournament import InTournament
class MainPage(tk.Frame):
  def __init__(self, master):
    tk.Frame.__init__(self, master)
    self._master = master
    self._label = tk.Label(self, text="Welcome to Mokemon!")
    self._label.pack(side="top", fill="x", pady=10)
    # create room
    tk.Label(self,text="Room Title: ").pack()
    self._roomTitle = tk.Entry(self, width=35)
    self._roomTitle.pack()
    tk.Button(self, text="Create Room",
              command=lambda: self.createRoom()).pack()
    # create tournament
    tk.Label(self,text="Tournament Title: ").pack()
    self._tournamentTitle = tk.Entry(self, width=35)
    self._tournamentTitle.pack()
    tk.Button(self, text="Create Tournament",
              command=lambda: master.switch_frame(InTournament)).pack()
    # room list
    tk.Label(self,text="Room List: ").pack()
    self._roomList = tk.Listbox(self, name='roomList')
    self._roomList.pack()
    self._roomList.bind('<<ListboxSelect>>', self.roomClick)
    # tournament list
    tk.Label(self,text="Tournament List: ").pack()
    self._tournamentList = tk.Listbox(self, name='tournamentListb')
    self._tournamentList.pack()
    self._tournamentList.bind('<<ListboxSelect>>', self.tournamentClick)
    self.getUsername()

  # create room button click event
  def createRoom(self):
    roomTitle = self._master._username + "'s Room"
    if self._roomTitle.get() != "":
      print("room title not empty")
      roomTitle = self._roomTitle.get()
    message = "createRoom;"+roomTitle+";"+self._master._username
    self._master.sendToServer(message)
    self._master.switch_frame(InRoom)
  # room list item select event
  def roomClick(self,event):
    try:
      w = event.widget
      index = int(w.curselection()[0])
      value = w.get(index)
      print('You selected item %d: "%s"' % (index, value))
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
      self._master._username = simpledialog.askstring("Input", "Enter Username", parent=self)
    # print(self._master._username)
  
  # add new room
  def addRoom(self,creatorIP,title,creatorName):
    self._roomList.insert(tk.END, title)