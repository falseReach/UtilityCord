import websocket #pip install websocket-client
import json
import threading
import time
import requests

class autoReplier:
    def __init__(self, token, id, message) -> None:
        self.AUTHENTICATION_PAYLOAD = {
        'op': 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "windows",
                "$browser": "chrome",
                "$device": 'pc'
            }
        }
    }
        self.HEARTBEAT_INTERVAL = 4.25 #seconds
        self.HEARTBEAT_PAYLOAD = {
                "op": 1,
                "d": "null"
            }
        self.DISCORD_WEBSOCKET = "wss://gateway.discord.gg/?encoding=json&v=9"
        self.REPLY_URL = "https://discord.com/api/v9/channels/{}/messages"
        self.ws = None
        self.token = token
        self.id = id
        self.message = message

    def heartbeat(self):
        print('Heartbeat begin')
        while True:
            self.ws.send(json.dumps(self.HEARTBEAT_PAYLOAD))
            print("Heartbeat sent")
            time.sleep(self.HEARTBEAT_INTERVAL)
    
    #Function only used internally for simplicity sake and to avoid errors. 
    #You can probably use it without error if you tried.
    def _reply(self, channel_id, message): 
        requests.post(self.REPLY_URL.format(channel_id), headers={'Authorization': self.token}, json={'content':message})
    
    def run(self):
        try:
            self.ws = websocket.WebSocket()
            self.ws.connect(self.DISCORD_WEBSOCKET)
            self.ws.send(json.dumps(self.AUTHENTICATION_PAYLOAD))
            
            #Starting heartbeat connection in seperate thread to keep Websocket connection alive.
            threading.Thread(target=self.heartbeat, args=[]).start()
            while True:
                receivedEvent = json.loads(self.ws.recv())
                
                #Checks if Event received is a message, a "DIRECT" message, and the author is not client. 
                if (receivedEvent['t'] == "MESSAGE_CREATE") and ("guild_id" not in receivedEvent['d']) and (self.id != receivedEvent['d']['author']['id']):
                    self._reply(receivedEvent['d']["channel_id"], self.message)

                print(receivedEvent)    
        except Exception as e:
            print(e)


if __name__ == "__main__":
    token = ""
    id = "" #Your id, it  should be in strings not integers.
    autoReplier(token, id, "hallo you have reached the skibidi services, I am not available right now, only in ohio").run()
