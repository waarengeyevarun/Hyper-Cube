# -*- coding: utf-8 -*-
import random
import threading
import string
import time
import os, os.path

Threads = []
HopsCount = []
HopsToGenerateFile = []
HopsToLookUp = []


class hypercube(object):
    def __init__(self, n):

        self.n = n
        self.vertices = []
        self.edges = {}
        self.edgeAsVertexDirection = {}
        self.nonAdjacentPairs = {}

        def genVertices(self):
            """
            generates vertices as n bit strings
            """
            for i in range(2 ** self.n):
                vertex = ''
                for k in range(self.n):
                    # print('i='+ str(i))
                    temp = (i / (2 ** (k))) % 2
                    # print('temp='+ str(temp))
                    vertex = str(temp) + vertex
                    # print('vertex='+ str(vertex))
                self.vertices.append(vertex)

        genVertices(self)

        def genEdgeFromVertexDirection(self, vertex, direction):
            """
            creates an edge from vertex and direction
            """
            edge = []
            targetVertex = list(vertex)
            if vertex[self.n - 1 - direction] == '0':
                targetVertex[self.n - 1 - direction] = '1'
                edge = (vertex, "".join(targetVertex))
            else:
                targetVertex[self.n - 1 - direction] = '0'
                edge = ("".join(targetVertex), vertex)
            return edge

        def genDirectionalEdges(self, direction):
            """
            creates all the edges in a given direction
            """
            directionalEdges = []
            hypercubeOneLessDim = hypercube(self.n - 1)
            VerticesOneLessDim = hypercubeOneLessDim.getVertices()
            for i in range(2 ** (self.n - 1)):
                SourceVertex = list(VerticesOneLessDim[i])
                SourceVertex.insert(self.n - 1 - direction, '0')
                directionalEdges.append(genEdgeFromVertexDirection(self, "".join(SourceVertex), direction))
            return directionalEdges

        def genEdges(self):
            for direction in range(self.n):
                directionalEdges = genDirectionalEdges(self, direction)
                self.edges.update(dict.fromkeys(directionalEdges, direction))
                self.edgeAsVertexDirection.update(
                    dict(zip([(x[0], direction) for x in directionalEdges], directionalEdges)))
                self.edgeAsVertexDirection.update(
                    dict(zip([(x[1], direction) for x in directionalEdges], directionalEdges)))

        genEdges(self)

        def genNonAdjacentPairs(self):
            vertices = self.vertices
            edges = self.edges.keys()

            for v1 in vertices:
                for v2 in vertices:
                    if v1 < v2 and ((v1, v2) not in edges):
                        self.nonAdjacentPairs.update(
                            {(v1, v2): [n - 1 - i for i in range(n) if list(v1)[i] != list(v2)[i]]})

        genNonAdjacentPairs(self)

    def getVertices(self):
        return self.vertices

    def getEdges(self):
        return self.edges

    def getNonAdjacentPairs(self):
        return self.nonAdjacentPairs

    def getEdgeAsVertexDirection(self):
        return self.edgeAsVertexDirection

    def genEdgeFromVertexDirection(self, vertex, direction):
        edge = []
        targetVertex = list(vertex)
        if vertex[self.n - 1 - direction] == '0':
            targetVertex[self.n - 1 - direction] = '1'
            edge = (vertex, "".join(targetVertex))
        else:
            targetVertex[self.n - 1 - direction] = '0'
            edge = ("".join(targetVertex), vertex)
        return edge

    def genDirectionalEdges(self, direction):
        directionalEdges = []
        hypercubeOneLessDim = hypercube(self.n - 1)
        VerticesOneLessDim = hypercubeOneLessDim.getVertices()
        for i in range(2 ** (self.n - 1)):
            SourceVertex = list(VerticesOneLessDim[i])
            SourceVertex.insert(self.n - 1 - direction, '0')
            directionalEdges.append(self.genEdgeFromVertexDirection("".join(SourceVertex), direction))
        return directionalEdges


