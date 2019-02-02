''' chenb24_Astar.py by Chen Bai(chenb24, 1560405)
A* Search of a problem space extended from starter code USC.py
    Version 0.2, January 30, 2019.
    Chen Bai, Univ. of Washington.
    Electronic and Computer Engineering

 Usage:
 python3 chenb24_Astar.py chenb24_EightWithHamming 'YOUR_PUZZLE_ARRAY'
 python3 chenb24_Astar.py chenb24_EightWithManhattan 'YOUR_PUZZLE_ARRAY'

This implementation is extended from USC.py
to implement A*, and it is to work will all heuristics,
including non-admissible ones, then when a state is regenerated
that was already put on the CLOSED list, it may need reconsideration
if the new priority value is lower than the old one.

Most of the print statements have been commented out, but can be
useful for a closer look at execution, or if preparing some
debugging infrastructure before adding extensions.
'''

VERBOSE = False  # Set to True to see progress; but it slows the search.

import sys

if sys.argv == [''] or len(sys.argv) < 2:
    # import EightPuzzle as Problem
    # import FranceWithCosts as Problem
    import FranceWithDXHeuristic as Problem
    # import chenb24_EightPuzzleWithManhattan as Problem
    # import chenb24_Rubik2Cube as Problem
    h = Problem.h
else:
    import importlib

    Problem = importlib.import_module(sys.argv[1])
    h = Problem.h
print("\nWelcome to chenb24_AStar")

COUNT = None  # Number of nodes expanded.
MAX_OPEN_LENGTH = None  # How long OPEN ever gets.
SOLUTION_PATH = None  # List of states from initial to goal, along lowest-cost path.
TOTAL_COST = None  # Sum of edge costs along the lowest-cost path.
BACKLINKS = {}  # Predecessor links, used to recover the path.

# The value g(s) represents the cost along the best path found so far
# from the initial state to state s.
g = {}  # We will use a global hash table to associate g values with states.


class My_Priority_Queue:
    def __init__(self):
        self.q = []  # Actual data goes in a list.

    def __contains__(self, elt):
        '''If there is a (state, priority) pair on the list
        where state==elt, then return True.'''
        # print("In My_Priority_Queue.__contains__: elt= ", str(elt))
        for pair in self.q:
            if pair[0] == elt:
                return True
        return False

    def delete_min(self):
        ''' Standard priority-queue dequeuing method.'''
        if not self.q:
            return []  # Simpler than raising an exception.
        temp_min_pair = self.q[0]  # first pair
        temp_min_value = temp_min_pair[1]  # priority
        temp_min_position = 0  # pair position
        for j in range(1, len(self.q)):
            if self.q[j][1] < temp_min_value:  # compare priority with certain
                temp_min_pair = self.q[j]
                temp_min_value = temp_min_pair[1]
                temp_min_position = j
        del self.q[temp_min_position]
        return temp_min_pair

    def insert(self, state, priority):
        '''We do not keep the list sorted, in this implementation.'''
        # print("calling insert with state, priority: ", state, priority)

        if self[state] != -1:
            print("Error: You're trying to insert an element into a My_Priority_Queue instance,")
            print(" but there is already such an element in the queue.")
            return
        self.q.append((state, priority))

    def __len__(self):
        '''We define length of the priority queue to be the
        length of its list.'''
        return len(self.q)

    def __getitem__(self, state):
        '''This method enables Pythons right-bracket syntax.
        Here, something like  priority_val = my_queue[state]
        becomes possible. Note that the syntax is actually used
        in the insert method above:  self[state] != -1  '''
        for (S, P) in self.q:
            if S == state: return P
        return -1  # This value means not found.

    def __delitem__(self, state):
        '''This method enables Python's del operator to delete
        items from the queue.'''
        # print("In MyPriorityQueue.__delitem__: state is: ", str(state))
        for count, (S, P) in enumerate(self.q):
            if S == state:
                del self.q[count]
                return

    def __str__(self):
        txt = "My_Priority_Queue: ["
        for (s, p) in self.q: txt += '(' + str(s) + ',' + str(p) + ') '
        txt += ']'
        return txt


def runAStar():
    '''the main function that initialize the parameters and starting states'''
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS, MAX_OPEN_LENGTH, SOLUTION_PATH
    COUNT = 0
    BACKLINKS = {}
    MAX_OPEN_LENGTH = 0
    SOLUTION_PATH = AStar(initial_state)
    print(str(COUNT) + " states expanded.")
    print('MAX_OPEN_LENGTH = ' + str(MAX_OPEN_LENGTH))
    # print("The CLOSED list is: ", ''.join([str(s)+' ' for s in CLOSED]))


def AStar(initial_state):
    '''A* Search. This is the actual algorithm.'''
    global g, COUNT, BACKLINKS, MAX_OPEN_LENGTH, CLOSED, TOTAL_COST
    CLOSED = {}
    BACKLINKS[initial_state] = None

    OPEN = My_Priority_Queue()
    OPEN.insert(initial_state, h(initial_state))
    g[initial_state] = 0.0

    while len(OPEN) > 0:
        # print("OPEN starts with:" + str(OPEN))
        if VERBOSE:
            report(OPEN, CLOSED, COUNT)
        if len(OPEN) > MAX_OPEN_LENGTH:
            MAX_OPEN_LENGTH = len(OPEN)

        (S, P) = OPEN.delete_min()
        # print("In Step 3, returned from OPEN.delete_min with results (S,P)= ", (str(S), P))
        CLOSED[S] = P

        if Problem.GOAL_TEST(S):  # check if goal state
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            path = backtrace(S)
            print('Length of solution path found: ' + str(len(path) - 1) + ' edges')
            TOTAL_COST = g[S]
            print('Total cost of solution path found: ' + str(TOTAL_COST))
            return path
        COUNT += 1

        for op in Problem.OPERATORS:
            if op.precond(S):
                new_state = op.state_transf(S)
                # print("new_state is " + str(new_state))
                new_h = h(new_state)
                gs = g[S]
                edge = S.edge_distance(new_state)
                new_g = gs + edge
                new_f = new_g + new_h
                # print("new_h: {}, new_g: {}, gs: {}, edge: {}, new_f: {}".format(new_h, new_g, gs, edge, new_f))

                if new_state in CLOSED:  # If new_state already in CLOSED:
                    # print("in CLOSED")
                    old_f = CLOSED[new_state]
                    if new_f >= old_f:
                        del new_state
                    if new_f < old_f:
                        CLOSED.pop(new_state)
                        OPEN.insert(new_state, new_f)
                        g[new_state] = new_g
                        BACKLINKS[new_state] = S
                elif new_state in OPEN:  # If new_state already in OPEN:
                    q = OPEN[new_state]
                    if new_f >= q:
                        del new_state
                    if new_f < q:
                        OPEN.__delitem__(new_state)
                        OPEN.insert(new_state, new_f)
                        g[new_state] = new_g
                        BACKLINKS[new_state] = S
                else:  # if new_state is not in either list
                    OPEN.insert(new_state, new_f)
                    g[new_state] = new_g
                    BACKLINKS[new_state] = S
    return None  # No more states on OPEN, and no goal reached.


def print_state_queue(name, q):
    print(name + " is now: ", end='')
    print(str(q))


def backtrace(S):
    global BACKLINKS
    path = []
    while S:
        path.append(S)
        S = BACKLINKS[S]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(s)
    return path


def report(open, closed, count):
    print("len(OPEN)=" + str(len(open)), end='; ')
    print("len(CLOSED)=" + str(len(closed)), end='; ')
    print("COUNT = " + str(count))


if __name__ == '__main__':
    runAStar()

