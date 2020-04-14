import socket  # send messages across a network
import threading
import os
from grid import Grid
import pygame

# basically sets the screen relative to your user environment
os.environ['SDL_VIDEO_WINDOW_POS'] = '400,100'

surface = pygame.display.set_mode((600, 600))  # dimensions of screen
pygame.display.set_caption('Tic-Tac-Toe')


def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


HOST = '127.0.0.1'  # standard interface adress
PORT = 65432  # port to listen on

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


def receive_data():
    global turn
    while True:
        data = sock.recv(1024).decode()  # length of a byte
        # creates a list that will be seen in CMD, splits the cellx,celly,your turn data
        data = data.split('-')
        x, y = int(data[0]), int(data[1])
        if data[2] == 'your turn':
            turn = True
        if data[3] == 'False':
            grid.game_over = True
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, 'X')
        print(data)


create_thread(receive_data)

grid = Grid()  # for the lines from the grid module


running = True
player = 'O'
turn = False  # server will go first
playing = 'True'

while running:  # we set it as TRUE
    for event in pygame.event.get():  # events basically read the keystrokes and do an action based on them
        if event.type == pygame.QUIT:  # disables the module
            running = False  # ends while loop

        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:  # basically reads the user clicks
            # will only execute if game over is True
            # this returns a tuple, so when i click with my left mouse, itll give me (1,0,0)
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.game_over:
                    # this stores the position of the click in a tuple (200,343)
                    pos = pygame.mouse.get_pos()
                    # this standardizes the cells, so if i click on the first cell, itll print out 0,0
                    cellX, cellY = pos[0]//200, pos[1]//200
                    grid.get_mouse(cellX, cellY, player)
                    if grid.game_over:
                        playing = 'False'
                    send_data = '{}-{}-{}-{}'.format(cellX,
                                                     cellY, 'your turn', playing).encode()
                    sock.send(send_data)
                    turn = False
                # if grid.switch_player:  # will only switch player if another grid is clicked on
                #     if player == 'X':
                #         player = 'O'
                #     elif player == 'O':
                #         player = 'X'
                #     grid.print_grid()  # for the array printed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:  # press space to clear game or if game over
                grid.clear_grid()
                grid.game_over = False
                playing == 'True'
            elif event.key == pygame.K_ESCAPE:
                running = False  # break out of this loop, game is over

    surface.fill((0, 0, 0))  # fill with black color
    grid.draw(surface)
    pygame.display.flip()
