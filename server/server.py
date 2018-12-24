import traceback
import socket
from threading import Thread
from components import *
from monsters import *

HOST = socket.gethostbyname(socket.gethostname())
# HOST = "46.101.195.117"
print(HOST)
TCP_PORT = 5000
BUFFER_SIZE = 1024
threads = []
rooms = {}
battles = {}
mainScreenUsers = []
monsterList = [Mika(),Dragonub(),AlienCopy()]

def sendRoomNotification(r):
  message = "listRooms;"+r.getListString()
  for wConn in mainScreenUsers:
    wConn.sendall(str.encode(message))

def sendAllRoomNotification(conn):
  print("sendall room")
  print(rooms)
  message = "listRooms"
  for roomID,room in rooms.items():
    if not room.full:
      message = message +";"+ room.getListString()
  conn.sendall(str.encode(message))

def handle_client(conn,addr):
  while True:
    try:
      data = ""
      current = conn.recv(BUFFER_SIZE)
      if current == b'':
        # TODO do necessary actions connection lost (rage quit)
        # client connection is lost
        print("exit", addr)
        break
      data = data + current.decode("utf-8")
      print("data: ",data)
      message = data.split(";")
      if message[0]=="discover":
        # discover message
        conn.sendall(str.encode("server;"+HOST))
      elif message[0]=="createRoom":
        # create room message
        mainScreenUsers.remove(conn)
        r = Room(message[1],message[3],message[2],conn)
        r.setCreatorConnection(conn)
        rooms[message[3]] = r
        # send notification to users in main screen
        sendRoomNotification(r)
      elif message[0] == "mainscreen":
        # in mainscreen message
        mainScreenUsers.append(conn)
        sendAllRoomNotification(conn)
      elif message[0] == "ready":
        # ready message - unready if already ready
        creatorIP = message[1]
        playerType = message[2]
        readyMessage = ""
        if playerType == "creator":
          if rooms[creatorIP].creatorReady:
            rooms[creatorIP].creatorReady = False
          else:
            rooms[creatorIP].creatorReady = True
          if rooms[creatorIP].full:
            readyMessage = "readyNotification;"+rooms[creatorIP].creatorName
        else:
          if rooms[creatorIP].participantReady:
            rooms[creatorIP].participantReady = False
          else:
            rooms[creatorIP].participantReady = True
          readyMessage = "readyNotification;"+rooms[creatorIP].participantName
        if rooms[creatorIP].participantReady and rooms[creatorIP].creatorReady:
          # start game
          print("start game: " + rooms[creatorIP].creatorName + 
            " and " + rooms[creatorIP].participantName)
          # init battle
          r = rooms[creatorIP]
          battles[creatorIP] = Battle(r.title)
          battles[creatorIP].setPlayer1(r.creatorName,r.creatorIP,r.creatorConnection)
          battles[creatorIP].setPlayer2(r.participantName,r.participantIP,r.participantConnection)
          # team select
          for i in range(2):
            m = "selectTeam;" + creatorIP + ";"+str(i)
            battles[creatorIP].sendToPlayer(i,m)
          # delete room
          rooms.pop(creatorIP, None)
        else:
          # send ready message
          if playerType == "creator":
            if rooms[creatorIP].full:
              rooms[creatorIP].participantConnection.sendall(str.encode(readyMessage))
          else:
            rooms[creatorIP].creatorConnection.sendall(str.encode(readyMessage))
      elif message[0] == "monsterList":
        m = "monsterList"
        ex = ""
        for monster in monsterList:
          ex += ";" +monster._name + "#" + monster._description + "#" + monster._image
        m += ex * 5
        conn.sendall(str.encode(m))
      elif message[0] == "monsterSelect":
        battleKey = message[1]
        side = int(message[2])
        monsterId = int(message[3])
        battles[battleKey]._players[side].setTeam([monsterList[monsterId].__class__()])
        if battles[battleKey].checkTeamsSelected():
          # send init battle message
          for i in range(2):
            m = "initBattle;" + battleKey + ";"+str(i)+";" + \
              battles[battleKey]._players[i].getCurrentMonsterInfo() + ";" + \
              battles[battleKey]._players[i].getCurrentMonsterImage("back") + ";" + \
              battles[battleKey]._players[i].getCurrentMonsterActionList() + ";" + \
              battles[battleKey]._players[1-i].getCurrentMonsterInfo() + ";" + \
              battles[battleKey]._players[1-i].getCurrentMonsterImage("front") + ";" + \
              battles[battleKey]._players[1-i]._name
            battles[battleKey].sendToPlayer(i,m)
      elif message[0] == "battle":
        battleKey = message[1]
        side = message[2]
        actionId = message[3]
        battles[battleKey].setAction(side,actionId)
        if battles[battleKey].turnReady():
          log, winner = battles[battleKey].turnUpdate()
          print("turn ready")
          print(log)
          # send update message
          for i in range(2):
            message = "turnUpdate;" + \
              battles[battleKey]._players[i].getCurrentMonsterInfo() + ";" + \
              battles[battleKey]._players[1-i].getCurrentMonsterInfo()+ ";" + \
              str(winner) + ";" +log
            battles[battleKey].sendToPlayer(i,message)
          # winner then remove battle
          if winner != -1:
            battles.pop(creatorIP,None)
      elif message[0] == "battleLeft":
        battleKey = message[1]
        side = message[2]
        battles[battleKey].sendToPlayer(1-int(side),"battleLeft")
      elif message[0] == "listRooms":
        # list only not full rooms
        print("listRooms",addr)
        message = "listRooms"
        for roomID,room in rooms.items():
          if not room.full:
            message = message +";"+ room.getListString()
        print("room list message: ",message)
        conn.sendall(str.encode(message))
      elif message[0] == "joinRoom":
        # participant join room message
        creatorIP = message[1]
        participantName = message[2]
        participantIp = message[3]
        rooms[creatorIP].setParticipantInfo(participantName, participantIp, conn)
        rooms[creatorIP].full = True
        # send join info to creator
        m = "joinInfo;"+rooms[creatorIP].participantName
        rooms[creatorIP].creatorConnection.sendall(str.encode(m))
        mainScreenUsers.remove(conn)
        # send clients in mainscreen to remove this room
        message = "removeRoom;"+creatorIP
        for wConn in mainScreenUsers:
          wConn.sendall(str.encode(message))
      elif message[0] == "roomInfo":
        creatorIp = message[1]
        if rooms[creatorIp].creatorReady:
          rooms[creatorIp].participantConnection.sendall(b"readyNotification")
      elif message[0] == "leaveRoom":
        playerType = message[1]
        creatorIP = message[2]
        if playerType=="creator":
          rooms[creatorIP].creatorConnection.sendall(b"leaveRoom")
          if rooms[creatorIP].full:
            rooms[creatorIP].participantConnection.sendall(b"leaveRoom")
          rooms.pop(creatorIP, None)
          # remove room message
          message = "removeRoom;"+creatorIP
          for wConn in mainScreenUsers:
            wConn.sendall(str.encode(message))
        else:
          pConn = rooms[creatorIP].participantConnection
          # send message to creator
          message = "participantLeft;"
          rooms[creatorIP].creatorConnection.sendall(str.encode(message))
          rooms[creatorIP].participantLeft()
          # send room available
          sendRoomNotification(rooms[creatorIP])
          pConn.sendall(b"leaveRoom")
      elif message[0]=="status":
        print("Room Info: ")
        for roomID,room in rooms.items():
          print(room.getRoomLog())
      else:
        conn.sendall(str.encode("empty;message"))
    except Exception as e:
      traceback.print_exc()
    
def main():
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      s.bind((HOST, TCP_PORT))
      s.listen(50)
      while True:
        conn, addr = s.accept()
        print(addr)
        t = Thread(target=handle_client,args=(conn, addr))
        t.daemon = True
        threads.append(t)
        t.start()
  except Exception as e:
    print("Socket is closed!")
    s.close()
    traceback.print_exc()

main()