# Deadlock Detection Simulator

Python deadlock detection simulator using a wait-for graph and DFS-based cycle detection. Final project for CPSC 35000 (Operating Systems).

## What it does

Simulates a group of processes that compete for shared resources and detects when they get stuck in a deadlock. The program tracks which processes hold which resources, builds a wait-for graph from the current state, and runs depth-first search through that graph to find a cycle. A cycle in the graph means those processes are deadlocked, and the program reports which ones.


## Test scenarios

The program runs six built-in scenarios:

1. No deadlock — confirms no false positives
2. Two-process deadlock
3. Three-process circular wait
4. Single-process edge case
5. Ten-process cycle (scaling test)
6. Twenty-process cycle (scaling test)


## Author

Salah Abdelmajid — CPSC 35000 — April 2026