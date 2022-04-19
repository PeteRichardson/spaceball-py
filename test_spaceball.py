from spaceball import SpaceBall

# Pass in the serial port the Spaceball is connected to
ball = SpaceBall(tty='/dev/tty.usbserial-AJ03ACPV')

# Register a simple handler for all the keydown events
# and the data (i.e. displacement) event.
# The handler just prints a text representation of
# each event.
@ball.handler_for('key_pick_down')
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
    print(event)

# Start the loop and event handlers
while True:
    ball.update()


# EXAMPLE OUTPUT -----------------------------
# This script should print output similar to this
# (without the # starting each line)
#
# The D lines show ball displacement, including
# 3-axis translation data and 3-axis rotation data.
# The second value (right after the D) is the "period"
# which tells how long it has been in ms since the last
# translation data was sent.
#
# The K lines show one or more keypresses.
# There are 8 keys number 1-8 and the "Pick" key on the ball.
#
# $ python3 test_spaceball.py
# D,81.500, T(     0,     0,     0) R(     0,     0,     0)
# K,_____5___
# K,______6__
# K,_______7_
# K,________8
# K,__2______
# D,61.875, T(     0,     0,     0) R(     2,   -10,     0)
# D,51.125, T(     0,     0,     0) R(     4,   -15,     1)
# D,72.750, T(     0,     0,     0) R(     1,    -3,     0)
# D,57.750, T(     0,     0,     0) R(     0,     0,     0)
# D,62.000, T(     0,     0,     0) R(     1,     9,    -1)
# D,62.125, T(     0,     0,     0) R(     2,    39,     0)
# D,61.750, T(    -1,    -1,    -4) R(     0,    82,    -1)
# D,61.750, T(    -1,     0,    -4) R(    -1,    28,     1)
# D,61.750, T(     0,     0,     0) R(     0,     0,     0)
# K,__2______
# K,_______7_
# K,_______7_
# D,62.125, T(    -1,    -2,    -5) R(     0,     0,     0)
# D,62.000, T(    -2,    -3,    -6) R(     0,     0,     0)
# K,P________
# D,61.500, T(    -2,    -4,    -6) R(     0,     0,     0)
# D,61.750, T(    -1,    -4,    -4) R(     0,     0,     0)
# D,61.875, T(     0,     0,     0) R(     0,     0,     0)