import socket
import threading
import time
import pygame
import sys
from random import choice


class Ball(object):

    def __init__(self):
        self.rect = pygame.rect.Rect(400-7, 400-7, 15, 15)
        self.x = 400
        self.y = 400
        self.velx = choice((3, -3))
        self.vely = choice((4, -4))
        self.size = 15

    def reset(self):
        self.__init__()
        time.sleep(2)

    def move(self):
        #self.x += self.velx
        #self.y += self.vely
        self.rect.move_ip(self.velx, self.vely)
        if self.rect.y > 800 - self.size:
            self.vely = -(abs(self.vely))
        elif self.rect.y < 0:
            self.vely = abs(self.vely)
        if self.rect.x > 800 - self.size:
            self.reset()
        elif self.rect.x < 0:
            self.reset()
        #   print(self.x,self.y)
        if abs(self.velx) < 40:
            self.velx *= 1.001
        global player1
        global player2

        if self.rect.colliderect(player1.rect):
            self.velx = abs(self.velx)
            self.vely = (self.rect.centery - player1.rect.centery) * 0.1 
        elif self.rect.colliderect(player2.rect):
            self.velx = -abs(self.velx)
            self.vely = (self.rect.centery - player2.rect.centery) * 0.1


class Player(object):

    def __init__(self, player):

        self.player = player
        
        if self.player == 1:
            x = 10
        elif self.player == 2:
            x = 800 - 10
        else:
            x = 400
            print("Player isn't 1 or 2")
        
        y = 400 - 30

        self.rect = pygame.rect.Rect(x, y, 20, 200)

class server_thread(threading.Thread):

    def __init__(self, sock, addr, p):
        threading.Thread.__init__(self)
        self.sock = sock
        self.host, self.port = addr
        self.p = p
        print("Connection on ", host, port)

    def run(self):
        global ball
        global running
        global player1
        global player2
        while running:
            try:
    
                data = str(ball.rect.x + 100) + "x" + str(ball.rect.y + 100)
                if self.p == 1:
                    data += "x" + str(player2.rect.x) + "x" + str(player2.rect.y)
                elif self.p == 2:
                    data += "x" + str(player1.rect.x) + "x" + str(player1.rect.y)
                self.sock.sendall(data.encode())
            except:
                print("The program has encountered an error : sending data")
                running = False

            try:
                data = self.sock.recv(2048).decode()
                coords = data.split("x")
                if self.p == 1:
                    player1.rect.x = int(coords[0])
                    player1.rect.y = int(coords[1])
                else:
                    player2.rect.x = int(coords[0])
                    player2.rect.y = int(coords[1])
                    

            except:
                print("The program has encountered an error : receiving data")

        self.sock.close()

class game_updater(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global running
        while running:
            time.sleep(1/60)
            global ball
            ball.move() 


### Game Data ###
player1 = Player(1)
player2 = Player(2)
ball = Ball()
running = True



###########################

# Initialize server
host = sys.argv[1]
port = int(sys.argv[2])


lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

lsock.bind((host, port))


lsock.listen(1)

ssock, addr = lsock.accept()
ssock.send("1".encode())
print("Player 1 connected")
sthread = server_thread(ssock, addr, 1)

lsock.listen(1)

ssock2, addr2 = lsock.accept()
ssock2.send("2".encode())
print("Player 2 connected")
sthread2 = server_thread(ssock2, addr2, 2) 
gthread = game_updater()

gthread.start()
sthread.start()
sthread2.start()
sthread.join()
sthread2.join()
gthread.join()
