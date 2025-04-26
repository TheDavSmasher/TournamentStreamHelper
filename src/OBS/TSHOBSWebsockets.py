import time
import sys
from obswebsocket import obsws, requests
from TSHOBSWebsocketAuth import WEBSOCKET_HOST, WEBSOCKET_PORT, WEBSOCKET_PASSWORD


class OBSWebsocketManager:
    ws = None

    def __init__(self):
        self.ws = obsws()
        try:
            self.ws.connect()
        except:
            print("Connection failed")
            time.sleep(2)
            sys.exit()
        print("Connected")

    def disconnect(self):
        self.ws.disconnect()
