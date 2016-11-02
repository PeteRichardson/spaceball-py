from spaceball import SpaceBall

ball = SpaceBall()

def handle_1_button(event):
	print ("1 button pushed!")

def dump_data(event):
	print event

ball.handlers['data'] = dump_data
ball.handlers['1_button_up'] = handle_1_button

while True:
    ball.update()