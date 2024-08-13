class OpenPipeIHMController:
  
  def subscribeToTag(self, tag, callback):
      return

  def unsubscribeToTag(self, tag):
      raise NotImplementedError

  def readTag(self, tag):
      raise NotImplementedError

  def writeTag(self, tag, value):
      raise NotImplementedError

  def subscribeToAlarm(self, alarm, callback):
      raise NotImplementedError

  def unsubscribeToAlarm(self, alarm):
      raise NotImplementedError

  def readAlarm(self, alarm):
      raise NotImplementedError

  def writeAlarm(self, alarm, value):
      raise NotImplementedError