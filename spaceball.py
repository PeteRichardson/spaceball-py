import serial
import re

class SpaceBallEvent:
    def __init__(self, type, data):
        self.type = type
        self.data = data

    @classmethod
    def create(cls, type, data):
        if type == 'K':
            return SpaceBallKeyEvent(data)
        elif type == 'D':
            return SpaceBallDataEvent(data)
        else:
            return SpaceBallEvent(type, data)

    def __str__(self):
        result = ""
        if self.type in ['K','D']:
            result += self.type
        else:
            result += "{:02x}".format(ord(self.type))
            #brep = "{:08b}".format(ord(c))
        for c in self.data:
            result += " {:02x}".format(c)
        return result

    def run(self, handlers):
        pass

class SpaceBallKeyEvent (SpaceBallEvent):
    last_key_data = [0x40, 0x40]

    def __init__(self, data):
        SpaceBallEvent.__init__(self, 'K', data)

        self.key_pick_down = (self.data[0] & 0x10) & ~ (SpaceBallKeyEvent.last_key_data[0] & 0x10)
        self.key_1_down = (self.data[1] & 0x01) & ~ (SpaceBallKeyEvent.last_key_data[1] & 0x01)
        self.key_2_down = (self.data[1] & 0x02) & ~ (SpaceBallKeyEvent.last_key_data[1] & 0x02)
        self.key_3_down = (self.data[1] & 0x04) & ~ (SpaceBallKeyEvent.last_key_data[1] & 0x04)
        self.key_4_down = (self.data[1] & 0x08) & ~ (SpaceBallKeyEvent.last_key_data[1] & 0x08)
        self.key_5_down = (self.data[0] & 0x01) & ~ (SpaceBallKeyEvent.last_key_data[0] & 0x01)
        self.key_6_down = (self.data[0] & 0x02) & ~ (SpaceBallKeyEvent.last_key_data[0] & 0x02)
        self.key_7_down = (self.data[0] & 0x04) & ~ (SpaceBallKeyEvent.last_key_data[0] & 0x04)
        self.key_8_down = (self.data[0] & 0x08) & ~ (SpaceBallKeyEvent.last_key_data[0] & 0x08)

        self.key_pick_up = ~ (self.data[0] & 0x10) & (SpaceBallKeyEvent.last_key_data[0] & 0x10)
        self.key_1_up = ~ (self.data[1] & 0x01) & (SpaceBallKeyEvent.last_key_data[1] & 0x01)
        self.key_2_up = ~ (self.data[1] & 0x02) & (SpaceBallKeyEvent.last_key_data[1] & 0x02)
        self.key_3_up = ~ (self.data[1] & 0x04) & (SpaceBallKeyEvent.last_key_data[1] & 0x04)
        self.key_4_up = ~ (self.data[1] & 0x08) & (SpaceBallKeyEvent.last_key_data[1] & 0x08)
        self.key_5_up = ~ (self.data[0] & 0x01) & (SpaceBallKeyEvent.last_key_data[0] & 0x01)
        self.key_6_up = ~ (self.data[0] & 0x02) & (SpaceBallKeyEvent.last_key_data[0] & 0x02)
        self.key_7_up = ~ (self.data[0] & 0x04) & (SpaceBallKeyEvent.last_key_data[0] & 0x04)
        self.key_8_up = ~ (self.data[0] & 0x08) & (SpaceBallKeyEvent.last_key_data[0] & 0x08)

    def __str__(self):
       return SpaceBallEvent.__str__(self)

    def run(self, handlers):
        if self.key_pick_up:
            handlers["key_pick_up"](self)
        elif self.key_pick_down:
            handlers["key_pick_down"](self)

        if self.key_1_up:
            handlers["key_1_up"](self)
        elif self.key_1_down:
            handlers["key_1_down"](self)

        if self.key_2_up:
            handlers["key_2_up"](self)
        elif self.key_2_down:
            handlers["key_2_down"](self)

        if self.key_3_up:
            handlers["key_3_up"](self)
        elif self.key_3_down:
            handlers["key_3_down"](self)

        if self.key_4_up:
            handlers["key_4_up"](self)
        elif self.key_4_down:
            handlers["key_4_down"](self)

        if self.key_5_up:
            handlers["key_5_up"](self)
        elif self.key_5_down:
            handlers["key_5_down"](self)

        if self.key_6_up:
            handlers["key_6_up"](self)
        elif self.key_6_down:
            handlers["key_6_down"](self)

        if self.key_7_up:
            handlers["key_7_up"](self)
        elif self.key_7_down:
            handlers["key_7_down"](self)

        if self.key_8_up:
            handlers["key_8_up"](self)
        elif self.key_8_down:
            handlers["key_8_down"](self)

        SpaceBallKeyEvent.last_key_data = self.data