################ Important ###########################
def getHopsCount(src, dest):
    # for e in ActualCube.edges:
    #   print e
    # if (src,dest) in ActualCube.edges:
    # print '\npass'
    cnt = 0
    while 1 == 1:
        if (src, dest) in ActualCube.edges:
            cnt = cnt + 1
            break
        if (dest, src) in ActualCube.edges:
            cnt = cnt + 1
            break

        for e in ActualCube.edges:
            if str(src) in str(e):
                if str(e[0]) == str(src):
                    src = str(e[1])
                else:
                    src = str(e[0])
                cnt = cnt + 1
        break
        if cnt > len(ActualCube.edges):
            return 0
        break;
    # return random.SystemRandom().randint(1, total_files)
    return cnt


def FileGen(t_name, m):  # worker function to generate Files
    # print('Thread: %s\r' %t_name)
    files_produced = 0
    while files_produced < m:
        # work a random time between 1 and 10 seconds // simulate user producing file
        time.sleep(random.SystemRandom().randint(0, 10))

        # produce random file and its key k // simulate user saving file in P2P
        random_string = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
        print('Thread ' + t_name + ', Generated Random String:' + random_string)
        total_sum = 0
        for c in random_string:
            # print 'ASCII of :'+ c + str(ord(c))
            total_sum = total_sum + ord(c)
        key = total_sum % (2 ** n)
        # print '\nTotal Sum: ' + str(total_sum)
        binary_key = str(format(key, "0" + str(n) + "b"))
        print 'Key: ' + str(
            key) + ' In Binary: ' + binary_key  # to format according to n, adding 0s as prefix, for ex 0=00 if n=2
        HopsToGenerateFile.append(getHopsCount(t_name, binary_key))  # calculate Hops
        # store the file in the node with identifier = key k // simulate P2P in action
        file = open(str(binary_key) + ".txt", "a+")
        file.write(random_string + '\n')
        file.close()

        # for threads in threading.enumerate():
        # print('\n' + threads.getName() + '-' + str(d.val))

        files_produced = files_produced + 1
        # work a random time between 1 and 10 seconds // simulate user doing other things
    return


def LookUp(t_name, p, NodeKeys):  # worker function to LookUp Files
    files_retrived = 0
    time.sleep(random.SystemRandom().randint(0, 10))
    while files_retrived < p:
        # HopsCount.append(getHopsCount(len(NodeKeys)))#Number of Hops to be looked Up
        random_key = random.choice(NodeKeys)  # select random key from the previously generated files
        # print "Chosen File: " + str(random_key)
        print'Node ' + t_name + ' is Looking Up for the File with Key ' + str(
            int(random_key.replace(".txt", ""), 2)) + ' Stored at Node ' + str(random_key)
        file = open(str(random_key), "r")
        print 'File Content:\n' + file.read()
        # print str(random_key.replace(".txt",""))
        HopsToLookUp.append(getHopsCount(t_name, random_key.replace(".txt", "")))  # Number of Hops to LookUp
        files_retrived = files_retrived + 1
    return


def KillNodes(q, r, NodeKeys):  # worker function to LookUp Files
    nodes_killed = 0
    while nodes_killed < q:
        time.sleep(r)
        random_node_to_delete = random.choice(NodeKeys)  # select random key from the previously generated files
        # print "Chosen File: " + str(random_key)
        print'\nNode ID To Be Killed: ' + str(int(random_node_to_delete.replace(".txt", ""), 2))
        indexToDelete = []
        for e in ActualCube.edges:
            if str(random_node_to_delete.replace(".txt", "")) in str(e):
                # print str(int(random_node_to_delete.replace(".txt",""), 2))
                indexToDelete.append(e)

        for i in indexToDelete:
            del ActualCube.edges[i]

        # print 'Length Of Edges:' + str(len(ActualCube.edges))
        nodes_killed = nodes_killed + 1
    return


