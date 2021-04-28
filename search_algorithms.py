# algo from CLRS

import queue as q
import math

WHITE = "white"
GRAY = "gray"
BLACK = "black"


class Vertex:

    def __init__(self, name, state):
        """
        Initializer for a new Vertex object.
        name <- name of state; should be unique for hashing
        state <- 3-tuple of state data
        """
        self.name = name
        self.state = state
        self.onSolnPath = False
        self.parent = None
        self.nextOnPath = None

    def __hash__(self):
        """so that this can be used as a dictionary key"""
        return hash((self.name, self.state))

    def __eq__(self, other_vertex):
        """implements the == operator"""
        return self.name == other_vertex.name and self.state == other_vertex.state


class Graph:

    def __init__(self):
        self.adj_dict = {}
        self.vertex_set = set()
        self.initial_vertex = None
        self.final_vertex = None

    def addNewPath(self, vertex1, vertex2):
        self.vertex_set.add(vertex1)
        self.vertex_set.add(vertex2)
        vertex2.parent = vertex1

        if vertex1 in self.adj_dict.keys():
            self.adj_dict[vertex1].add(vertex2)  # this is a set
        else:
            self.adj_dict[vertex1] = {vertex2}

    def setInitialVertex(self, vert):
        self.initial_vertex = vert

    def setFinalVertex(self, vert):
        self.final_vertex = vert

    def addEdge(self, v1, v2):
        self.addNewPath(v1, v2)

    def addNewPaths(self, vertex_list):
        if len(vertex_list) % 2 != 0:
            return False

        for i in range(0, len(vertex_list), 2):
            self.addNewPath(vertex_list[i], vertex_list[i + 1])

    def getAllVertices(self):
        return list(self.vertex_set)

    def getAdjacentVertices(self, vertex):

        if vertex not in self.adj_dict.keys():
            return []
        return self.adj_dict[vertex]

    def printGraph(self):
        print("PRINTING GRAPH")
        verts = self.getAllVertices()

        for vert in verts:
            print("Key: ", vert.name)

            for each_vert in self.getAdjacentVertices(vert):
                print("\t\t", each_vert.name)


def breadthFirstSearch(graph, source_vertex, goal_vertex=None, debug=False):
    # First, find all vertices except the source
    path_to_solution = []
    goal_found = False

    color = dict()
    degree = dict()
    parent = dict()

    init_list = [vert for vert in graph.getAllVertices() if vert != source_vertex]

    if debug:
        print("Init list is: ")
        for a in init_list:
            print(a.name)

    for vertex in init_list:
        color[vertex] = WHITE
        degree[vertex] = math.inf  # infinite
        parent[vertex] = None

    color[source_vertex] = GRAY
    degree[source_vertex] = 0
    parent[source_vertex] = None

    my_queue = q.Queue()  # LIFO queue
    my_queue.put(source_vertex)

    while not my_queue.empty():
        vert = my_queue.get()

        # check for goal
        if vert == goal_vertex:
            goal_found = True
            break

        if debug:
            print("Exploring vertex ", vert.name)

        adj_list = graph.getAdjacentVertices(vert)

        if adj_list == []:
            print("ADJACENCY LIST EMPTY")
        for adj_vert in adj_list:
            if color[adj_vert] == WHITE:
                color[adj_vert] = GRAY
                degree[adj_vert] = degree[vert] + 1
                parent[adj_vert] = vert
                my_queue.put(adj_vert)

                if debug:
                    print("\tdiscovered {}".format(adj_vert.name))
        color[vert] = BLACK

    # generate the path to the solution, working backwards from the goal
    if goal_vertex is not None and goal_found:

        goal_vertex.onSolnPath = True
        path_to_solution.append(goal_vertex)
        m_parent = parent[goal_vertex]
        m_parent.nextOnPath = goal_vertex
        while m_parent:
            m_parent.onSolnPath = True
            path_to_solution.append(m_parent)

            if parent[m_parent]:
                parent[m_parent].nextOnPath = m_parent
            m_parent = parent[m_parent]

    # return the reverse of the reverse path list above
    return path_to_solution[::-1], color, degree, parent


def resetParentdict(graph, parent):
    for v in graph.getAllVertices():
        parent[v] = None


def depthFirstSearch(graph, start_vertex, goal_vertex, debug=False):
    path_to_solution = []
    color = dict()
    parent = dict()
    degree = dict()
    time = 0
    final_time = dict()

    # initial setting
    for vertex in graph.getAllVertices():
        color[vertex] = WHITE
        parent[vertex] = None

    oth_list = [v for v in graph.getAllVertices() if v != start_vertex]
    dfsVisit(graph, start_vertex, goal_vertex, color, parent, degree, time, final_time)
    for vert in oth_list:
        if color[vert] == WHITE:

            if debug:
                print("Visiting: ", vert.name)
            dfsVisit(graph, vert, goal_vertex, color, parent, degree, time, final_time)

    path_to_solution.append(goal_vertex)
    m_parent = parent[goal_vertex]
    m_parent.nextOnPath = goal_vertex
    while m_parent != start_vertex:
        path_to_solution.append(m_parent)

        if m_parent is None:
            break
        parent[m_parent].nextOnPath = m_parent
        m_parent = parent[m_parent]

    return path_to_solution[::-1]


def dfsVisit(graph, vertex, goal_vertex, c_dict, p_dict, d_dict, time, final_time):
    print("DFS visits ", vertex.state)
    c_dict[vertex] = GRAY  # the vertex 'vertex' has just been discovered
    time += 1
    d_dict[vertex] = time

    for v in graph.getAdjacentVertices(vertex):

        if c_dict[v] == WHITE:
            p_dict[v] = vertex
            dfsVisit(graph, v, goal_vertex, c_dict, p_dict, d_dict, time, final_time)

    c_dict[vertex] = BLACK
    time += 1  # futile
    final_time[vertex] = time

    return False


