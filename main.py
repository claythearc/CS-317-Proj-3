"""
Clayton A. Turner
CS 317 Project 3
Python 3.7 but should work on any Python 3.6+ due to f-string usage
Kruskal's Algoritm and Djikstras

"""

from collections import defaultdict, namedtuple, deque
import math


class Graph:

    def __init__(self):
        """ Default constructor that builds the Graph """
        self.root = list()  # type: list('Node')
        self.nodeset = set()  # type: set('Node')
        self.size = len(self.nodeset)  # type: int, holds # of unique vertexes
        self.distances = defaultdict(list)  # type: defaultdict(list)

    def addNode(self, node1: str, node2: str, weight: int, both=False):
        """Add a node into the Graph, and then sort the list"""
        self.distances[node1].append([node2, weight])
        if both:
            self.distances[node2].append([node1, weight])
        self.root.append(Node(node1, node2, weight))
        self.nodeset.add(node1)
        self.nodeset.add(node2)
        self.size = len(self.nodeset)
        self.sort()

    def __str__(self):
        """Overrides the dunder str method so that I can call print(Graph) directly
        Basically it creates a list of the desired output """
        temp = list()  # type: list
        temp.append("The graph has the letters {}".format(self.nodeset))
        for n in self:
            temp.append("{} to {} weight {}".format(n.node1, n.node2, n.weight))
        return str(temp)

    def __iter__(self):
        """iterator. This lets me call for x in Graph and iterate over each of the layers"""
        for item in self.root:
            yield item

    def sort(self):
        """Sort method that calls the .sort() method to map each element by the nodes weight. Then do not reverse
        So it stays in Non Decresasing order."""
        self.root.sort(key=lambda x: x.weight, reverse=False)

    def debug(self):
        for k,v in self.distances.items():
            print(f"Key: {k} Value: {v}")

    def neighbor(self, parent: str):
        """Return the nodes that neighbor the passed parent object"""
        for key, value in self.distances.items():
            if parent in key:
                for path in value:
                    yield path


class Node:
    def __init__(self, node1: str, node2: str, weight: int):
        """Constructfor for the Node Class"""
        self.node1 = node1
        self.node2 = node2
        self.weight = int(weight)

    def __lt__(self, other: 'Node'):
        """Overrides Node 1 < Node 2 by comparing the weight attribute"""
        return self.weight < other.weight

    def __le__(self, other):
        """Overrides Node1 <= Node 2 by comparing the weight attribute"""
        return self.weight <= other.weight

    def __str__(self):
        """Fancy String override to print the Node by calling print(Node)"""
        return "{} <-> {} Weight: {}".format(self.node1, self.node2, self.weight)


class MST:
    """Builds the Minimum Spanning Tree and Adjacency Matrix"""

    def __init__(self):
        self.total = 0  # type: int holds the total amount of nodes
        self.mst = list()  # type: list holds the nodes
        self.mstset = set()  # type: set holds the set of vertexes to know if this is a cycle

    def addmst(self, adjnode: Node):
        """Add a node to the Minimum Spanning Tree and the Minimum Spanning Tree Set """
        self.mst.append(adjnode)
        self.mstset.add(adjnode.node1)
        self.mstset.add(adjnode.node2)

    def is_cycle(self, newnode: Node, graph: Graph):
        """This method determines if the addition of a node will cause a cycle to form in the graph"""
        tempset = self.mstset.copy()  # create a copy of our MST Set variable
        tempset.add(newnode.node1)  # add node1 and node 2 to the set
        tempset.add(newnode.node2)
        return len(tempset) == len(self.mstset)  # if the lengths are the same it will create a cycle because a set

    # is guaranteed to have all unique elements

    def is_final(self, newnode: Node, graph: Graph):
        """Will the vertex complete the graph"""
        tempset = set()  # type: set temp variable
        for node in self.mst:  # iterate over the minimum spanning tree
            # node 1 is the left, node 2 is the right
            tempset.add(node.node2)  # add each right node
        tempset.add(newnode.node2)  # add the current destination to the temporary set
        return len(tempset) == (len(graph.nodeset) - 1)

    # if the length of our temp set is == the nodeset-1 then every node except the start point is within our graph

    def print(self):
        """Outputs the Minimum Spanning tree."""
        total = 0
        templist = ["MST:"]
        for node in self.mst:
            total += node.weight
            templist.append(f"{node.node1}-{node.node2} weight {node.weight}")
        templist.append(f"Total Weight: {total}")
        return templist


