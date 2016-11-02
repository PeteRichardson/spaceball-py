from spaceball import SpaceBall

ball = SpaceBall()

@ball.handler_for('1_button_up')
@ball.handler_for('5_button_up')
@ball.handler_for('data')
def dump_event(event):
	print event

while True:
    ball.update()