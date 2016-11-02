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
    def __init__(self, data):
        SpaceBallEvent.__init__(self, 'K', data)

    def __str__(self):
        print "Key Event! ",
        return SpaceBallEvent.__str__(self)

    def run(self, handlers):
        if self.data[0] & 0x1F:    # check pick button and buttons 5-8
            if (self.data[0] & 0x10):
                handlers["pick_button_up"](self)
            if (self.data[0] & 0x01):
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
            if (self.data[0] & 0x04):
                handlers["3_button_up"](self)
            if (self.data[0] & 0x08):
                handlers["4_button_up"](self)


class SpaceBallDataEvent (SpaceBallEvent):
    def __init__(self, data):
        SpaceBallEvent.__init__(self, 'D', data)

    def __str__(self):
        print "Data Event! ",
        return SpaceBallEvent.__str__(self)

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



            