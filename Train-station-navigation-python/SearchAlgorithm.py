# This file contains all the required routines to make an A* search algorithm.
#
__authors__='EduardSergiRoger'
__group__='DV11'
# _________________________________________________________________________________________
# Intel.ligencia Artificial 
# Grau en Enginyeria Informatica
# Curs 2015-2016
# Universitat Autonoma de Barcelona
# _________________________________________________________________________________________

from SubwayMap import *
import math


class Node:
    # __init__ Constructor of Node Class.
    def __init__(self, station, father):
        """
        __init__: 	Constructor of the Node class
        :param
                - station: STATION information of the Station of this Node
                - father: NODE (see Node definition) of his father
        """
        
        self.station = station      # STATION information of the Station of this Node
        self.g = 0                  # REAL cost - depending on the type of preference -
                                    # to get from the origin to this Node
        self.h = 0                  # REAL heuristic value to get from the origin to this Node
        self.f = 0                  # REAL evaluate function
        self.parentsID = []         # TUPLE OF NODES (from the origin to its father)
        self.father = father        # NODE pointer to his father
        self.time = 0               # REAL time required to get from the origin to this Node
                                    # [optional] Only useful for GUI
        self.num_stopStation = 0    # INTEGER number of stops stations made from the origin to this Node
                                    # [optional] Only useful for GUI
        self.walk = 0               # REAL distance made from the origin to this Node
                                    # [optional] Only useful for GUI
        self.transfers = 0          # INTEGER number of transfers made from the origin to this Node
                                    # [optional] Only useful for GUI


    def setEvaluation(self):
        """
        setEvaluation: 	Calculates the Evaluation Function
        :returns
                - f: REAL evaluate function
        """
        self.f = self.g + self.h


    def setHeuristic(self, typePreference , node_destination , city):
        """"
        setHeuristic: 	Calculates the heuristic depending on the preference selected
        :params
                - typePreference: INTEGER Value to indicate the preference selected: 
                                0 - Null Heuristic
                                1 - minimum Time
                                2 - minimum Distance 
                                3 - minimum Transfers
                                4 - minimum Stops
                - node_destination: PATH of the destination station
                - city: CITYINFO with the information of the city (see CityInfo class definition)
        """
        distancia = math.sqrt((node_destination.station.x - self.station.x)**2 + (node_destination.station.y - self.station.y)**2)
        temps = distancia / city.max_velocity
        if int(typePreference) == 0: #null h
            self.h = None
        elif (typePreference) == 1: #Time 
            self.h = temps

        elif int(typePreference) == 2: #Distance
            self.h = distancia

        elif int(typePreference) == 3: #Transfers
            if node_destination.station.id in city.multipleStations: #estacio amb mes d'una linia
                for ele in city.multipleStations[node_destination.station.id]:
                    if self.station.line == stationList[ele-1].line:
                        break
                    else:
                        self.h = 1
            elif node_destination.station.line != self.station.line: #estacio amb una linia
                    self.h = 1

        elif int(typePreference) == 4: #Stops
            for key in self.station.destinationDic:
                if key != node_destination:
                    self.h = 1

    def setRealCost(self,  costTable):
        """
        setRealCost: 	Calculates the real cost depending on the preference selected
        :params
                 - costTable: DICTIONARY. Relates each station with their adjacency an their real cost. NOTE that this
                             cost can be in terms of any preference.
        """
        aux = self
        self.g = 0
        while aux.father != None:
            try:
                self.g += costTable[aux.father.station.id][aux.station.id]
                aux = aux.father
            except:
                print "error clau dict", (self.father.station.id,self.station.id)


def Expand(fatherNode, stationList, typePreference, node_destination, costTable,city):
    """
        Expand: It expands a node and returns the list of connected stations (childrenList)
        :params
                - fatherNode: NODE of the current node that should be expanded
                - stationList: LIST of the stations of a city. (- id, destinationDic, name, line, x, y -)
                - typePreference: INTEGER Value to indicate the preference selected:
                                0 - Null Heuristic
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
                                4 - minimum Stops
                - node_destination: NODE (see Node definition) of the destination
                - costTable: DICTIONARY. Relates each station with their adjacency an their real cost. NOTE that this
                             cost can be in terms of any preference.
                - city: CITYINFO with the information of the city (see CityInfo class definition)
        :returns
                - childrenList:  LIST of the set of child Nodes for this current node (fatherNode)

    """
    childrenList = []   
    for key in fatherNode.station.destinationDic:
        nodeAux = Node(stationList[key-1],fatherNode)
        childrenList.append(nodeAux)    
        nodeAux.setHeuristic(typePreference,node_destination, city) #h
        nodeAux.setRealCost(costTable) #g
        nodeAux.setEvaluation() #f = g + h

        nodeAux.time = fatherNode.time
        time = fatherNode.station.destinationDic[nodeAux.station.id]
        nodeAux.time += time
        nodeAux.walk = fatherNode.walk
        if nodeAux.station.name != fatherNode.station.name:
            nodeAux.walk += city.velocity_lines[fatherNode.station.line -1] * time

        nodeAux.transfers = fatherNode.transfers
        if nodeAux.station.line != fatherNode.station.line:
            nodeAux.transfers +=1
        nodeAux.num_stopStation = fatherNode.num_stopStation
        nodeAux.num_stopStation +=1

        nodeAux.parentsID.insert(0,fatherNode.station.id)
        if fatherNode.parentsID != None: #quan no es el node origen (ja que no te pare)
            nodeAux.parentsID.extend(fatherNode.parentsID)
        
    return childrenList
  


