from SearchAlgorithm import *
from SubwayMap import *

def main():

    #------------------------------------------------------------------#
    #read file
    filename='Stations_Session1.txt'
    stationList=readStationInformation(filename)
    #read adjacency matrix
    filename='Connections_Session1.txt'
    adjacency=readCostTable(filename)

    #Real TIME cost table
    filename = 'PartialLyon_Session1_Time.txt'
    timeStations = readCostTable(filename)
    setNextStations(stationList, timeStations)

    # CITY information
    # velocity
    filename = "PartialLyon_Session1_InfoVelocity.txt"
    infoVelocity = readInformation(filename)
    # Transfers times
    filename = "PartialLyon_Session1_InfoTransfers.txt"
    infoTransfers = readInformation(filename)
    city=CityInfo(len(infoVelocity),infoVelocity,infoTransfers,adjacency)

    #------------------------------------------------------------------#

    coord=[67,79] #massena l1
    coord1=[160,60] #republique l1
    coord2=[100,199] #
    coord3=[152,230] #lacasagne l4
    #------------------------------------------------------------------#


    #def AstarAlgorithm(stationList, coord_origin, coord_destination, typePreference,city,flag_redundants):
    origen = coord
    desti = coord3
    print "origen: " + str(coord2station(origen,stationList)) + "+1 desti:" + str(coord2station(desti,stationList)) + "+1 == " + str(AstarAlgorithm(stationList, origen, desti, 4, city, 0))
    #print "origen: " + str(coord2station(coord,stationList)) + "+1 desti:" + str(coord2station(coord2,stationList)) + "+1 == " + str(AstarAlgorithm(stationList, coord, coord2, 1, city, 0))


if __name__ == '__main__':
    main()