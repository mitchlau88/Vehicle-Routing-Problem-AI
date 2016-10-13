import random
from MapV3 import *

vehicleNum = 2;
capability = 2;
count =0;
loopNum = 100;
popSize = 5;
mutationPosPer = 5;
solutionSet = [popSize];
# the syntax of the statement below should be fine but the compiler states "undefined variable"
bestSolution = Solution(numPackage);

for sol in solutionSet:
    for package in range(0, numPackage-1):
        sol.arrangement[package]=random(0,vehicleNum-1);

def loop():
       
    isEnd = 0;
    while isEnd == 0:
        # evaluation:
        # evaluate each generation:
        for item in solutionSet():
            item.updateSumPathLength(numPackage,capability,w.nodes(),shortestPathGraph);
            sorted(solutionSet, key=lambda solution: solution[0]);
        # save the best solution:
        if bestSolution.sumPathLength < 0:
            bestSolution = solutionSet[0];
        else:
            if bestSolution.sumPathLength > solutionSet[0].sumPathLength:
                if solutionSet[0].sumPathLength >= 0:
                    bestSolution = solutionSet[0];
        
        # termination:
        # isEnd? T->terminate the loop, F-> continue the loop
        if count < loopNum:
            count = count + 1;
            newSolutionSet = [popSize];
            # selection
            # crossover & mutation
            for s in newSolutionSet:
                s = Solution(numPackage);
                # selection
                parent1 = random(0,popSize/2 -1);
                parent2 = random(0,popSize/2 -1);
                    
                #crossover
                crossPoint = random(0,numPackage-1)
                for vehicle in range(0,s.numPackage-1):
                    if vehicle < crossPoint:
                        s.arrangement[vehicle] = solutionSet[parent1].arrangement[vehicle];
                    else:
                        s.arrangement[vehicle] = solutionSet[parent2].arrangement[vehicle];
                        
                    # mutation
                    if randomTrue(mutationPosPer):
                        s.arrangement[vehicle] = random(0,vehicleNum-1);
                
            #elimate old generation except the saved best solution
            solutionSet = newSolutionSet;
        else:
            isEnd = 1;
    return

def randomTrue(percentage):
    return random.randrange(1,100,1) <= percentage

def getDistance(source, distination, locationList, matrix):
    sourceSerial = -1;
    distinationSerial = -1;
    for location in range(0,locationList.length-1):
        if locationList(location) == source:
            sourceSerial = location;
        if locationList(location) == distination:
            distinationSerial = location;
    return matrix[sourceSerial,distinationSerial];
