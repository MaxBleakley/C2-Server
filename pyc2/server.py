import socket # Socket needed for networking in python
import subprocess # System commands needed for python
import sys # Python runtime
import time # Timers etc
import threading # Runs multiple tasks
import asyncio # Many network tasks
import io # Memory text streams
import os # Interacts with OS
import psutil # System utility information
import colorama # Coloured terminal output
from colorama import Fore, Back, Style 
exit_event = threading.Event()

counter=-1
clientlist=[]
clientdata=[]
automigrate=""

host = "0.0.0.0"
port = 4545

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # This defines an IPV4 and TCP Socket/Endpoint
s.bind((host, port)) # This binds the socket to host and port 
s.listen(5) # Sets socket to listen. 5 connections can wait in queue before being accepted
print(Fore.GREEN + "[+] Listening on " + host + ":" + str(port) + Style.RESET_ALL) # Prints a line saying port and ip address the server is listening on


# This block of code starts the threads to keep the main programme alive 

# threading.Thread(...) Creates a new thread
# target=init_main_sock tells the thread which function to run
# daemon = True makes the programme run as background thread 
# start() Actually begins the thread 

# The line below also calls a variable (handler_thread) which is equal too threading.Thread(...) so that the thread can be referenced
handler_thread = threading.Thread(target=init_main_sock) # creates and starts threat to run the init_main_sock function
handler_thread.daemon = True
handler_thread.start()

while True:
    time.sleep(1)

