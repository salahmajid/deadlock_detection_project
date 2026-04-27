**Salah Abdelmajid \- CPSC 35000 \- April 2026**  
	The program is going to simulate a group of processes that compete for shared resources. Each process holds some resources and may need to wait on others that are already taken. As the simulation runs, the program will watch for situations where processes are stuck waiting on each other, which is a deadlock. When the deadlock happens, the program will report which processes are involved. The detection will work by building a wait-for graph and running depth-first search through that graph to look for a cycle. If a cycle is found, then those processes are deadlocked. 

**Components:**

* **Process state-** The state of all processes is going to be tracked using two dictionaries. The holds and waiting dictionary. The holds maps each process ID to the list of the resources it currently holds and the waiting maps each process ID to the resource it is waiting for, or none if it is not blocked.   
* **Resource ownership tracking \-** Will keep track of which process owns each resource in the system. Stored as a python dictionary called owner that maps each resource ID to the process ID holding it, or none if the resource is free.   
* **Simulation driver \-** Steps the simulation by calling request and release functions in a specific order for each test scenario. After actions that could cause a deadlock, the driver will call the deadlock check so that any deadlock is caught the moment it forms.   
* **Wait-for graph builder \-** This will look at the current state of the program and produce a wait-for graph. The graph is going to be stored as a python dictionary where each key is a process ID and the value is a list of process IDs it is waiting on.   
* **Cycle detector \-** Runs depth-first search through the wait-for graph to find a cycle. The depth-first search will keep a list called path that tracks the processes currently on the search trail. If the search reaches a process that is already on the path, that means a cycle exists, and the detector returns the list of processes involved.   
* **Reporter \-** Prints what is happening at each step of the simulation. For every action it shows whether the process got the resource or got blocked, and if a deadlock is detected, it prints the cycle of processes involved.

**Data Flow:**   
	The simulation driver would be the top-level controller. On each step it tells the resource manager to apply a process action. The resource manager will update which processes holds which resource and which process is waiting for what. The wait-for graph builder will then read the state and produce a fresh graph. The cycle detector takes the graph and runs the depth-first search. The result will go to the reporter and then print it. 

**Test Scenarios:**  
	The program will run six built-in scenarios that exercise different cases: 

* A clean run with no deadlock (To confirm no false positives)  
* A two-process deadlock where each process holds one resource and waits for the other  
* A three-process circular wait  
* A single-process edge case  
* A ten-process cycle (To test scaling)  
* A twenty-process cycle (To compare detection times at a much larger scale)

**Analysis Tools:**

* **Python Debugger \-** Used to set breakpoints inside the cycle detector. Step through the depth-first search one line at a time and inspect the wait-for graph as the algorithm runs. Shows an internal view of how the detection actually works.  
* **Strace \-** Used to record the system calls the operating system makes while the program runs. This gives an external view of the program from the OS perspective and shows what resources the Python interpreter itself uses. 