class Solution:
    def __init__(self,packageNumber):
        self.sumPathLength = -1;
        self.arrangement = [packageNumber];
        return
    
    def updateSumPathLength(self, numVehicle, capability, locationList, matrix):
        vehicles = [[] for vehicle in range(numVehicle)];
        
        # send all packages into their own vehicles
        for pack in range(0,numPackage-1):
            vehicles[self.arrangement[pack]].append_child(pack);
        self.sumPathLength=0;
        
        #greedy search: closet valuable location first
        for vehicle in range(0,numVehicle-1):
            valuableLocations = [];
            path =[];
            path.append(garage);
            for pack in vehicles[vehicle]:
                valuableLocations.append(pack.source);
            pathPointer=0;
            vehiclePathLength=0;
            carriedPacks = [];
            while valuableLocations:
                nextLocation = -1;
                # greedy search for the next closest valuable location
                if carriedPacks.length < capability:
                    # if they have package left, find the closest valuable location, then add the distance between the location and current position into the pathlength
                    for location in range(valuableLocations.length-1):
                        if nextLocation == -1:
                            nextLocation = location;
                        else:
                            if getDistance(path[pathPointer], valuableLocations[nextLocation], locationList, matrix) > getDistance(path[pathPointer], valuableLocations[location], locationList, matrix):
                                nextLocation = location;
                else:
                    # since the vehicle is full, search the closet valuable location from carried packages
                    for location in range(valuableLocations.length-1):
                        for destination in range(carriedPacks.length-1):
                            if carriedPacks[destination].destination == valuableLocations[location]:
                                    if nextLocation == -1:
                                        nextLocation = location;
                                    else:
                                        if getDistance(path[pathPointer], valuableLocations[nextLocation], locationList, matrix) > getDistance(path[pathPointer], valuableLocations[location], locationList, matrix):
                                            nextLocation = location;
                # move to the found location
                path.append(valuableLocations[nextLocation]);
                vehiclePathLength = vehiclePathLength + getDistance(path[pathPointer], valuableLocations[nextLocation], locationList, matrix);
                pathPointer = pathPointer +1;
                
                # remove all carried packages which has reach their desination
                # remove all destination of carried packages
                for pack in vehicles[vehicle]:
                    for carriedPack in carriedPacks:
                        if carriedPack.destination == path[pathPointer]:
                            if pack.desintation == carriedPack.destination:
                                valuableLocations.remove(carriedPack.destination);
                                carriedPacks.remove(carriedPack);
                                vehicles[vehicle].remove(pack);
                # carry all packages which have not been carried and the current 
                for pack in vehicles[vehicle]:
                    if pack.source == path[pathPointer]:
                        hasCarried = 0;
                        for carriedPack in carriedPacks:
                            if pack.source == carriedPack.source:
                                hasCarried = 1;
                        if hasCarried == 0:
                            if carriedPacks.length < capability:
                                valuableLocations.append(pack.desintation);
                                carriedPacks.append(pack);
                # next iteration or end of the loop
            vehiclePathLength = vehiclePathLength + getDistance(path[pathPointer], garage, locationList, matrix);
            path.append(garage);
            self.sumPathLength = self.sumPathLength + vehiclePathLength; 
        return
    
    def outputSolution(self, numVehicle, capability, locationList, matrix):
        vehicles = [[] for vehicle in range(numVehicle)];
        print "Package Arrangement: " + self.arrangement;
        for pack in range(0,numPackage-1):
            print pack;
            vehicles[self.arrangement[pack]].append_child(pack);
        self.sumPathLength=0;
        
        #greedy search: closet valuable location first
        for vehicle in range(0,numVehicle-1):
            valuableLocations = [];
            path =[];
            path.append(garage);
            for pack in vehicles[vehicle]:
                valuableLocations.append(pack.source);
            pathPointer=0;
            vehiclePathLength=0;
            carriedPacks = [];
            while valuableLocations:
                nextLocation = -1;
                # greedy search for the next closest valuable location
                if carriedPacks.length < capability:
                    # if they have package left, find the closest valuable location, then add the distance between the location and current position into the pathlength
                    for location in range(valuableLocations.length-1):
                        if nextLocation == -1:
                            nextLocation = location;
                        else:
                            if getDistance(path[pathPointer], valuableLocations[nextLocation], locationList, matrix) > getDistance(path[pathPointer], valuableLocations[location], locationList, matrix):
                                nextLocation = location;
                else:
                    # since the vehicle is full, search the closet valuable location from carried packages
                    for location in range(valuableLocations.length-1):
                        for destination in range(carriedPacks.length-1):
                            if carriedPacks[destination].destination == valuableLocations[location]:
                                    if nextLocation == -1:
                                        nextLocation = location;
                                    else:
                                        if getDistance(path[pathPointer], valuableLocations[nextLocation], locationList, matrix) > getDistance(path[pathPointer], valuableLocations[location], locationList, matrix):
                                            nextLocation = location;
                # move to the found location
                path.append(valuableLocations[nextLocation]);
                vehiclePathLength = vehiclePathLength + getDistance(path[pathPointer], valuableLocations[nextLocation], locationList, matrix);
                pathPointer = pathPointer +1;
                
                # remove all carried packages which has reach their desination
                # remove all destination of carried packages
                for pack in vehicles[vehicle]:
                    for carriedPack in carriedPacks:
                        if carriedPack.destination == path[pathPointer]:
                            if pack.desintation == carriedPack.destination:
                                valuableLocations.remove(carriedPack.destination);
                                carriedPacks.remove(carriedPack);
                                vehicles[vehicle].remove(pack);
                # carry all packages which have not been carried and the current 
                for pack in vehicles[vehicle]:
                    if pack.source == path[pathPointer]:
                        hasCarried = 0;
                        for carriedPack in carriedPacks:
                            if pack.source == carriedPack.source:
                                hasCarried = 1;
                        if hasCarried == 0:
                            if carriedPacks.length < capability:
                                valuableLocations.append(pack.desintation);
                                carriedPacks.append(pack);
                # next iteration or end of the loop
            vehiclePathLength = vehiclePathLength + getDistance(path[pathPointer], garage, locationList, matrix);
            path.append(garage);
            self.sumPathLength = self.sumPathLength + vehiclePathLength;
            print "Vehicle " + vehicle + ": Path: " + path + " the Sum of all Paths Length: " + self.sumPathLength; 
        return
