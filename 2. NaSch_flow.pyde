#LIBRARIES
from random import uniform, randint

#ENTRY VALUES
flow = 900 #veic per hour
L = 300 #number of cells 
T = 300 #number of seconds for the simulation
DENSITY = 0.40 #how many cars
vmax = 6 #maximum car speed 
vmax_tk = 5 #maximum truck speed 
p = 0.6 #probability of random stop
t = 0 #current time step ~ 1 s

#STARTING VALUES
veicList = []
posList = []
leader = 0
carNum = int(DENSITY*L)
entry_flow = flow/3600

#LIBRARIES
from random import uniform, randint

#ENTRY VALUES
flow = 900 #veic per hour
L = 300 #number of cells 
T = 300 #number of seconds for the simulation
DENSITY = 0.40 #how many cars
vmax_car = 6 #maximum car speed 
vmax_tk = 5 #maximum truck speed 
p = 0.6 #probability of random stop
t = 0 #current time step ~ 1 s

#STARTING VALUES
veicList = []
posList = []
leader = 0
carNum = int(DENSITY*L)
entry_flow = flow/3600

class Car:
    def __init__(self,id,v,x):
        self.col = color(random(255),random(140),random(255))
        self.id = id
        self.v = v
        self.x = x
        
    #REGULAR DISPLAY   
    def display(self):
        fill(self.col)
        rect(SZ*self.x,SZ*(t+6),SZ,SZ)
       
    #ALTERNATIVE DISPLAY     
    def alt_display(self):    
        for i in range(5):
            fill(self.col)
            rect(SZ*self.x,SZ*i,SZ,SZ)
    
    def update(self):
#STEP 1: acceleration 
# All cars that have not already reached the maximal velocity vmax acceleration by one unit: v -> v+1         
        if self.v < vmax:
            self.v += 1        
        
#STEP 2: safety distance
#If a car has d empty cells in front of it and is its velocity v (after step 1) larger then d, then it reduces the velocity to d: v -> min{d,v}        
        d = safe_dist(self.id)
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
            veicList.remove(self)

def safe_dist(id):
    posList = []
    n = len(veicList)
    leader = veicList[n-1].id
    pos = (n-1)+leader-id
        
#CASE 1: CAR IS LEADING.
    if id == leader:
        d = vmax

#CASE 2: CAR IS FOLLOWING.
    else:
        d = veicList[pos+1].x - veicList[pos].x - 1
    
    return d
          
                                                      
def setup():
    global L,vmax,SZ,carNum,posList,veicList
    size(600,600)
    noStroke()
    background(255)
    frameRate(12)
    SZ = width/L

    #DEFINE UNIQUE POSITIONS
    posList = []
    i = 0
    while i < carNum:
        position = randint(0,L)
        if position not in posList: 
            posList.append(position)
            i += 1
    posList = sorted(posList)
    
    #PLACING CARS IN DECRECENT ID ORDER (car "0" is always the first to lead)
    # { ... >(id_4)> ... >(id_3)> ... >(id_2)> ... >(id_1)> ... >(id_0)> ... }
    
    i = 0
    while i < carNum:
        veicList.append(Car(carNum-1-i,randint(0,vmax),posList[i]))
        i += 1
                
        
def draw():
    global T,t,SZ,posList,veicList,leader

#SET ENTRY FLOW
    if t%4 == 0:
        newcar = [Car(veicList[0].id+1,0,0)]
        i=0
        while i < len(veicList):
            newcar.append(veicList[i])
            i+=1
        veicList = newcar

#UPDATE POSITIONS
    i = 0
    while i < len(veicList):
        veicList[len(veicList)-1-i].update()
        i += 1

#DISPLAY CURRENT TIME STEP
    posList=[]
    i=0
    while i < len(veicList):
         veicList[i].display()
         veicList[i].alt_display()
         posList.append(veicList[i].x)
         i += 1

#CLEAN ALTERNATIVE DISPLAY
    for l in range(L):
        if l not in posList:
            for j in range(5):
                rect(SZ*l,SZ*j,SZ,SZ)
                fill(255)


#next time step
    if t < T:
        t += 1
