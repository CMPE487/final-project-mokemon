from abc import ABC, abstractmethod
class UI(ABC):
  def __init__(self):
    self.rooms = {}
    pass
  
  @abstractmethod
  def getUserName(self):
    pass
  
  @abstractmethod
  def showActionList(self):
    pass

  @abstractmethod
  def createRoom(self):
    pass

  @abstractmethod
  def showRoom(self,title,creatorName):
    pass
  @abstractmethod
  def getActionRoom(self):
    pass
  
  @abstractmethod
  def showListRooms(self):
    pass
  
  @abstractmethod
  def notificationListRooms(self,creatorIP,title,creatorName):
    pass