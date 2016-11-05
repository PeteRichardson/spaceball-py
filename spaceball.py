import serial
import re

class SpaceBallEvent:
    def __init__(self, type, data):
        self.type = type
        self.data = data

    @classmethod
    def create(cls, type, data):
        if type == 'K':
            return SpaceBallButtonEvent(data)
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

class SpaceBallButtonEvent (SpaceBallEvent):
    last_button_data = [0x40, 0x40]

    def __init__(self, data):
        SpaceBallEvent.__init__(self, 'K', data)

    def __str__(self):
        print "Button Event! prev data = 0x{:02x} 0x{:02x}...".format(SpaceBallButtonEvent.last_button_data[0], SpaceBallButtonEvent.last_button_data[1]),
        return SpaceBallEvent.__str__(self)

    def run(self, handlers):
        if self.data[0] & 0x1F:    # check pick button and buttons 5-8
            if (self.data[0] & 0x10 and not (SpaceBallButtonEvent.last_button_data[0] & 0x10)):
                handlers["pick_button_up"](self)
            if (self.data[0] & 0x01 and not (SpaceBallButtonEvent.last_button_data[0] & 0x01)):
                handlers["5_button_up"](self)
            if (self.data[0] & 0x02):
                handlers["6_button_up"](self)
            if (self.data[0] & 0x04):
                handlers["7_button_up"](self)
            if (self.data[0] & 0x08):
                handlers["8_button_up"](self)

        if self.data[1] & 0x0F:    # check buttons 1-4
            if (self.data[1] & 0x01):
                handlers["1_button_up"](self)
            if (self.data[1] & 0x02):
                handlers["2_button_up"](self)
            if (self.data[1] & 0x04):
                handlers["3_button_up"](self)
            if (self.data[1] & 0x08):
                handlers["4_button_up"](self)

        last_button_data = self.data

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
            'pick_button_up',
            '1_button_up',
            '2_button_up',
            '3_button_up',
            '4_button_up',
            '5_button_up',
            '6_button_up',
            '7_button_up',
            '8_button_up',
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



            