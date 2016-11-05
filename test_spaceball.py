from spaceball import SpaceBall

ball = SpaceBall()

@ball.handler_for('key_1_down')
@ball.handler_for('key_2_down')
@ball.handler_for('key_3_down')
@ball.handler_for('key_4_down')
@ball.handler_for('key_5_down')
@ball.handler_for('key_6_down')
@ball.handler_for('key_7_down')
@ball.handler_for('key_8_down')
@ball.handler_for('data')
def dump_event(event):
	print event

while True:
    ball.update()