import traceback
from threading import Thread
import tkinter as tk
import socket
from frames import *

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
clientIp = socket.gethostbyname(socket.gethostname())
app = None
  
def listenServer():
  global app
  while True:
    try:
      data = ""
      current = s.recv(1024)
      if not current:
        print("Server is down!")
        break
      data = current.decode("utf-8")
      print(type(app._frame).__name__)
      print("data received: ",data)
      # handle messages 
      message = data.split(";")
      if hasattr(app._frame, 'listener'):
        app._frame.listener(message)
    except Exception as e:
      traceback.print_exc()

if __name__ == "__main__":
  app = MainApp(s,clientIp)
  t = Thread(target=listenServer)
  t.daemon = True
  t.start()
  app.title("Mokemon")
  app.focus_set()  
  app.mainloop()
  s.close()
