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

```
+-----------+        HTTPS         +-------------+        IPC/API        +------------+
|  Agent    | <------------------> |   Server    | <-------------------> |  Operator  |
| (target)  |   check-in/tasking   | (listeners, |   tasking/results     |    CLI     |
+-----------+                      |  task queue,|                       +------------+
                                   |  data store)|
                                   +-------------+
```

**Server** — Accepts agent connections via one or more listeners, queues operator-issued tasks, stores results.

**Listeners** — Transport adapters (HTTP/S to start). Decoupled from core logic so new transports can be added without touching the server.

**Agent** — Minimal client that checks in, retrieves tasks, returns results. Kept deliberately simple.

**Operator interface** — CLI for managing sessions and issuing tasks.

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

---

## Roadmap

- [ ] 
- [ ] 

---

## Contributing

This is a collaborative project between Max Bleakley & Ben Robinson.

---

## Legal & Ethics
