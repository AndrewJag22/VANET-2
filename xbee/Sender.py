__author__ = 'Aakash'
import XBee_Threaded
from time import sleep

if __name__ == "__main__":
    xbee = XBee_Threaded.XBee("COM4")  # Your serial port name here

    # A simple string message

    str = raw_input("Type message to send: ")
    sent = xbee.SendStr(str)

    # A message that requires escaping
    #xbee.Send(bytearray.fromhex("7e 7d 11 13 5b 01 01 01 01 01 01 01"))
    if str == "ex":
        xbee.shutdown()