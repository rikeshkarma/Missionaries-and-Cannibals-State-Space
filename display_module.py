import pygame as pg
import search_algorithms as ser


class DisplayModule:

    def __init__(self):
        self.algo_used = 'BFS'
        pg.init()
        self.screen = pg.Surface((1450, 1200))
        self.graph = None
        self.rad = 8
        self.font = pg.font.SysFont('Arial', 26)
        self.seen_list = []
        self.draw_checked_list = []  # for tracing the path to the solution

    def setGraph(self, graph):
        self.graph = graph

    def isAncestor(self, vert, possible_vert):
        a = vert.parent
        while a:
            if a == possible_vert:
                return True
            a = a.parent

        return False

    def checkOnSolnPath(self, vert, parent):
        if not vert:
            return False

        if vert in self.draw_checked_list:
            return False

        if vert.state == (3, 3, 1) and parent is not None:
            return False

        self.draw_checked_list.append(vert)
        x = vert
        while x.nextOnPath is not None:
            x = x.nextOnPath

        # temp hack for solution
        if x.state == (0, 0, 0):
            # print("OK!")
            return True
        return False

    def drawVertex(self, vertex, parent_vertex, x, y, numChildrenToDraw, depth):
        nc = numChildrenToDraw

        if vertex.state in self.seen_list:
            nc = 1

        col = (255, 0, 0)

        self.seen_list.append(vertex.state)

        if vertex == self.graph.final_vertex:
            col = (0, 255, 0)
        if numChildrenToDraw == 0:  # draw no children
            col = (255, 0, 255)

        pg.draw.circle(self.screen, col, (x, y), self.rad)
        self.screen.blit(self.font.render(vertex.name, True, (0, 0, 255)), (x, y))

        if vertex == self.graph.final_vertex:
            return

        if numChildrenToDraw == 0:
            return

        # distribute allocated area to successors

        dx = -100
        dy = 100

        li = [x for x in self.graph.getAdjacentVertices(vertex) if x != parent_vertex]

        for each in li:
            if self.isAncestor(vertex, each):
                # continue
                return
                # dc=False
            '''
            # if we keep the second condition, we need a depth limit
            if each.state in self.seen_list and self.isAncestor(vertex, each):
                #return
                return
            '''
            if each.state in self.seen_list:
                nc = 1  # 2

            self.drawVertex(each, vertex, x + dx, y + dy, nc - 1, depth + 1)

            if self.checkOnSolnPath(each, vertex):
                pg.draw.line(self.screen, (255, 255, 0), (x, y), (x + dx, y + dy), 3)

            else:
                pg.draw.line(self.screen, (255, 255, 255), (x, y), (x + dx, y + dy))

            dx += 100
        # self.seen_list.append(vertex.state)

    def mainLoop(self):
        # temp hack, add initial soln to checked list
        self.drawVertex(self.graph.initial_vertex, ser.Vertex("fas", (12, 12, 12)), 1200, 20, -1, 1)
        pg.image.save(self.screen, self.algo_used + "_graph.jpeg")

        print("Graph saved as", self.algo_used + "_graph.jpeg")