def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is


class SpaceBallDataEvent (SpaceBallEvent):
    def __init__(self, data):
        SpaceBallEvent.__init__(self, 'D', data)
        self.period = (self.data[0] * 256 + self.data[1]) / 16.0
        self.Tx = twos_comp(self.data[ 2] * 256 + self.data[ 3],16)
        self.Ty = twos_comp(self.data[ 4] * 256 + self.data[ 5],16)
        self.Tz = twos_comp(self.data[ 6] * 256 + self.data[ 7],16)

        self.Rx = twos_comp(self.data[ 8] * 256 + self.data[ 9],16)
        self.Ry = twos_comp(self.data[10] * 256 + self.data[11],16)
        self.Rz = twos_comp(self.data[12] * 256 + self.data[13],16)


    def __str__(self):
        msg = "D,"
        msg += "{:6.3f},".format(self.period)
        msg += "{:6d},{:6d},{:6d},".format(self.Tx, self.Ty, self.Tz)
        msg += "{:6d},{:6d},{:6d}".format(self.Rx, self.Ry, self.Rz)
        return msg

    def run(self, handlers):
        handlers["data"](self)


class SpaceBall:

    def __init__(self, tty='/dev/tty.USA19QW1P1.1'):
        self.tty = tty
        self.ser = serial.Serial(timeout=None)
        self.ser.baudrate = 9600
        self.ser.port = self.tty
        self.ser.open()
        self.ser.reset_input_buffer()

        config_data = [
            "\x0D",                 # Clear the line
            "CB\x0D",               # Communications Mode Set to Binary
            "NT\x0DFT?\x0DFR?\x0D", # Set Null Region and Trans and Rot Sensitivity
            "P@r@r\x0D",            # Data rate to 20 events per Second
            "MSSV\x0D",             # Ball Event Type: Trans and Rot Vectors
            "Z\x0D",                # Rezero the ball
            "Bc\x0D",               # Beep it
            "H"
        ]
        for msg in config_data:
            self.ser.write(msg)

        self.handlers = dict.fromkeys([
            'key_pick_up',
            'key_1_up',
            'key_2_up',
            'key_3_up',
            'key_4_up',
            'key_5_up',
            'key_6_up',
            'key_7_up',
            'key_8_up',
            'key_pick_down',
            'key_1_down',
            'key_2_down',
            'key_3_down',
            'key_4_down',
            'key_5_down',
            'key_6_down',
            'key_7_down',
            'key_8_down',
            'data'
            ], lambda e: None
        )

    def handler_for(self, event):
        def gethandler(f):
            self.handlers[event] = f
            return f
        return gethandler

    def read_event(self):
        type = self.ser.read()
        data = []
        c = self.ser.read()
        while c != '\x0D':
            data.append(ord(c))
            c = self.ser.read()
        result = SpaceBallEvent.create(type, data)
        return result

    def update(self):
        e = self.read_event()
        e.run(self.handlers)

    def register_handler(self, regex, handler):
        pass



            