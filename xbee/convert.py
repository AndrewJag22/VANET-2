import struct

getBin = lambda x: x > 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]


def floatToBinary64(value):
    val = struct.unpack('Q', struct.pack('d', value))[0]
    return getBin(val)


def binaryToFloat(value):
    hx = hex(int(value, 2))
    return struct.unpack("d", struct.pack("q", int(hx, 16)))[0]


def floattohex(val):
    binstr = floatToBinary64(val)
    h = hex(int(binstr, 2))
    return h.split('x')[1].split('L')[0]


def hextofloat(val):
    val = '0x' + val + 'L'
    s = bin(int(val.split('L')[0], 16))
    q = int(s, 0)
    b8 = struct.pack('Q', q)
    return struct.unpack('d', b8)[0]


def inttohex(val):
    return format(val, 'x')


def hextoint(val):
    return int(val, 16)


def pad(val, n):
    return (n*2 - len(val)) * '0' + val


def packetencode(lati, longi, speed, compass, devId, tstamp):
    return pad(inttohex(tstamp), 5) + devId + pad(floattohex(lati), 8) + pad(floattohex(longi), 8) + pad(inttohex(speed), 2) + pad(inttohex(compass), 2)


def packetdecode(payload):
    tstamp = hextoint(payload[:10])
    devId = payload[10:26]
    lati = hextofloat(payload[26:42])
    longi = hextofloat(payload[42:58])
    speed = hextoint(payload[58:62])
    compass = hextoint(payload[62:])

    return tstamp, devId, lati, longi, speed, compass