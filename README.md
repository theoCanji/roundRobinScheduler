# Round-Robin Scheduler Simulation

This project implements a **Round-Robin (RR) scheduling algorithm** with support for **process blocking** and **priority-based ready queue management**. The scheduler reads a list of processes from a file and simulates their execution using a configurable time slice and block duration.

---

## 🧠 Features

- Implements **Round-Robin CPU scheduling** with:
  - Process arrival handling
  - CPU bursts and blocking after a specified interval
  - Priority-based ready queue (higher priority = earlier scheduling)
  - Idle time tracking
- Calculates and displays the **average turnaround time**
- Logs detailed events during simulation: process start, block, preemption, and idle periods

---

## 📄 Input File Format

Each line in the process input file should follow this format:
<name> <priority> <arrival_time> <total_time> <block_interval>


- `name`: String ID for the process (e.g., `P1`)
- `priority`: Integer (higher = more priority)
- `arrival_time`: Integer, time at which process enters the system
- `total_time`: Integer, total CPU time needed
- `block_interval`: Integer, how frequently a process blocks

Lines starting with `#` are treated as comments.


---

## 🚀 How to Run

Ensure you're using Python 3.

### Command Line

```bash
python3 roundrobin.py <process_file.txt> <time_slice> <block_duration>
```
### Example
python3 roundrobin.py processes.txt 10 20

This runs the simulation using:

- processes.txt as input
- a time slice of 10 units
- a block duration of 20 units

## 🧾 Output Format

Each event printed has the form:
<current_time> <process_name or (IDLE)> <duration> <token>

Where:
- `T` = Terminated
- `B` = Blocked
- `P` = Preempted
- `I` = Idle






