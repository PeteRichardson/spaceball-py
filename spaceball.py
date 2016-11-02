import serial
import re

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


ball = SpaceBall()
while True:
    c = ball.read()
    if c in ['K','D', '\x0D']:
    	print c,
    else:
        #brep = replchars.sub(replchars_to_hex, c)
        brep = "{:02x}".format(ord(c))
        #brep = "{:08b}".format(ord(c))
        print brep,
    if c == "\x0D":
        print
            