_author__ = 'Aakash'
import XBee_Threaded
import convert
lati = -89.987456
longi = -170.12345
speed = 100
compass = 122
devId = "0013A2004167387C"
tstamp = 1493482746

if __name__ == "__main__":
    xbee = XBee_Threaded.XBee("COM6")  # Your serial port name here

   # xbee.Send(bytearray.fromhex("7e 7d 11 13 5b 01 01 01 01 01 01 01"))
    # A simple string message
    while True:
        payload = convert.packetencode(lati,longi,speed,compass,devId,tstamp)
        xbee.SendStr(payload)
        raw_input()
       #sent = xbee.SendStr(str)

    xbee.shutdown()
