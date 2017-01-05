Tilemap = [[6,1,3,4],[0,2,11,10],[5,8,7,9],[14,12,15,13]]
dummyMap = [[2,0,3,4],[1,5,7,8],[9,6,10,11],[13,14,15,12]]

import queue
import copy
import sys
sys.setrecursionlimit(10**8)
minimumdepth = 10
overlaplist = list()
overlaplistdepth = list()
movecount = 0
#경로
route = list()
def findroute(node):
    route.clear()
    while node != None:
        route.append(node.Tilemap)
        node = node.SuperNode
    route.reverse()
    
    print(route)

def manhattan(map_):
    if map_ == None:
        return 9999999
    puzzle = list()
    for i in range(16):
        puzzle.append(map_[i//4][i%4])
    md = 0
    for i in range(16):
        row1 = i // 4
        col1 = i % 4
        if puzzle[i] != 0:
            row2 = (puzzle[i]-1) // 4
            col2 = (puzzle[i]-1) % 4
        else:
            row2 = 3
            col2 = 3
        md += (abs(row1-row2) + abs(col1-col2))

    return md


class Tree:
    #SubNode1#right
    #SubNode2#left
    #SubNode3#down
    #SubNode4#up
   # SuperNode
   # Tilemap
   # depth
    depth = 0
    def AddSubNode(self):
        r = moveTilemap(copy.deepcopy(self.Tilemap),"RIGHT")
        mr = manhattan(r)
        
        l = moveTilemap(copy.deepcopy(self.Tilemap),"LEFT")
        ml = manhattan(l)
        
        d = moveTilemap(copy.deepcopy(self.Tilemap),"DOWN")
        md = manhattan(d)
        
        u = moveTilemap(copy.deepcopy(self.Tilemap),"UP")
        mu = manhattan(u)

        manhlist = list()
        manhlist.append(mr)
        manhlist.append(md)
        manhlist.append(ml)
        manhlist.append(mu)
        maplist = list()
        maplist.append(r)
        maplist.append(d)
        maplist.append(l)
        maplist.append(u)

       
          
        for i in range(4):
            for j in range(i,4):
                if manhlist[i] > manhlist[j]:
                    temp1 = manhlist[i]
                    temp2 = maplist[i]
                    manhlist[i] = manhlist[j]
                    maplist[i] = maplist[j]
                    manhlist[j] = temp1
                    maplist[j] = temp2
        
        
        self.SubNode1 = Tree(self,maplist[0])
        self.SubNode2 = Tree(self,maplist[1])

        
        self.SubNode3 = Tree(self,maplist[2])
        #self.SubNode4 = Tree(self,maplist[3])
        
    #def saveroute(self):
     #   here
    def __init__(self,Super,Tilemap_):
        global minimumdepth
        global overlaplist
        self.Tilemap = copy.deepcopy(Tilemap_)
        if self.Tilemap is not None:
            pass#print(self.Tilemap)
        self.SuperNode = Super
        if Super != None:
            self.depth = Super.depth + 1
        if checkTilemap(self.Tilemap) != False:
            if minimumdepth >= self.depth:
                minimumdepth = self.depth
            findroute(self)
            self.Tilemap = None
        
        #print(self.depth)
        if self.depth > minimumdepth:
            self.Tilemap = None
            
        if self.Tilemap != None:
            if overlaplist.count(self.Tilemap) != 0:
                ind = overlaplist.index(self.Tilemap)
                if overlaplistdepth[ind] > self.depth:
                    overlaplistdepth[ind] = self.depth
                else:
                    self.Tilemap = None
            else:
                overlaplist.append(self.Tilemap)
                overlaplistdepth.append(self.depth)

                
                
        if self.Tilemap != None:
            self.AddSubNode()
        

def checkTilemap(Tilemap_):
    if Tilemap_ is None:
        return False
    if Tilemap_[0][0] == 0:
        start = 2
        end = 16
    elif Tilemap_[3][3] == 0:
        start = 1
        end = 15
    else:
        return False
    
    for x in range(start,end):
        y=x-1
        prevtile = Tilemap_[y//4][y%4]
        tile = Tilemap_[x//4][x%4]
        if tile - prevtile != 1:
            return False
    print("done")
    #input()
    return True



def moveTilemap(Tilemap_,dirc):
    global movecount
    movecount+=1
    Tilemap = copy.deepcopy(Tilemap_)
    for x in range(16):
        if Tilemap_[x//4][x%4] == 0:
            zerotile = [x//4,x%4]
    if dirc == "RIGHT":#
        if zerotile[1]+1>3:
            return None
        else:
            Tilemap[zerotile[0]][zerotile[1]] = Tilemap_[zerotile[0]][zerotile[1]+1]
            Tilemap[zerotile[0]][zerotile[1]+1] = 0
    if dirc == "LEFT":
        if zerotile[1]-1<0:
            return None
        else:
            Tilemap[zerotile[0]][zerotile[1]] = Tilemap_[zerotile[0]][zerotile[1]-1]
            Tilemap[zerotile[0]][zerotile[1]-1] = 0
    if dirc == "DOWN":
        if zerotile[0]+1>3:
            return None
        else:
            Tilemap[zerotile[0]][zerotile[1]] = Tilemap_[zerotile[0]+1][zerotile[1]]
            Tilemap[zerotile[0]+1][zerotile[1]] = 0
    if dirc == "UP":#
        if zerotile[0]-1<0:
            return None
        else:
            Tilemap[zerotile[0]][zerotile[1]] = Tilemap_[zerotile[0]-1][zerotile[1]]
            Tilemap[zerotile[0]-1][zerotile[1]] = 0
    
    return copy.deepcopy(Tilemap)
#print(dummyMap)
#print(moveTilemap(dummyMap,"LEFT"))

d = [[1,6,2,4],[5,10,3,7],[9,0,15,8],[13,14,12,11]]
tree = Tree(None,d)
print(movecount)