def RemoveCycles(childrenList):
    """
        RemoveCycles: It removes from childrenList the set of childrens that include some cycles in their path.
        :params
                - childrenList: LIST of the set of child Nodes for a certain Node
        :returns
                - listWithoutCycles:  LIST of the set of child Nodes for a certain Node which not includes cycles
    """
    listWithoutCycles = childrenList
    for child in listWithoutCycles:
        if child.station.id in child.parentsID:
            listWithoutCycles.remove(child)

    return listWithoutCycles


def RemoveRedundantPaths(expandList, TCP, llista):
    """
        RemoveRedundantPaths:   It removes the Redundant Paths. They are not optimal solution!
                                If a node is visited and have a lower g in this moment, TCP is updated.
                                In case of having a higher value, we should remove this child.
                                If a node is not yet visited, we should include to the TCP.
        :params

        :returns

    """
    for path in expandList: #per als nodes de la llista a nodes a visitar
        if path[0].station.id in TCP:
            cp = TCP[path[0].station.id]
            if path[0].g < cp:
                TCP[path[0].station.id] = path[0].g
                for j in range(len(llista) -1):
                    if (llista[j][0].station.id == path[0].station.id):

                        llista.pop(j)
            elif path[0].g > cp:
                expandList.remove(path)
        else:
            TCP[path[0].station.id] = path[0].g
    return expandList, llista, TCP






def setCostTable( typePreference, stationList,city):
    """
    setCostTable :      Real cost of a travel.
    :param
            - typePreference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
                                4 - minimum Stops
            - stationList: LIST of the stations of a city. (- id, destinationDic, name, line, x, y -)
            - city: CITYINFO with the information of the city (see CityInfo class definition)
    :return:
            - costTable: DICTIONARY. Relates each station with their adjacency an their g, depending on the
                                 type of Preference Selected.
    """

    for ele in stationList: #diccionari de estacions amb mes d'una linia
        l = []
        for key in ele.destinationDic:
            if ele.name == stationList[key-1].name:
                l.append(stationList[key-1].id)
        city.multipleStations[ele.id] = l

    dicc = {}
    if int(typePreference) == 0 or int(typePreference) == 4: #adjecency
        for ele in stationList:
            dicc[ele.id] = {}
            for key in ele.destinationDic:
                dicc[ele.id][key] = 1
        return dicc

    elif int(typePreference) == 1: #time
        for ele in stationList:
            dicc[ele.id] = {}
            for key in ele.destinationDic:
                dicc[ele.id][key] = ele.destinationDic[key]
        return dicc
        
    elif int(typePreference) == 2: #distance
        for ele in stationList:
            v = city.velocity_lines[ele.line-1]
            dicc[ele.id] = {}
            for key in ele.destinationDic:
                if ele.name == stationList[key-1].name:
                    dicc[ele.id][key] = 0 #mateixa estacio diferent linia
                else:
                    dicc[ele.id][key] = v * ele.destinationDic[key] # e = v * t   
        return dicc

    elif int(typePreference == 3): #transfers
        for ele in stationList:
            dicc[ele.id] = {}
            for key in ele.destinationDic:
                if ele.line != stationList[key-1].line:
                    dicc[ele.id][key] = 1 
                else:
                 dicc[ele.id][key] = 0        
        return dicc    

  

    




def coord2station(coord, stationList):
    """
    coord2station :      From coordinates, it searches the closest station.
    :param
            - coord:  LIST of two REAL values, which refer to the coordinates of a point in the city.
            - stationList: LIST of the stations of a city. (- id, destinationDic, name, line, x, y -)

    :return:
            - possible_origins: List of the Indexes of the stationList structure, which corresponds to the closest
            station
    """
    x = coord[0]
    y = coord[1]
    possible_origins = []
    minim = 100000
    for ele in stationList:
        x1 = ele.x
        y1 = ele.y
        dist = math.sqrt(((x-x1)**2) + ((y-y1)**2))
        if dist < minim:
            minim = dist
            estacio = ele
    possible_origins.append(estacio.id-1)
    for ele1 in estacio.destinationDic:
        if stationList[ele1-1].name == estacio.name:
            possible_origins.append(stationList[ele1-1].id-1)
    return possible_origins



