import search_algorithms as serAlgo
import display_module as dsply_module
from timeit import default_timer as timer


class Application:

    def __init__(self, num_c, num_m, boat_pos):
        self.CANNIBALS = num_c
        self.MISSIONARIES = num_m
        self.ORIG_BOATPOS = boat_pos

        self.initial_state = (num_c, num_m, boat_pos)
        self.cur = self.initial_state

        self._graph = serAlgo.Graph()
        self.init_vert = serAlgo.Vertex(str(self.initial_state), self.initial_state)

    def getCurrentState(self):
        return self.cur_state

    def isStateLegal(self, state):
        numC = state[0]
        numM = state[1]

        # sanity check
        if numC < 0 or numM < 0:
            return False
        if numC > self.CANNIBALS or numM > self.MISSIONARIES:
            return False

        # other side
        oC = self.CANNIBALS - numC
        oM = self.MISSIONARIES - numM

        # outnumbered on one side, illegal
        if numC > numM and numM != 0:
            return False

        # outnumbered on the other side, also illegal
        if oC > oM and oM != 0:
            return False

        return True

    def addIfLegal(self, state):
        if self.isStateLegal(state):
            return [state]
        return []

    def generateAllLegalStates(self, state):
        c = state[0]
        m = state[1]
        b = state[2]

        legal_state_list = []

        # if the boat is on the left bank
        if b == 1:
            # move one missionary to the right
            st_1 = (c, m - 1, 0)
            legal_state_list.extend(self.addIfLegal(st_1))

            # cannibal to right
            st_2 = (c - 1, m, 0)
            legal_state_list.extend(self.addIfLegal(st_2))

            # both to the right
            st_3 = (c - 1, m - 1, 0)
            legal_state_list.extend(self.addIfLegal(st_3))

            # two of each kind
            st_4 = (c - 2, m, 0)
            legal_state_list.extend(self.addIfLegal(st_4))

            st_5 = (c, m - 2, 0)
            legal_state_list.extend(self.addIfLegal(st_5))
        else:

            # missionary to the left
            st_1 = (c, m + 1, 1)
            legal_state_list.extend(self.addIfLegal(st_1))

            # cannibal to the left
            st_2 = (c + 1, m, 1)
            legal_state_list.extend(self.addIfLegal(st_2))

            # both to the left
            st_3 = (c + 1, m + 1, 1)
            legal_state_list.extend(self.addIfLegal(st_3))

            st_4 = (c + 2, m, 1)
            legal_state_list.extend(self.addIfLegal(st_4))

            st_5 = (c, m + 2, 1)
            legal_state_list.extend(self.addIfLegal(st_5))

        return legal_state_list

    def goalTest(self, state):
        return state == (0, 0, 0)

    def addSuccessorsToGraph(self, g_state):
        g_vert = serAlgo.Vertex(str(g_state), g_state)
        next_states = self.generateAllLegalStates(g_state)

        for state in next_states:
            vert = serAlgo.Vertex(str(state), state)
            # skip if this state is equal to the parent state ( which must be one of the adjacent states )
            adjacent_vertices = self._graph.getAdjacentVertices(g_vert)
            if vert in adjacent_vertices:
                self._graph.addNewPath(g_vert, vert)
                continue

            self._graph.addNewPath(g_vert, vert)
            self.addSuccessorsToGraph(state)

    def generateGraph(self):
        self.addSuccessorsToGraph(self.init_vert.state)

    def solveBFS(self):
        print("The graph is: ")
        self._graph.printGraph()

        g = (0, 0, 0)
        goal_vertex = serAlgo.Vertex(str(g), g)
        self._graph.setFinalVertex(goal_vertex)

        path, _, _, _ = serAlgo.breadthFirstSearch(self._graph, self.init_vert, goal_vertex, False)

        print("The solution path is: ")
        for x in path[:-1]:
            print(x.name, " -> ")
        print(path[-1].name)

        return path

    def solveDFS(self):

        print("The graph is: ")
        self._graph.printGraph()
        g = (0, 0, 0)
        goal_vertex = serAlgo.Vertex(str(g), g)

        self._graph.setFinalVertex(goal_vertex)
        path = serAlgo.depthFirstSearch(self._graph, self.init_vert, goal_vertex, True)

        print("The solution path is: ")
        for x in path[:-1]:
            print(x.name, " -> ")
        print(path[-1].name)


if __name__ == '__main__':
    app = Application(3, 3, 1)
    app.generateGraph()
    app._graph.setInitialVertex(app.init_vert)

    method = input("Method? Type B for BFS, D for DFS:")
    method = method.lower()

    path = []
    start = timer()
    if method == 'b':
        path = app.solveBFS()
    else:
        path = app.solveDFS()
    end = timer()

    print("The time taken is: ", (end - start) * 1000, "milliseconds")

    stri = "BFS" if method == 'b' else "DFS"

    d = dsply_module.DisplayModule()
    d.algo_used = stri
    d.setGraph(app._graph)
    d.mainLoop()
