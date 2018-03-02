from __future__ import division

"""
This script simulates a random biological network
and includes code for NetworkNode objects

"""
from random import random
from copy import copy

class NetworkNode(object):
    """A network node"""
    def __init__(self,edges=[],name=None,properties={}):
        """initialize a NetworkNode object
        edges -- a list of NetworkNode objects connected to self
        name -- the name of the node as a str
        properties -- a dictionary of metadata about the node
        """
        self.Edges = copy(edges)
        #Why not just self.Edges = edges?
        #default parameter values are created once
        #so that would sneakily make all nodes
        #share the same edge list!
        self.Name = name
        self.Properties = copy(properties)
         
    def degree(self):
        """Returns the degree of the node"""
        result = len(self.Edges)  
        return result
    
    def addEdge(self,other):
        """Add an edge between self and another node"""
        if other not in self.Edges:
            self.Edges.append(other)


def erdos_renyi_random_network(n,p):
    """Define a random Erdos-Renyi network with n nodes
    n - number of nodes
    p - probability any pair of nodes is connected
    """
    #Generate nodes
    network = []
    for i in range(n):
        curr_node = NetworkNode(name=i)
        network.append(curr_node)
    #Connect nodes
    #Note the function doesn't need to return anything
    #as the Node objects are modified 'in place' rather
    #than copied.
    connect_nodes_random(network,p)
    
    return network

def connect_nodes_random(network,p):
    """Randomly add edges between all node pairs with uniform probability p
    network -- a list of Node objects representing an *undirected* network
    p -- the probability that two nodes will be connected  
    """

    for i,curr_node1 in enumerate(network):
        for j,curr_node2 in enumerate(network):
            #Don't add edges between node
            #and itself
            if i == j:
                continue
            
            if random() <= p:
                curr_node1.addEdge(curr_node2)          
                curr_node2.addEdge(curr_node1)

if __name__ == "__main__":
    random_network_10 = erdos_renyi_random_network(30,0.10)
    for node in random_network_10:
        print("Node name:\n",node.Name,"\t",node.degree())
        print("Edges:",sorted([edge.Name for edge in node.Edges]))