print'\n\n************* Goal-1 ***************'
n = int(input("How many dimensions required for Hypercube?: "))
m = int(input("\nHow many Files to be Generated by each Node?: "))
ActualCube = hypercube(n)

print('\nAppending Threads with the Nodes in Cube...')
for f in ActualCube.vertices:
    t = threading.Thread(name=f, target=FileGen, args=(f, m))
    Threads.append(t)
    print '\n' + str(f)

print('\nCompleted!')
print('\nConnection Among ' + str(2 ** n) + ' Threads')
for e in ActualCube.edges:
    print e

print'\n************* Goal-1 Accomplished ***************'

s = int(input("\nGo Ahead....? Press Any Number and Enter: "))

print'\n\n************* Goal-2 ***************\n'

for threads in Threads:
    threads.start()
    threads.join()

print '\nHops To Generate Files:' + str(HopsToGenerateFile)
# print '\n' + str(len([name for name in os.listdir('.') if name.endswith('.txt')])) + ' Hops Required to store ' + str(m) + ' File(s) generated by each of the ' + str(2**n) + ' Nodes.'
print '\n' + str(sum(HopsToGenerateFile) / len(HopsToGenerateFile)) + ' : Average Hops Required to store ' + str(
    m) + ' File(s) generated by each of the ' + str(2 ** n) + ' Nodes.'
HopsToGenerateFile
print'\n************* Goal-2 Accomplished ***************'

print'\n\n************* Goal-3 ***************'
# for f in onlyfiles:
#    if '.txt' in f:
#        onlyNodeFiles.append(f)
NodeKeys = [name for name in os.listdir('.') if name.endswith('.txt')]  # lookup for the previously generated files
# print 'Node Keys: ' + str(NodeKeys)
p = int(input("How many Files to be Retrieved by each Node? (Should be <= m here, m=" + str(m) + "): "))
for f in ActualCube.vertices:
    t = threading.Thread(name=f, target=LookUp, args=(f, p, NodeKeys))
    t.start()
    t.join()

print 'Hops to LookUp Files: ' + str(HopsToLookUp)
print str(sum(HopsToLookUp) / len(HopsToLookUp)) + ' : Average Hops required to lookup & retrieve ' + str(
    p) + ' file(s) among ' + str(m * (2 ** n)) + ' files in ' + str((2 ** n)) + ' Nodes by each Node.'
print str(len([i for i in HopsToLookUp if i == 0])) + ' Lookup Failure(s)'
print'\n************* Goal-3 Accomplished ***************'
################ Important ###########################

print'\n************* Goal-4 ***************'
# for f in onlyfiles:
#    if '.txt' in f:
#        onlyNodeFiles.append(f)
NodeKeys = [name for name in os.listdir('.') if name.endswith('.txt')]  # lookup for the previously generated files
HopsToLookUp = []
q = int(input("How many Nodes to Attack out of " + str(2 ** n) + " Nodes? : "))
r = int(input("How long(seconds) should Evil Thread Work?: "))
for f in ActualCube.vertices:
    t = threading.Thread(name=f, target=LookUp, args=(f, p, NodeKeys))  # Try to retrieve p number of files
    t.start()

evilthread = threading.Thread(name='evil', target=KillNodes, args=(q, r, NodeKeys))
evilthread.start()

time.sleep(200)
print 'Hops to LookUp Files: ' + str(HopsToLookUp)
print str(sum(HopsToLookUp) / (len(HopsToLookUp) - len([i for i in HopsToLookUp if
                                                        i == 0]))) + ' : Average Hops required to lookup & retrieve After Evil Thread Introduced to kill ' + str(q) + ' after each ' + str(r) + ' seconds.'
print str(len([i for i in HopsToLookUp if i == 0])) + ' Lookup Failure(s)'
print'\n************* Goal 4 Accomplished ***************'
# print str(len(ActualCube.edges))
################ Important ###########################