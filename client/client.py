import traceback
import sys
import os
from socket import *
from threading import Thread
from config import *
from userinterfaces import *
from state import State

# global variables
global server_sock, username, currentState

def send_discover_message(to, pck):
  try:
    # try to open socket
    sock = socket(AF_INET, SOCK_STREAM)
    sock.settimeout(DISCOVER_TIMEOUT)
    sock.connect(to)
    sock.settimeout(None)
    sock.send(bytes(pck, "utf8"))
    resp = sock.recv(BUFFER_SIZE)
    data = resp.decode("utf8")
    ## "server" ; host_ip
    tag, server_ip = data.split(";")
    if tag == "server":
      global server_sock
      server_sock = sock
    else:
      server_sock = None
  except Exception as e:
    print("server is not: ", to, " and ", e)
    pass

def connect_to_server():
  arr = host.split(".")
  arr.pop()
  ip = ".".join(arr)
  threads = []
  # TODO for i in range(2, 254):
  for i in range(10, 11):
    req_ip = ip + "." + str(i)
    # if req_ip == host:
    # 	continue
    discover_pck = "discover;" + host + ";" + username
    thread = Thread(target=send_discover_message, args=((req_ip, port), discover_pck))
    thread.daemon = True
    threads.append(thread)
    thread.start()
  for thread in threads:
    thread.join()

# listens server and decode messages
def server_listener(s,ui):
  try:
    while True:
      data = ""
      current = s.recv(BUFFER_SIZE)
      if current == b'':
        # client connection is lost
        print("server connection is lost")
        break
      data = data + current.decode("utf-8")
      message = data.split(";")
      if message[0]=="discover":
        conn.sendall(str.encode("server;"+HOST))  
      elif message[0]=="listRooms":
        # send a notification for each room
        for room in message[1:]:
          roomInfo = room.split("#")
          creatorIP = roomInfo[0]
          title = roomInfo[1]
          creatorName = roomInfo[2]
          ui.notificationListRooms(creatorIP,title,creatorName)
      else:
        print("data: ",data)
  except Exception as e:
    traceback.print_exc()

# connect to server 
while(True):
  print("connecting to server..")
  connect_to_server()
  if(server_sock is None):
    print("Server not found")
    choice = input("Would you like to try again? (yes)")
    if choice == "yes":
      continue
    else:
      exit()
  else:
    print("connected successfully")
    break
# init ui
ui = Terminal()
username = ui.getUserName()
# TODO set line up in ui

# open listener
t = Thread(target=server_listener, args=(server_sock,ui))
t.daemon = True
t.start()
currentState = State.ActionList
# stores variables to share between states
extras = {}
while(True):
  if currentState == State.ActionList:
    # TODO improve this part ... 
    actionid = ui.showActionList()
    if actionid == 1:
      currentState = State.CreateRoom
    elif actionid == 2:
      currentState = State.ListRooms
    elif actionid == 3:
      currentState = State.CreateTournament
    elif actionid == 4:
      currentState = State.JoinTournament
    # update prevState
    extras["prevState"] = State.ActionList
  elif currentState == State.CreateRoom:
    options = ui.createRoom()
    if options["back"]:
      currentState = State.ActionList
    else:
      currentState = State.InRoom
      # notify server to create a new room
      message = "createRoom;"+options["title"]+";"+username
      server_sock.send(str.encode(message))
      extras["title"] = options["title"]
    # update prevState
    extras["prevState"] = State.CreateRoom
  elif currentState == State.InRoom:
    if extras["prevState"] == State.CreateRoom:
      # creator
      action = ui.showRoom(extras["title"],username)
      if action == "ready":
        # TODO consider unready
        # send ready message
        print("send message ready")
        message = "ready;"+host+";"+"creator"
        server_sock.send(str.encode(message))
      elif action == "/back":
        # TODO send remove room message
        print("send remove room message")
        currentState = State.ActionList
    elif extras["prevState"] == State.ListRooms:
      # participant
      # TODO get creator name and creator ready
      roomCreatorName = extras["roomCreatorName"]
      roomCreatorId = extras["roomCreatorId"]
      roomTitle = extras["title"]
      # TODO improve this logic
      # TODO send message to check creator ready 
      action = ui.showRoom(roomTitle,roomCreatorName)
      if action == "ready":
        # TODO consider unready
        # send ready message
        print("send message ready")
        message = "ready;"+host+";"+"participant"
        server_sock.send(str.encode(message))
      elif action == "/back":
        # TODO send remove room message
        print("send remove room message")
        currentState = State.ActionList
      pass
    elif extras["prevState"] == State.InRoom:
      # TODO comes after ready?
      print("in room again")
      pass
    # update prevState
    extras["prevState"] = State.InRoom
  elif currentState == State.ListRooms:
    # get room list
    message = "listRooms"
    server_sock.send(str.encode(message))
    roomMessage = ui.showListRooms()
    if roomMessage == "/back":
      currentState = State.ActionList
      extras["prevState"] = State.ListRooms
      continue
    roomCreatorId, roomTitle, roomCreatorName = roomMessage
    # join room
    message = "joinRoom;" + roomCreatorId
    server_sock.send(str.encode(message))
    # set current state
    currentState = State.InRoom
    # set extras info
    extras["roomCreatorName"] = roomCreatorName
    extras["roomCreatorId"] = roomCreatorId
    extras["title"] = roomTitle
    extras["prevState"] = State.ListRooms
  else:
    message = input("new message: ")
    server_sock.send(str.encode(message))
