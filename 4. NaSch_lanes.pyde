#LIBRARIES
from random import uniform, randint

#ENTRY VALUES
flowList = [900,900,900,900,900,900,900,900,900,900,900,900] #entry flow in each lane [lane 1, lane 2, lane 3...] in veic/hour
L = 300 #number of cells 
T = 300 #number of seconds for the simulation
DENSITY = 0.20 #how many cars
vmax = 6 #maximum car speed 
p = 0.6 #probability of random stop
t = 0 #current time step ~ 1 s
tp = 0.5 #truck/total ratio
n_lanes = 2 #number of n_lanes in each direction
display_lane = 0 #lane for the space-time diagram
leader = 0
veicNum = int(DENSITY*L)

#LISTS
posMatrix = []
entry_count = []
veicList = []
        
class Veic:
    def __init__(self,ln,id,ty,v,x):
        self.col = color(random(255),random(140),random(255))
        self.type = ty # 0 = car, 1 = truck
        self.id = id
        self.v = v
        self.x = x
        self.lane = ln
        
        # if self.lane < n_lanes:
        #     self.col = color(random(255),random(140),random(255))
        # else:
        #     self.col = color(150,120,255)
        
    #SPACE-TIME DIAGRAM
    def display(self):
        if self.lane == display_lane:   
            fill(self.col)
            rect(SZ*self.x,SZ*(t+8*n_lanes),SZ,SZ)
            if self.type == 1:
                rect(SZ*(self.x+1),SZ*(t+8*n_lanes),SZ,SZ)
       
    #UPPER DISPLAY    
    def up_display(self):    
        fill(self.col)
        
        #LEFT TO RIGHT LANES ->
        if self.lane < n_lanes:
            rect(SZ*self.x,SZ*(1+4*self.lane),SZ,SZ)
            rect(SZ*self.x,SZ*(2+4*self.lane),SZ,SZ)
            if self.type == 1:
                rect(SZ*(self.x+1),SZ*(1+4*self.lane),SZ,SZ)
                rect(SZ*(self.x+1),SZ*(2+4*self.lane),SZ,SZ)
    
        #RIGHT TO LEFT LANES <-
        else:
            rect(SZ*(L-1-self.x),SZ*(1+4*self.lane),SZ,SZ)
            rect(SZ*(L-1-self.x),SZ*(2+4*self.lane),SZ,SZ)
            if self.type == 1:
                rect(SZ*(L-2-self.x),SZ*(1+4*self.lane),SZ,SZ)
                rect(SZ*(L-2-self.x),SZ*(2+4*self.lane),SZ,SZ)    
     
    def update(self):
#STEP 1: acceleration 
# All cars that have not already reached the maximal velocity vmax acceleration by one unit: v -> v+1         
        if self.v < vmax-self.type:
            self.v += 1        
        
#STEP 2: safety distance
#If a car has d empty cells in front of it and is its velocity v (after step 1) larger then d, then it reduces the velocity to d: v -> min{d,v}        
        d = safe_dist(self.lane,self.id)-self.type
        if d < self.v:
            self.v = d
            
#STEP 3: randomization
# With probability p, the velocity is reduced by one unit (if v after step 2):v -> v-1
        if self.v > 0:
            if uniform(0,1) < p:
                self.v -= 1
        elif self.v < 0:
            self.v = 0
                
#STEP 4: driving
#After steps 1-3 the new velocity vn for each car n has been determined forward by vn cells: xn -> xn+vn.
        self.x += self.v
        
#STEP 5: leaving
        if self.x > (L-1):
            veicList[self.lane].remove(self)


#CHECK SAFE DISTANCE AHEAD

def safe_dist(ln,id):
    posMatrix = []
    n = len(veicList[ln])
    leader = veicList[ln][n-1].id
    pos = (n-1)+leader-id
        
#CASE 1: CAR IS LEADING.
    if id == leader:
        d = vmax

#CASE 2: CAR IS FOLLOWING.
    else:
        d = veicList[ln][pos+1].x - veicList[ln][pos].x - 1
    return d
          
                                                      
def setup():
    global L,vmax,SZ,veicNum,posMatrix,veicList, cars_in_the_system, entry_count
    size(600,600)
    noStroke()
    background(255)
    frameRate(10)
    SZ = width/L
    
    
    #CREATE A NUMBER OF ROWS EQUAL TO THE NUMBER OF LANES
    for lane in range(2*n_lanes):
        veicList.append([])
        posMatrix.append([])
        entry_count.append(0)
    
    
    #INSERTS A NUMBER OF CARS EQUAL veicNum INTO THE SYSTEM WITH PROPER LANE, TYPE, SPEED AND POSITION 
    lane = 0 #starting lane
    while lane < 2*n_lanes:
        
        #DEFINE UNIQUE POSITIONS
        i = 0
        while i < veicNum:
            position = randint(0,L)
            if position not in posMatrix[lane]: 
                posMatrix[lane].append(position)
                i += 1
        posMatrix[lane] = sorted(posMatrix[lane])
        
        #PLACE CARS IN DECRECENT ID ORDER (car "0" is always the first to lead)
        # { ... >(id_4)> ... >(id_3)> ... >(id_2)> ... >(id_1)> ... >(id_0)> ... }
        
        i = 0
        while i < veicNum:
            ty = 0
            if uniform(0,1) < tp:
                ty = 1
            veicList[lane].append(Veic(lane,veicNum-1-i,ty,randint(0,vmax),posMatrix[lane][i]))
            i += 1
        lane += 1   
     
        
        
def draw():
    global T,tp,t,SZ,posMatrix,veicList,leader, entry_count, n_lanes

    lane = 0
    while lane < 2*n_lanes:
    
    #SET ENTRY FLOW
        if (t*flowList[lane]/3600-entry_count[lane]) > 1 and veicList[lane][0].x > 0:
            ty = 0
            if uniform(0,1) < tp:
                ty = 1
            new_veicList = [Veic(lane,veicList[lane][0].id+1,ty,0,0)]
            
            i=0
            while i < len(veicList[lane]):
                new_veicList.append(veicList[lane][i])
                i+=1
                
            veicList[lane] = new_veicList
            entry_count[lane] += 1
    
    #UPDATE POSITIONS
        i = 0
        n = len(veicList[lane])
        while i < n:
            veicList[lane][n-1-i].update()
            i += 1
    
    #DISPLAY CURRENT TIME STEP
        posList = []
        i=0
        while i < len(veicList[lane]):
            veicList[lane][i].display()
            veicList[lane][i].up_display()
            posList.append(veicList[lane][i].x)
            if veicList[lane][i].type == 1:
                posList.append(veicList[lane][i].x+1)
            i += 1
        posMatrix[lane] = posList
            
    #SAVE CURRENT TIME STEP
    #in progress

    #CLEAN UPPER DISPLAY
        if lane < n_lanes:
            #LEFT TO RIGHT n_lanes ->
            for l in range(L):
                if l not in posMatrix[lane]:
                    for j in range(4):
                        rect(SZ*l,SZ*(j+4*lane),SZ,SZ)
                        fill(255)
        else:
            #RIGHT TO LEFT n_lanes <-
            for l in range(L):
                if l not in posMatrix[lane]:
                    for j in range(4):
                        rect(SZ*(L-1-l),SZ*(j+4*lane),SZ,SZ)
                        fill(255)
        lane += 1
            
#NEXT TIME STEP
    if t < T:
        t += 1
