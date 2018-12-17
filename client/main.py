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
  while True:
    try:
      data = ""
      current = s.recv(1024)
      if not current:
        print("break")
        break
      data = current.decode("utf-8")
      print(type(app._frame).__name__)
      print("data received: ",data)
      # handle messages 
      if type(app._frame).__name__ == "MainPage":
        message = data.split(";")
        if message[0]=="listRooms":
          for room in message[1:]:
            roomInfo = room.split("#")
            creatorIP = roomInfo[0]
            title = roomInfo[1]
            creatorName = roomInfo[2]
            app._frame.addRoom(creatorIP,title,creatorName)
    except Exception as e:
      traceback.print_exc()

if __name__ == "__main__":
  app = MainApp(s,clientIp)
  t = Thread(target=listenServer)
  t.daemon = True
  t.start()
  app.title("Mokemon")
  app.geometry("600x600")
  app.focus_set()
  app.mainloop()
  s.close()
