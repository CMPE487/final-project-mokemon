import tkinter as tk
import frames.mainpage as mpage

class InRoom(tk.Frame):
  def __init__(self, master,args=None):
    tk.Frame.__init__(self, master)
    self._master = master
    self._playerType = args["playerType"]
    print(self._playerType)
    tk.Label(self, text="In Room").pack(side="top", 
              fill="x", pady=10)
    tk.Label(self, text="Player 1: ").pack(side="top", 
              fill="x", pady=10)
    self._player1Name = tk.Label(self, text=self._master._username)
    self._player1Name.pack(side="top", fill="x", pady=10)
    tk.Label(self, text="Player 2: ").pack(side="top", 
              fill="x", pady=10)
    self._player2Name = tk.Label(self, text="Player 2 Name")
    self._player2Name.pack(side="top", fill="x", pady=10)
    self.readyButton = tk.Button(self, text="Ready",
              command=lambda: 
                self.readyClick())
    self.readyButton.pack()
    tk.Button(self, text="Return to main menu",
              command=lambda: 
                master.switch_frame(mpage.MainPage)).pack()

  def readyClick(self):
    message = "ready;"+self._master._ip+";"+self._playerType
    self._master.sendToServer(message)
    # TODO update ui