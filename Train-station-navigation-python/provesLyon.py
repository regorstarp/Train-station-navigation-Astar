from SearchAlgorithm import *
from SubwayMap import *

def main():

    #------------------------------------------------------------------#
    #read file
    filename='Stations_Final.txt'
    stationList=readStationInformation(filename)
    #read adjacency matrix
    filename='Connections_Final.txt'
    adjacency=readCostTable(filename)

    #Real TIME cost table
    filename = 'CompletLyon_Final_Time.txt'
    timeStations = readCostTable(filename)
    setNextStations(stationList, timeStations)

    # CITY information
    # velocity
    filename = "CompletLyon_Final_InfoVelocity.txt"
    infoVelocity = readInformation(filename)
    # Transfers times
    filename = "CompletLyon_Final_InfoTransfers.txt"
    infoTransfers = readInformation(filename)
    multipleStations = {}
    city=CityInfo(len(infoVelocity),infoVelocity,infoTransfers,adjacency, multipleStations)

    #------------------------------------------------------------------#

    coord=[100,150] #gare de vaise verd
    coord1=[300,50] #cuice groc
    coord2=[211,392] #place jean jaures blau
    coord3=[293,455] #lacasagne l4

    #------------------------------------------------------------------#


    #def AstarAlgorithm(stationList, coord_origin, coord_destination, typePreference,city,flag_redundants):
    origen = coord2
    desti = coord3
    Origen = coord2station(origen,stationList)
    Desti = coord2station(desti,stationList)
    estacioOrigen = []
    estacioDesti = []
    for ele in Origen:
        estacioOrigen.append(stationList[ele].id)
    for ele in Desti:
        estacioDesti.append(stationList[ele].id)
    print "origen: " + str(estacioOrigen) + " desti:" + str(estacioDesti)+ "\n" + str(AstarAlgorithm(stationList, origen, desti, 1, city, 1)) + "\n" 
    print "origen: " + str(estacioOrigen) + " desti:" + str(estacioDesti)+ "\n" + str(AstarAlgorithm(stationList, origen, desti, 2, city, 1)) + "\n"
    print "origen: " + str(estacioOrigen) + " desti:" + str(estacioDesti)+ "\n" + str(AstarAlgorithm(stationList, origen, desti, 3, city, 1)) + "\n"
    print "origen: " + str(estacioOrigen) + " desti:" + str(estacioDesti)+ "\n" + str(AstarAlgorithm(stationList, origen, desti, 4, city, 1)) + "\n"


if __name__=='__main__':
    main()




