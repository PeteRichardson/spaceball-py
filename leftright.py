from spaceball import SpaceBall
import sys
import subprocess 

class Line(object):
    ''' An object that can scale the ball x value
        to the width of the screen.
    '''
    def __init__(self, width=80):
        self.width = width
        self.x = width/2
        self.scale = 12
        self.maxmove = self.width/15

    def update(self, move):
        if move != 0:
            move = move/self.scale
            if abs(move) > self.maxmove:
                oldmove = move
                move = self.maxmove * abs(move)/move
            self.x = (self.x + move)
            if self.x > self.width:
                self.x = self.width
            elif self.x < 0:
                self.x = 0

    def __str__(self):
        '''Print some spaces and then a character.'''
        return " "*int(self.x) + "🏄‍♂️"


if __name__ == "__main__":
    # Get the screen size and instantiate the Line
    rows, columns = subprocess.check_output(['stty', 'size']).decode().split()
    line = Line(width=int(columns)-1)

    ball = SpaceBall(tty='/dev/tty.usbserial-AJ03ACPV')

    # Register a handler to update the Line whenever displacement data comes in.
    @ball.handler_for('data')
    def dump_event(event):
        line.update(event.Tx)

    # print the Line after each update
    while True:
        ball.update()
        print (line)


