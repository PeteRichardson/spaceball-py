from spaceball import SpaceBall

ball = SpaceBall()

def handler_for(event):
	def gethandler(f):
		ball.handlers[event] = f
		return f
	return gethandler

@handler_for('1_button_up')
@handler_for('5_button_up')
def handle_button(event):
	print ("Button pushed!")

@handler_for('data')
def dump_data(event):
	print event

while True:
    ball.update()