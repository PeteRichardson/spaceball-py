import serial
import re

def config_ball(ser):
    """
    \015            # Clear the line
    CB\015          # Communications Mode Set to Binary
    NT\015FT?\015FR?\015    # Set Null Region and Trans and Rot Sensitivity
    P@r@r\015       # Data rate to 20 events per Second
    MSSV\015        # Ball Event Type: Trans and Rot Vectors
    Z\015           # Rezero the ball
    BcCc\015        # Beep it
    """
    ser.write("\015")
    ser.write("CB\015")
    ser.write("NT\015FT?\015FR?\015")
    ser.write("P@r@r\015")
    ser.write("MSSV\015")
    ser.write("Z\015")
    ser.write("BcCc\015")
    ser.write("H")

replchars = re.compile('([^ -~])')
def replchars_to_hex(match):
    return r'\x{0:02x}'.format(ord(match.group()))


with serial.Serial(timeout=None) as ser:
    #ser.baudrate = 9600
    ser.port = '/dev/cu.usbserial-A403JWZ2'
    ser.open()
    ser.reset_input_buffer()
    config_ball(ser)
    while True:
        c = ser.read()
        #brep = replchars.sub(replchars_to_hex, c)
        #brep = "{:02x}".format(ord(c))
        brep = "{:08b}".format(ord(c))
        print brep,
        if c == "\x00":
            print
            