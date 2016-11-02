import serial
import re

class SpaceBallDataEvent:
    def __init__(self, type, data):
        self.type = type
        self.data = data

    def __str__(self):
        result = ""
        if self.type in ['K','D']:
            result += self.type
        else:
            result += "{:02x}".format(ord(self.type))
            #brep = "{:08b}".format(ord(c))
        for c in self.data:
            result += " {:02x}".format(ord(c))
        return result

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
            "BcCc\x0D",             # Beep it
            "H"
        ]
        for msg in config_data:
            self.ser.write(msg)

    def read(self):
        return self.ser.read()

    def read_event(self):
        type = self.read()
        data = []
        c = self.read()
        while c != '\x0D':
            data.append(c)
            c = self.read()
        result = SpaceBallDataEvent(type, data)
        return result




            