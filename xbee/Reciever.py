__author__ = 'Aakash'
import XBee_Threaded
from time import sleep
import mainThreaded

def recieve_module():
    xbee = XBee_Threaded.XBee("COM6")  # Your serial port name here

    Msg = xbee.Receive()
    if Msg:
        content = Msg[7:-1].decode('ascii')
        print("Msg: " + content)
        if Msg == "ex":
            xbee.shutdown()