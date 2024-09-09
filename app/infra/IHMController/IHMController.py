from abc import ABC, abstractmethod


class IHMController(ABC):
  @abstractmethod
  def subscribeToTag(self, tag, callback):...
  
  @abstractmethod
  def unsubscribeToTag(self, tag):...
  
  @abstractmethod
  def readTag(self, tag):...
  
  @abstractmethod
  def writeTag(self, tag, value):...
  
  @abstractmethod
  def subscribeToAlarm(self, alarm, callback):...
  
  @abstractmethod
  def unsubscribeToAlarm(self, alarm):...
  
  @abstractmethod
  def readAlarm(self, alarm):...
  
  @abstractmethod
  def writeAlarm(self, alarm, value):...


class FakeIHMController(IHMController):
    def __init__(self):
        self.tags = {}
        self.alarms = {}
    
    def subscribeToTag(self, tag, callback):
        return
    
    def unsubscribeToTag(self, tag):
        return
    
    def readTag(self, tag):
        return self.tags[tag]
    
    def writeTag(self, tag, value):
        self.tags[tag] = value
    
    def subscribeToAlarm(self, alarm, callback):
        return
    
    def unsubscribeToAlarm(self, alarm):
        return
    
    def readAlarm(self, alarm):
        return self.alarms[alarm]
    
    def writeAlarm(self, alarm, value):
        self.alarms[alarm] = value
  