def kruskal(krusgraph: Graph):
    """Method to perform Kruskal's algorithm"""
    adjmat = MST()  # type: MST
    for node in krusgraph:  # iterate the Graph in sorted order
        if not adjmat.is_cycle(node, krusgraph):  # if the edge won't form a cycle
            adjmat.addmst(node)  # add it to the minimum spanning tree
        elif adjmat.is_final(node, krusgraph):  # if the node will complete the mst
            adjmat.addmst(node)  # add it
            break  # and break
    return adjmat  # return the Adjacency Object containing the mst


def Dijkstra(graph: Graph, source: str):
    """Algorithm for performing Djikstra's algorithm"""
    vertex = set(str())  # variable initialization
    dist = dict()
    prev = dict()
    for node in graph.nodeset:  # return the nodes in the graph, just the names and do initialization
        dist[node] = math.inf
        prev[node] = None
        vertex.add(node)
    dist[source] = 0  # set initial distance 0
    while vertex:  # while there are verticies to look over
        # pick the smallest thats still in our set
        u = min((item for item in dist.items() if item[0] in vertex), key=lambda i: i[1])[0]
        vertex.remove(u)  # remove the one we picked
        for neighbor in graph.neighbor(u): #returns a list [dest, weight] of its neighbors
            alt = dist[u] + neighbor[1]  # temp variable for its distance
            if alt < dist[neighbor[0]]:  # if the distance is more than our current one
                dist[neighbor[0]] = alt  # update the dicts
                prev[neighbor[0]] = u
    return dist, prev  # return our dictionaries


if __name__ == "__main__":
    KrusGraph = Graph()  # initiate instances of my Graph and DijGraph class
    with open("graph.txt") as f:  # open the file in a context manager to avoid memory leaks
        for line in f:  # for every line in the file
            to_node, from_node, weight = line.strip().split(",")  # strip the newline, unpack it based on a "," split
            KrusGraph.addNode(to_node, from_node, int(weight))  # add the path to the Kruskal Graph

    mstlist = kruskal(KrusGraph).print()

    costs, paths = Dijkstra(KrusGraph, "M")
    strlist = []
    for k, v in paths.items():
        temppstr = str()
        tempstr = f"Path: {k}"
        while v:
            tempstr += f" <- {v}"
            v = paths[v]
        tempstr += f" Distance = {costs[k]}"
        strlist.append(tempstr)
    with open("output.txt", "a+") as f:
        f.write("**************Directed*********** \n")
        f.write("***********Kruskal********* \n")
        f.write("\n".join(mstlist))
        f.write("\n************Djikstra******** \n")
        f.write("\n".join(strlist))

    #Duplicate code to run the graph again, in undirected mode.
    KrusGraph = Graph()  # initiate instances of my Graph and DijGraph class
    with open("graph.txt") as f:  # open the file in a context manager to avoid memory leaks
        for line in f:  # for every line in the file
            to_node, from_node, weight = line.strip().split(",")  # strip the newline, unpack it based on a "," split
            KrusGraph.addNode(to_node, from_node, int(weight), both=True)  # add the path to the Kruskal Graph

    mstlist = kruskal(KrusGraph).print()

    costs,paths = Dijkstra(KrusGraph, "M")
    strlist = []
    for k, v in paths.items():
        temppstr = str()
        tempstr = f"Path: {k}"
        while v:
            tempstr += f" <- {v}"
            v = paths[v]
        tempstr += f" Distance = {costs[k]}"
        strlist.append(tempstr)
    with open("output.txt", "a+") as f:
        f.write("\n**************Undirected***********\n")
        f.write("***********Kruskal********* \n")
        f.write("\n".join(mstlist))
        f.write("\n************Djikstra******** \n")
        f.write("\n".join(strlist))