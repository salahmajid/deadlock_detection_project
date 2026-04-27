"""
Deadlock Detection Simulator
Salah Abdelmajid - CPSC 35000 - April 2026
"""
 
import time
 
 
# ---------- State ----------
# I'm using three dictionaries to track everything because dictionary lookups
# are O(1), which keeps the simulation fast even when scaling up to 20+ processes.
#
# held_by_process[pid]      = list of resources held by that process
# blocked_on[pid]           = resource that process is blocked on, or None
# resource_holder[resource] = pid that holds it, or None if free
 
held_by_process = {}
blocked_on = {}
resource_holder = {}
 
 
def setup(num_processes, num_resources):
    """Initialize state for a fresh scenario."""
    # global is needed here because each test scenario resets these dictionaries,
    # and without global the assignments would create new local variables instead
    global held_by_process, blocked_on, resource_holder
    held_by_process = {p: [] for p in range(1, num_processes + 1)}
    blocked_on = {p: None for p in range(1, num_processes + 1)}
    resource_holder = {r: None for r in range(1, num_resources + 1)}
 
 
def request(pid, resource):
    """Process pid asks for a resource."""
    # Validate inputs first so a typo in a test scenario gives a clear error
    # instead of a confusing KeyError deep in the code
    if pid not in held_by_process:
        print(f"  ERROR: P{pid} does not exist in this scenario")
        return
    if resource not in resource_holder:
        print(f"  ERROR: R{resource} does not exist in this scenario")
        return
 
    if resource_holder[resource] is None:
        # Resource is free, so the process gets it immediately
        resource_holder[resource] = pid
        held_by_process[pid].append(resource)
        blocked_on[pid] = None
        print(f"  P{pid} got R{resource}")
    else:
        # Resource is taken, so the process has to wait. We record what it's
        # waiting for so the wait-for graph builder can use that information later
        blocked_on[pid] = resource
        print(f"  P{pid} blocked, waiting for R{resource}")
 
 
def release(pid, resource):
    """Process pid releases a resource."""
    # Validate so a bug in the test scenario fails loudly instead of silently
    if pid not in held_by_process:
        print(f"  ERROR: P{pid} does not exist in this scenario")
        return
    if resource not in held_by_process[pid]:
        print(f"  ERROR: P{pid} cannot release R{resource} (it is not holding it)")
        return
 
    held_by_process[pid].remove(resource)
    resource_holder[resource] = None
    print(f"  P{pid} released R{resource}")
 
 
def build_graph():
    """Build the wait-for graph showing which processes are blocked by which"""
    # An adjacency list (dictionary mapping each process to its neighbors) is
    # the natural fit here because most processes will only wait on one other,
    # so a full matrix would waste memory
    graph = {p: [] for p in held_by_process}
    for p, r in blocked_on.items():
        if r is not None and resource_holder[r] is not None:
            # Process p is waiting for resource r, which is held by resource_holder[r],
            # so we add an edge from p to whoever holds the resource
            graph[p].append(resource_holder[r])
    return graph
 
 
def find_cycle(graph):
    """DFS through the graph. Return list of processes in a cycle, or None."""
    # I use two structures here:
    # - visited: every node we've already finished exploring (so we don't redo work)
    # - path: the current DFS trail. If we hit a node already on the path, that's a cycle
    visited = set()
    path = []
 
    def dfs(node):
        if node in path:
            # Found a cycle. Slice the path from where the cycle starts to here,
            # then add the start node again at the end so the cycle reads as a loop
            i = path.index(node)
            return path[i:] + [node]
        if node in visited:
            return None
        visited.add(node)
        path.append(node)
        for neighbor in graph[node]:
            result = dfs(neighbor)
            if result:
                return result
        # If no cycle found through this node, remove it from the current path
        # before backing up so it doesn't pollute searches from other start nodes
        path.pop()
        return None
 
    # Try starting DFS from every node in case the graph has multiple disconnected pieces
    for node in graph:
        if node not in visited:
            result = dfs(node)
            if result:
                return result
    return None
 
 
def check_for_deadlock():
    """Build the graph, check for a cycle, and time how long detection took."""
    # I time only the detection part (graph building + DFS), not the full
    # simulation, since the proposal calls for analyzing how the algorithm scales
    start = time.perf_counter()
    graph = build_graph()
    cycle = find_cycle(graph)
    elapsed_ms = (time.perf_counter() - start) * 1000
 
    if cycle:
        cycle_str = " -> ".join(f"P{p}" for p in cycle)
        print(f"  *** DEADLOCK: {cycle_str} ***")
        print(f"  Detection took {elapsed_ms:.4f} ms")
        return True
    print(f"  Detection took {elapsed_ms:.4f} ms")
    return False
 
 
# ---------- Test scenarios ----------
 
def test_no_deadlock():
    print("\n--- Test 1: No deadlock ---")
    setup(2, 2)
    request(1, 1)
    request(1, 2)
    release(1, 1)
    release(1, 2)
    request(2, 1)
    if not check_for_deadlock():
        print("  No deadlock found (correct)")
 
 
def test_two_process_deadlock():
    print("\n--- Test 2: Two-process deadlock ---")
    setup(2, 2)
    request(1, 1)
    request(2, 2)
    request(1, 2)   # P1 blocked
    request(2, 1)   # P2 blocked, deadlock
    check_for_deadlock()
 
 
def test_three_process_cycle():
    print("\n--- Test 3: Three-process cycle ---")
    setup(3, 3)
    request(1, 1)
    request(2, 2)
    request(3, 3)
    request(1, 2)
    request(2, 3)
    request(3, 1)
    check_for_deadlock()
 
 
def test_single_process():
    print("\n--- Test 4: Single process ---")
    setup(1, 2)
    request(1, 1)
    request(1, 2)
    if not check_for_deadlock():
        print("  No deadlock found (correct)")
 
 
def test_scaling(n):
    print(f"\n--- Test: {n}-process cycle ---")
    setup(n, n)
    # First, every process grabs its own resource so nothing is blocked yet
    for p in range(1, n + 1):
        request(p, p)
    # Then every process requests the next process's resource. The (p % n) + 1
    # math makes the last process wrap around to request resource 1, closing the cycle
    for p in range(1, n + 1):
        next_resource = (p % n) + 1
        request(p, next_resource)
    check_for_deadlock()
 
 
if __name__ == "__main__":
    test_no_deadlock()
    test_two_process_deadlock()
    test_three_process_cycle()
    test_single_process()
    test_scaling(10)
    test_scaling(20)
 