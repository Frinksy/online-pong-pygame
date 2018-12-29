# Online Pong
> Simple online pong game made with pygame  
> Server hosts the game, two clients play, connecting to the server


## Usage
### UDP Version
> Server : python server_udp.py [host] [port]
> Clients : pytho server_udp.py [host] [port]  
> Host and port should match the ones used to start server  
> Using UDP should be preferred, as it should be less laggy across laggy connections  
### TCP Version (old)
> You can always use the old tcp version of the game :  
> Server : python server.py [host] [port]  
> Clients : python client.py [host] [port]  

## Requirements
> Python 3 or above (tested on Python 3.7.1)  
> Pygame module  
> For use over the internet, the machine the server runs on will have to have port-forwarding enabled