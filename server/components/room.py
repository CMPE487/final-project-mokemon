class Room():
  def __init__(self,title,creatorIP,creatorName,conn):
    self.title = title
    self.creatorIP = creatorIP
    self.participantIP = ""
    self.participantName = ""
    self.creatorName = creatorName
    self.creatorReady = False
    self.participantReady = False
    self.full = False
    self.participantConnection = None
  
  # returns the room info for listRooms
  def getListString(self):
    return self.creatorIP+"#"+self.title+"#"+self.creatorName
  
  def getRoomLog(self):
    message = "Title: " + self.title + "\n"
    message += "creatorIP: " + self.creatorIP + "\n"
    message += "participantIP: " + self.participantIP + "\n"
    message += "creatorName: " + self.creatorName + "\n"
    message += "creatorReady: " + str(self.creatorReady) + "\n" 
    message += "participantReady: " + str(self.participantReady) + "\n"
    message += "full: " + str(self.full)
    return message
  
  def setCreatorConnection(self,conn):
    self.creatorConnection = conn
  
  def setParticipantInfo(self,participantName, participantIP, conn):
    self.participantName = participantName
    self.participantIP = participantIP
    self.participantConnection = conn
  
  # participant left the room
  def participantLeft(self):
    self.full = False
    self.participantName = ""
    self.participantIP = ""
    self.participantConnection = None