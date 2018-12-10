class Room():
  def __init__(self,title,creatorIP,creatorName):
    self.title = title
    self.creatorIP = creatorIP
    self.participantIP = ""
    self.creatorName = creatorName
    self.creatorReady = False
    self.participantReady = False
    self.full = False
  
  # returns the room info for listRooms
  def getListString(self):
    return self.creatorIP+"#"+self.title+"#"+self.creatorName
  