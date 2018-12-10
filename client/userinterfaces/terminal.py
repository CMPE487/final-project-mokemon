import traceback
from userinterfaces.ui import UI
class Terminal(UI):
  def __init__(self):
    super().__init__()

  def getUserName(self):
    return input("Enter Username: ")
  
  def printActionList(self):
    print("Actions: (Write Action Number)")
    print("1 - Create Room")
    print("2 - List Rooms")
    print("3 - Create Tournament")
    print("4 - Join Tournament")

  def showActionList(self):
    while True:
      self.printActionList()
      action = input()
      try:
        actionNumber = int(action)
        if actionNumber > 0 and actionNumber < 5:
          return actionNumber
      except Exception as e:
        pass

  def createRoom(self):
    options = {}
    options["back"] = False
    options["title"] = input("Title: (/back)\n")
    if options["title"] == "/back":
      options["back"] = True
    return options
  
  def readyNotification(self,playerName):
    print(playerName+" is ready!")

  def showRoom(self,title,creatorName):
    print("Room: "+title+" Created By: "+creatorName)
  
  def getActionRoom(self):
    action = ""
    while True:
      action = input("Write ready. (/back)\n")
      if action == "ready" or action == "/back":
        break
    return action

  def notificationListRooms(self,creatorIP,title,creatorName):
    roomID = str(len(list(self.rooms.keys()))+1)
    print(roomID+" - "+title+"/creator:"+creatorName)
    self.rooms[roomID] = (creatorIP,title,creatorName)

  def showListRooms(self):
    print("Available Rooms: ")
    # TODO consider removed rooms
    # return roomCreatorIp
    while True:
      message = input()
      # TODO improve
      if message == "/back":
        return message
      try:
        id = int(message)
        if id <= len(list(self.rooms.keys())) and id >-1:
          break
      except Exception as e:
        traceback.print_exc()
        print("Enter a valid room id!")
    return self.rooms[str(id)]