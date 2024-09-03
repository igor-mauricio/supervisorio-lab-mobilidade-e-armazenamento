import sys
sys.path.insert(0, '..\\')
import json

from infra.IHMController.Runtime import Runtime

def printOnSuccess(jsonResponse):
    # parse and print success json
    tagsInfo = jsonResponse["Params"]["Tags"]
    for tag in tagsInfo:
        print(
            "Name : {}\nErrorCode : {}\nError Description : {}\n\n".format(
                tag["Name"], tag["ErrorCode"], tag["ErrorDescription"]
            )
        )


def printOnError(jsonResponse):
    # parse and print error json
    print(
        "Message : {}\nError Code : {}\nErrorDescription : {}".format(
            jsonResponse["Message"],
            jsonResponse["ErrorCode"],
            jsonResponse["ErrorDescription"],
        )
    )


def callbackFunction(response):
    # Callback comes here from Runtime
    # do JSON loading in a try block to avoid invalid JSON processing.
    try:
        j = json.loads(response)
        msg = j.get("Message")
        if msg == "NotifyWriteTag":
            printOnSuccess(j)
        elif msg == "ErrorWriteTag":
            printOnError(j)
    except json.decoder.JSONDecodeError:
        print("response is not a valid JSON")





class OpenPipeIHMController:
  
  def subscribeToTag(self, tag, callback):
      return

  def unsubscribeToTag(self, tag):
      raise NotImplementedError

  def readTag(self, tag):
      raise NotImplementedError

  def writeTag(self, tag, value):
        global Runtime
        runtime = Runtime(callbackFunction)
        WriteTagCommand = '{"Message":"WriteTag","Params":{"Tags":[{"Name":"' + tag + '","Value":"'+ value +'"}]},"ClientCookie":" myCookie1"}\n'
        runtime.SendExpertCommand(WriteTagCommand)

  def subscribeToAlarm(self, alarm, callback):
      raise NotImplementedError

  def unsubscribeToAlarm(self, alarm):
      raise NotImplementedError

  def readAlarm(self, alarm):
      raise NotImplementedError

  def writeAlarm(self, alarm, value):
      raise NotImplementedError
  


# runtime = Runtime.Runtime(callbackFunction)
# SubscribeTagsExpertCommand = '{"Message":"SubscribeTag","Params":{"Tags":["Potato","Carrot", "Wheat", "Egg", "Bamboo", "Onion"]},"ClientCookie":"myCookie1"}\n'
# runtime.SendExpertCommand(SubscribeTagsExpertCommand)
# time.sleep(100)