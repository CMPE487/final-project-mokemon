import tkinter as tk
from frames.mainpage import *

class MainApp(tk.Tk):
  def __init__(self,s):
    tk.Tk.__init__(self)
    self._frame = None
    self._socket = s
    self._username = None
    self.switch_frame(MainPage)
    
  def switch_frame(self, frame_class, args=None):
    """Destroys current frame and replaces it with a new one."""
    new_frame = frame_class(self)
    if self._frame is not None:
      self._frame.destroy()
    self._frame = new_frame
    self._frame.pack()
  
  def sendToServer(self,message):
    self._socket.sendall(str.encode(message))