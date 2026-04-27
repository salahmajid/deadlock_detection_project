**Status Report \- Deadlock Detection**

This project simulates a group of processes that compete for shared resources and detects when they get stuck in a deadlock. The simulator is written in Python. It tracks which processes hold which resources, builds a wait-for graph from the current state, and runs depth-first search through that graph to look for a cycle. A cycle in the graph means those processes are deadlocked, and the program reports which ones.

**Completed:** 

* Software design document   
* Python simulator and detection algorithm completed  
* Six test scenarios coded into the program  
* Initial run with timing data captured for each scenario  
* Input validation added so bad test inputs give clean errors  
* GitHub repo set up for version control, organization, and if I have to work remote - https://github.com/salahmajid/deadlock_detection_project

**What I have left:** 

* Capture pdb session walking through the cycle detection  
* Capture strace output of a test run  
* Formal test case document in the pass/fail table format  
* Flowchart of the detection algorithm (the model deliverable)  
* Research paper  
* Presentation slides

**Status:** I’m doing well\! I should be on track to finish by the deadline. The code works on all six scenarios. What is left is documentation, capturing the analysis tool outputs, and the writeup.

