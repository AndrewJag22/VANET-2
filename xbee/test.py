import struct

__author__ = 'Aakash'


lati = -89.987456
longi = -170.123456
speed = 100
compass = 122
devId = "0013A2004167387C"
tstamp = 1493482746

class conversion:
    def intToHex(self,val):
        return format(val, 'X')

    def hexToInt(self, val):
        return int(val, 16)

    def floatToHex(self, val):
        return struct.pack('>f', val).encode('hex')

    def hexToFloat(self, val):
        xval = struct.unpack('!f', str(val).decode('hex'))[0]
        #return round(xval, 5)
        return ("{:.6f}".format(xval))

    def pad(self, val , numBytes):
        vlen = (len(val)/2)
        x = numBytes - len(val)*4

c = conversion()
print (c.intConvert(1493482746))
print (c.hexToInt("5904BCFA"))
print(c.floatConvert(-179.123456))
print(c.hexToFloat('c3331f9b'))