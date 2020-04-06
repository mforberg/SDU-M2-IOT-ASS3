import network
import time
import socket
import ssl
import uselect as select
import machine
import gc


def create_socket():
    s= socket.socket()
    s.setblocking(True)
    
    try:
        # localhost
        #s.connect(('192.168.1.128', 5000))
        # amazon EC2
        s.connect(('18.184.213.158', 5000))

    except OSError as e:
        if str(e) == '[Errno 119] EINPROGRESS': # For non-Blocking sockets 119 is EINPROGRESS
            print("In Progress")
        else:
            s.close()
            
            time.sleep(30) # stackoverflow happens if this recursive call happens too many times, stagger the connection attempts to increase chance of SUCCess
            #gc.collect() # might have to collect garbage to prevent OSError: 23
            create_socket()
    return s

def send(sock, data):
    d = bytes(str(data), "utf8")
    print(d)
    sock.send(d)