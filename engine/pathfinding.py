import copy
import math
import pygame
import time

class Pathfinder:

    def __init__(self, mapObject, unit, window):
        self.currentMap = mapObject
        self.unit = unit
        self.window = window

        self.variables = dict(
            visitedList = [],
            pathFinderPoints = [],
            pathPoint = 0,
            pathEnd = True,
            pathPoints = []
        )

    def calculatePath(self, window, x, y):
        self.variables['pathPoint'] = 0
        self.variables['pathFinderPoints'] = self.findPath(window, self.unit.physics['x'] + 32, self.unit.physics['y'] + 48, int(x / 32)*32, int(y / 32 + 0.5)*32, self.currentMap.tiles['blocked'])
        self.variables['pathEnd'] = False

    def resetPathFinder(self):
        self.variables['pathPoints'] = []
        self.variables['pathPoint'] = 0
        self.variables['pathEnd'] = True

    def pathMoveStep(self, window):

        #if point is players current tile position do not move player back to that tile center

        if ( ( int( self.variables['pathFinderPoints'][0][0] / 32 + 0.5 ) != int( self.unit.physics['x'] / 32 - 16.5 ) ) and ( int( self.variables['pathFinderPoints'][0][1] / 32 + 0.5 ) != int( self.unit.physics['y'] / 32 + 36.5 ) ) ) and ( self.variables['pathPoint'] != 0 ):

            if self.variables['pathFinderPoints'][self.variables['pathPoint']][0] - 16 < self.unit.physics['x']:
                self.unit.moveLeft(window)

            elif self.variables['pathFinderPoints'][self.variables['pathPoint']][0] - (16 + self.unit.physics['speed']) > self.unit.physics['x']:
                self.unit.moveRight(window)

            elif self.variables['pathFinderPoints'][self.variables['pathPoint']][1] - 36 < self.unit.physics['y']:
                self.unit.moveUp(window)

            elif self.variables['pathFinderPoints'][self.variables['pathPoint']][1] - (36 + self.unit.physics['speed']) > self.unit.physics['y']:
                self.unit.moveDown(window)

            else:
                
                #center X and Y to tile when tile is reached

                self.unit.physics['x'] = self.variables['pathFinderPoints'][self.variables['pathPoint']][0] - 16
                self.unit.physics['y'] = self.variables['pathFinderPoints'][self.variables['pathPoint']][1] - 36

                self.unit.drawPlayer(window, 0) #draw when changing point to stop flicker

                self.variables['pathPoint'] += 1
            
                if(self.variables['pathPoint'] > len(self.variables['pathFinderPoints']) - 1):
                    self.variables['pathPoint'] = 0
                    self.variables['pathEnd'] = True
        else:
            
            #move past start point

            self.variables['pathPoint'] += 1

            self.unit.drawPlayer(window, 0) #draw when changing point to stop flicker

            if(self.variables['pathPoint'] > len(self.variables['pathFinderPoints']) - 1):
                self.variables['pathPoint'] = 0
                self.variables['pathEnd'] = True

    def checkPathEnd(self):
        return self.variables['pathEnd']

    def estimateBestPath(self, x2, y2, paths):
        PathElement=0
        CurrentDif=0
        OldDif=0

        OldDif=math.sqrt((math.pow((x2-paths[0][len(paths[0])-1][0]),2)+math.pow((y2-paths[0][len(paths[0])-1][1]),2)))

        for i in range(1,len(paths)):
            CurrentDif=math.sqrt((math.pow((x2-paths[i][len(paths[i])-1][0]),2)+math.pow((y2-paths[i][len(paths[i])-1][1]),2)))

            if(CurrentDif<OldDif):
                    PathElement=i
                    OldDif=CurrentDif

        if(not PathElement==0):
            c=copy.copy(paths[0])
            paths[0]=paths[PathElement]
            paths[PathElement]=c

        return(paths )

    def notVisited(self, x1, y1):
        for i1 in reversed(self.variables['visitedList']):
            if(i1[0]==x1 and i1[1]==y1):
                return(False)
        return(True)

    def getMoves(self, x1, y1):
        
        MoveList = []

        YMove = 32
        XMove = 32
        
        if(not y1 <= 0):
            if(not self.currentMap.isTileBlocked(x1, (y1 - YMove)) and self.notVisited(x1, (y1 - YMove))):
                self.variables['visitedList'].append([x1, (y1 - YMove)])
                MoveList.append([x1, (y1 - YMove)])

        if((y1 + YMove) < self.currentMap.properties['height']):
            if(not self.currentMap.isTileBlocked(x1, (y1 + YMove)) and self.notVisited(x1, (y1 + YMove))):
                self.variables['visitedList'].append([x1, (y1 + YMove)])
                MoveList.append([x1, (y1 + YMove)])

        if(not x1 <= 0):
            if(not self.currentMap.isTileBlocked((x1 - XMove), y1) and self.notVisited((x1 - XMove), y1)):
                self.variables['visitedList'].append([(x1 - XMove), y1])
                MoveList.append([(x1 - XMove), y1])

        if((x1 + XMove) < self.currentMap.properties['width']):
            if(not self.currentMap.isTileBlocked((x1 + XMove), y1) and self.notVisited((x1 + XMove), y1 )):
                self.variables['visitedList'].append([(x1 + XMove), y1])
                MoveList.append([(x1 + XMove), y1])

        #return the moves that can be made from current path

        return(MoveList)


    def findPath(self, window, x1, y1, x2, y2, BlkTiles):

        IsPaths=True

        x1=int(x1/32+0.5)*32
        y1=int(y1/32+0.5)*32
        x2=int(x2/32+0.5)*32
        y2=int(y2/32+0.5)*32

        self.variables['visitedList'] = [[x1, y1]]
        PathList=[ [ [x1, y1 ] ] ]

        #check if start is block tile

        if(self.currentMap.isTileBlocked(x1+32, y1+48)):
           return(PathList[0])

        #check if end is block tile
        
        if(self.currentMap.isTileBlocked(x2 + 32, y2 + 48)):
           return(PathList[0])

        while PathList:
            
            x = PathList[0][len(PathList[0]) - 1][0]
            y = PathList[0][len(PathList[0]) - 1][1]

            #if path reached goal return path points to goal
            if ((x == x2) and (y == y2)):
                return(PathList[0])
            
            m = self.getMoves(x, y)
            
            for i in m:
                c = copy.copy(PathList[0])
                c.append(i)
                c = copy.copy(c)
                PathList.append(c)
            PathList.pop(0)
            
            #rearrange paths for performance
            if PathList:
                PathList = self.estimateBestPath(x2, y2, PathList)

        #if no path to destination send back start point
        return([[x1, y1]])
        
