import socket
import threading
import pygame
import time
import sys
from pygame.locals import *


class Player(object):
    """Object to handle each player's paddle"""
    def __init__(self, player):
        
        # Define size of paddle
        self.height = 200
        self.width = 20

        # Set player's position on screen
        if player == 1:
            self.rect = Rect(20, 400-(self.height/2), self.width, self.height)
            self.player = 1
        elif player == 2:
            self.rect = Rect(800-20-self.width, 400-(self.height/2), self.width, self.height)
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
    """Object to draw and move ball"""
    def __init__(self):
        self.rect = pygame.rect.Rect(400-8, 400-8, 15, 15)

    def draw(self):
        global screen
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
    
    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y



class dataThread(threading.Thread):
    """Thread to send and receive data from server
       Also updates objects' positions
    """
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):

        # Initialise socket
        host = sys.argv[1]
        port = int(sys.argv[2])
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        csock.sendto("start".encode(), (host, port))

        global running
        global ball

        data = csock.recv(2048).decode()
        
        time.sleep(1)



        global player
        global enemy
        player.__init__(int(data)) # Reinitialise player to place on correct side
        # Reinitialise enemy to place on correct side
        if int(data) == 1:
            enemy.__init__(2)
        else:
            enemy.__init__(1)
            
        data = csock.recv(2048)
        csock.settimeout(4)
        while running:
            """Main loop to get data from server and send"""
            
            # Get data
            data = csock.recv(2048)

            if data:

                try:
                    data = data.decode()

                    coords = data.split("x")

                    ball.rect.x = int(coords[0]) - 100
                    ball.rect.y = int(coords[1]) - 100

                    enemy.rect.x = int(coords[2])
                    enemy.rect.y = int(coords[3])

                except:

                    print("Packet choke")
                


                # Send data
                try:
                    if player.player == 1:
                        data = "a"
                    else:
                        data = "b"
                    data += str(player.rect.x) + "x" + str(player.rect.y)
                    csock.sendto(data.encode(), (host, port))
                
                except:
                    print("Data could not be sent")

            else:
                running = False
                break # Exit loop 

        csock.close()


       
### Initialisation ###
pygame.init()
screen = pygame.display.set_mode((800, 800))

running = True
ball = Ball()
player = Player(1)
enemy = Player(2)

########################################################################
background = pygame.surface.Surface((800, 800))                        #
pygame.draw.rect(background, (255, 255, 255), Rect(0,0,800,4))         #
pygame.draw.rect(background, (255, 255, 255), Rect(0,800-4,800,4))     # Draw background
pygame.draw.rect(background, (255, 255, 255), Rect(0,0,4,800))         #
pygame.draw.rect(background, (255, 255, 255), Rect(800-4,0,400,800))   #
pygame.draw.rect(background, (255, 255, 255), Rect(400-2,0,4,800))     #
########################################################################

# Start data thread
dthread = dataThread()
dthread.start()



# Rendering loop
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

    # Draw elements on screen
    screen.blit(background, (0, 0))
    ball.draw()
    player.draw()
    enemy.draw()

    # Update screen & render 60FPS
    pygame.display.flip()
    clock.tick(60)

# Wait for data thread to end
dthread.join()
