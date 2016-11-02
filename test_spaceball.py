from spaceball import SpaceBall

ball = SpaceBall()
while True:
    c = ball.read()
    if c in ['K','D', '\x0D']:
    	print c,
    else:
        brep = "{:02x}".format(ord(c))
        #brep = "{:08b}".format(ord(c))
        print brep,
    if c == "\x0D":
        print