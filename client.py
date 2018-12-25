import socket
import threading
import pygame
import time
from pygame.locals import *


class Player(object):

    def __init__(self, player):
        
        self.height = 200
        self.width = 20
        if player == 1:
            self.rect = Rect(20, 400-self.height/2, self.width, self.height)
            self.player = 1
        elif player == 2:
            self.rect = Rect(800-20-self.width, 400-self.height/2, self.width, self.height)
            self.player = 2
    
    def draw(self):
        global screen
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

    def move(self):
        k = pygame.key.get_pressed()
        if k[K_UP] and self.rect.y > 9:
            self.rect.move_ip(0, -9)
        if k[K_DOWN] and self.rect.y < 800-self.height-9:
            self.rect.move_ip(0, 9)

class Ball(object):

    def __init__(self):
        self.rect = pygame.rect.Rect(0, 0, 15, 15)

    def draw(self):

        global screen

        pygame.draw.rect(screen, (255, 255, 255), self.rect)
    
    def move(self, x, y):

        self.rect.x = x
        self.rect.y = y



class dataThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):

        host = '127.0.0.1'
        port = 53355
        csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        csock.connect((host, port))

        global running
        global ball

        data = csock.recv(2048).decode()
        
        time.sleep(1)
        global player
        global enemy
        player.__init__(int(data))
        if int(data) == 1:
            enemy.__init__(2)
        else:
            enemy.__init__(1)
            

        while running:

            data = csock.recv(2048)

            if data:
                #print(repr(data))
                #print(running)

                try:
                    data = data.decode()

                    coords = data.split("x")

                    ball.rect.x = int(coords[0]) - 100
                    ball.rect.y = int(coords[1]) - 100

                    enemy.rect.x = int(coords[2])
                    enemy.rect.y = int(coords[3])

                except:

                    print("Packet choke")
                
                try:
                    data = str(player.rect.x) + "x" + str(player.rect.y)
                    csock.send(data.encode())
                
                except:
                    print("Data could not be sent")

            else:
                break

        csock.close()


       
### Initialisation ###
pygame.init()
screen = pygame.display.set_mode((800, 800))

running = True
ball = Ball()
player = Player(1)
enemy = Player(2)

######################

dthread = dataThread()
dthread.start()

clock = pygame.time.Clock()
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    
    k = pygame.key.get_pressed()
    if k[K_ESCAPE]:
        running = False
        break

    player.move()


    screen.fill((0,0,0))
    ball.draw()
    player.draw()


    enemy.draw()

    pygame.display.flip()
    
    clock.tick(60)





dthread.join()

