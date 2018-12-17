import tkinter as tk
import frames.actionlist as actlist

class CreateRoomOptions(tk.Frame):
  def __init__(self, master):
    tk.Frame.__init__(self, master)
    tk.Label(self, text="Create Room Options").pack(side="top", fill="x", pady=10)
    tk.Button(self, text="Return to action list",
              command=lambda: master.switch_frame(actlist.ActionList)).pack()
