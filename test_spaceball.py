from spaceball import SpaceBall

ball = SpaceBall()

@ball.handler_for('1_button_up')
@ball.handler_for('2_button_up')
@ball.handler_for('3_button_up')
@ball.handler_for('4_button_up')
@ball.handler_for('5_button_up')
@ball.handler_for('6_button_up')
@ball.handler_for('7_button_up')
@ball.handler_for('8_button_up')
@ball.handler_for('pick_button_up')
@ball.handler_for('data')
def dump_event(event):
	print event

while True:
    ball.update()