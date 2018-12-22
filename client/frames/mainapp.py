import tkinter as tk
from frames.mainpage import *

class MainApp(tk.Tk):
  def __init__(self,s,ip):
    tk.Tk.__init__(self)
    self._frame = None
    self._socket = s
    self._ip = ip
    self._username = None
    self.switch_frame(MainPage)
    
  def switch_frame(self, frame_class, args=None):
    """Destroys current frame and replaces it with a new one."""
    new_frame = None
    if args == None:
      new_frame = frame_class(self)
    else:
      new_frame = frame_class(self,args)
    if self._frame is not None:
      self._frame.destroy()
    self._frame = new_frame
    if hasattr(self._frame, 'updateAfterLoad'):
      self._frame.updateAfterLoad()
    self._frame.pack()
  
  def sendToServer(self,message):
    self._socket.sendall(str.encode(message))