def AstarAlgorithm(stationList, coord_origin, coord_destination, typePreference,city,flag_redundants):
    """
     AstarAlgorithm: main function. It is the connection between the GUI and the AStar search code.
     INPUTS:
        - stationList: LIST of the stations of a city. (- id, name, destinationDic, line, x, y -)
        - coord_origin: TUPLE of two values referring to the origin coordinates
        - coord_destination: TUPLE of two values referring to the destination coordinates
        - typePreference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
                            4 - minimum Stops
        - city: CITYINFO with the information of the city (see CityInfo class definition)
    OUTPUTS:
        - time: REAL total required time to make the route
        - distance: REAL total distance made in the route
        - transfers: INTEGER total transfers made in the route
        - stopStations: INTEGER total stops made in the route
        - num_expanded_nodes: INTEGER total expanded nodes to get the optimal path
        - depth: INTEGER depth of the solution
        - visitedNodes: LIST of INTEGERS, IDs of the stations corresponding to the visited nodes
        - idsOptimalPath: LIST of INTEGERS, IDs of the stations corresponding to the optimal path
        (from origin to destination)
        - min_distance_origin: REAL the distance of the origin_coordinates to the closest station
        - min_distance_destination: REAL the distance of the destination_coordinates to the closest station
        - flag_redundants: [0/1]. Flag to indicate if the algorithm has to remove the redundant paths (1) or not (0)


        EXAMPLE:
        return optimalPath.time, optimalPath.walk, optimalPath.transfers,optimalPath.num_stopStation,
        len(expandedList), len(idsOptimalPath), visitedNodes, idsOptimalPath, min_distance_origin,
        min_distance_destination
    """

    origen = coord2station(coord_origin, stationList) #llista d'origens
    desti = coord2station(coord_destination, stationList) #llista de destins


    class optimalPath:
        time = 0
        walk = 0
        transfers = 0
        num_stopStation = 0
        idsOptimalPath = []
        visitedNodes = []
        num_expanded_nodes = 0
        min_distance_destination = math.sqrt( (coord_destination[0]- stationList[desti[0]].x)**2 + (coord_destination[1]-stationList[desti[0]].y)**2 )
        min_distance_origin = math.sqrt( (coord_origin[0]- stationList[origen[0]].x)**2 + (coord_origin[1]-stationList[origen[0]].y)**2 )
        num_expanded_nodes = 0
    
    llista = []
    for i in origen:
        aux = [Node(stationList[i],None)]
        llista.append(aux)
    TCP = {}
    nodeDesti = Node(stationList[desti[0]],None)    
    costTable = setCostTable(typePreference, stationList,city)
    coord_head = [stationList[origen[0]-1].x,stationList[origen[0]-1].y]
    coord_destination = [nodeDesti.station.x, nodeDesti.station.y]

    while llista and coord_head != coord_destination: #mentre llista no buida i no trobem el desti

        headList = llista[0] #branca que triem explorar
        optimalPath.visitedNodes.append(headList[0].station.id)
        llista.pop(0) #treiem la branca a explorar ja que la actualitzarem
        expandList = Expand(headList[0], stationList, typePreference, nodeDesti, costTable,city) #expandim el cap del cap
        
        expandList = RemoveCycles(expandList)
        tmp = []
        for node in expandList: #afegim les opcions obtingudes
            add = []
            add.insert(0,node)
            add.extend(headList)
            tmp.append(add)
        expandList = tmp
        if flag_redundants == 1:
            expandList, llista, TCP = RemoveRedundantPaths(expandList, TCP, llista)
        optimalPath.num_expanded_nodes += len(expandList)
        llista.extend(expandList)
        llista.sort(key = lambda x: x[0].f) #ordenem la llista segons la f
        try:
            coord_head[0] = llista[0][0].station.x
            coord_head[1] = llista[0][0].station.y
        except:
            print "error"
    
    if llista:
        idsOptimalPath = []
        for ele in llista[0]:
            idsOptimalPath.append(ele.station.id)
        optimalPath.depth = len(idsOptimalPath)
        optimalPath.time = llista[0][0].time
        optimalPath.walk = llista[0][0].walk
        optimalPath.transfers = llista[0][0].transfers
        optimalPath.num_stopStation = llista[0][0].num_stopStation
        return optimalPath.time, optimalPath.walk, optimalPath.transfers, optimalPath.num_stopStation, len(optimalPath.visitedNodes),  len(idsOptimalPath),optimalPath.visitedNodes, idsOptimalPath, optimalPath.min_distance_origin, optimalPath.min_distance_destination
    else:
        return "No solution"






