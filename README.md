# PyC2

A modular command-and-control (C2) framework written in Python, built for authorised red-team operations, security research, and education.

> **Authorised use only.** This software is intended solely for use in environments you own or have explicit, written permission to test. Unauthorised access to computer systems is illegal under the UK Computer Misuse Act 1990, the US CFAA, and equivalent legislation worldwide. The authors accept no liability for misuse. See [Legal & Ethics](#legal--ethics).

---

## Overview

Python C2 provides the core components of a modern C2 framework: a central server, pluggable listeners, lightweight agents, and an operator interface. It is designed as a learning and research platform — readable code over obfuscation, clear interfaces over monolithic design.

**Goals**

- Demonstrate C2 architecture and tradecraft concepts in a transparent, auditable codebase.
- Provide a sandbox for studying detection (the defensive counterpart) and network forensics.
- Serve as a collaborative project with clean module boundaries for parallel development.

---

## Features

---

## Architecture

The project follows a simple client-server architecture. The server listens for incoming TCP connections, while the agent/client connects back to the server and sends basic system or session information.

## Architecture

The project follows a simple client-server architecture. The server listens for incoming TCP connections, while the agent/client connects back to the server and sends basic system or session information.

```text
+-------------------+        TCP        +-------------------+
|                   |  connect() -----> |                   |
|  netcatClient.py  |                   |     server.py     |
|                   |  send/recv <----> |                   |
+-------------------+                   +-------------------+

+-------------------+        TCP        +-------------------+
|                   |  connect() -----> |                   |
|     agent.py      |                   |     server.py     |
|                   |  send/recv <----> |                   |
+-------------------+                   +-------------------+

+-------------------+
|     crypto.py     |
| Shared helper     |
| functions         |
+-------------------+
```
---

## Tech stack

- TBD

---

## Prerequisites

- Linux
- Python 3.11 or later
- An isolated lab network (VMs or containers) — **do not run on networks you do not control**
---

## Usage


---

## Project structure

C2-SERVER/
└── pyc2/
    ├── agent.py
    ├── crypto.py
    ├── netcatClient.py
    └── server.py

---

## File Overview

| File | Purpose |
|---|---|
| `agent.py` | Handles the client/agent functionality and communication with the server. |
| `crypto.py` | Contains encryption, decryption, or hashing-related helper functions. |
| `netcatClient.py` | Provides a simple client used for testing socket connections. |
| `server.py` | Starts the server socket, listens for incoming clients, and manages connections. |

## Roadmap

- [ ] Deployment Of Agent Logic
- [X] Development of NetCat Client
- [X] Development of Server 
- [ ] Encryption of Traffic

---

## Contributing

This is a collaborative project between Max Bleakley & Ben Robinson.

---

## Legal and Ethical Use

This project is intended strictly for educational and research purposes within an authorised cyber security lab environment.

The code in this repository must only be used on systems, networks, and devices where explicit permission has been granted. Using this software against third-party systems without authorisation may be illegal and unethical.

This project must not be used for:

- unauthorised access to systems or networks
- persistence, evasion, credential theft, or data exfiltration
- deploying malware or backdoors
- attacking public IP addresses, organisations, or individuals
- bypassing security controls without written permission

Acceptable use includes:

- controlled lab testing
- university coursework
- defensive security research
- learning about TCP sockets, client-server communication, and secure coding
- testing inside isolated virtual machines or private networks

The author/s does not condone malicious use of this software. Users are responsible for ensuring that their actions comply with all applicable laws, university policies, and ethical guidelines.