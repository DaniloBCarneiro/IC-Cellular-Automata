from random import uniform, randint

flow = 900 #veic per hour
L = 300 #number of cells 
T = 300 #number of seconds for the simulation
DENSITY = 0.40 #how many cars
vmax = 5 #maximum speed 
p = 0.6 #probability of random stop
t = 0 #current time step

carList = []
timeMatrix = []
carNum = int(DENSITY*L)

class Car:
    def __init__(self,id,v,x):
        self.col = color(random(255),random(140),random(255))
        self.id = id
        self.v = v
        self.x = x
       
    def display(self):
        fill(self.col)
        rect(SZ*self.x,SZ*(t+6),SZ,SZ)
        
    def alt_display(self):    
        for i in range(5):
            fill(self.col)
            rect(SZ*self.x,SZ*i,SZ,SZ)
    
    def update(self):
#Step 1: acceleration 
# All cars that have not already reached the maximal velocity vmax acceleration by one unit: v -> v+1         
        if self.v < vmax:
            self.v += 1        
        
#Step 2: safety distance
#If a car has d empty cells in front of it and is its velocity v (after step 1) larger then d, then it reduces the velocity to d: v -> min{d,v}        
        d = checkFront(self.id)
        if d < self.v:
            self.v = d
            
#Step 3: randomization
# With probability p, the velocity is reduced by one unit (if v after step 2):v -> v-1
        if self.v > 0:
            if uniform(0,1) < p:
                self.v -= 1
        elif self.v < 0:
            self.v = 0
                
#Step 4: driving
#After steps 1-3 the new velocity vn for each car n has been determined forward by vn cells: xn -> xn+vn.
        self.x += self.v
        if self.x > (L-1):
            self.x -= (L-1)
   
def checkFront(id):
    #check front
    if id == (carNum-1):
        d = carList[0].x - carList[id].x - 1
    else: 
        d = carList[id+1].x - carList[id].x - 1
    
    #round map
    if d < 0:
        if id == (carNum-1):
            d = carList[0].x - carList[id].x + (L-1) - 1
        else: 
            d = carList[id+1].x - carList[id].x + (L-1) - 1
    return d                    
                                                      
def setup():
    global carList,L,vmax,carNum,SZ
    size(600,600)
    noStroke()
    background(255)
    frameRate(12)
    SZ = width/L
    
    #define unique positions
    posList = []
    i = 0
    while i < carNum:
        position = randint(0,L)
        if position not in posList: 
            posList.append(position)
            i += 1
    
    #organize positions
    posList = sorted(posList)
        
    #place cars
    for i in range(carNum):
        carList.append(Car(i,randint(0,vmax),posList[i]))
        
def draw():
    global T,t,SZ

    for car in range(carNum):
         carList[car].display()
        
#update cars
    posList=[]
    for car in range(carNum):
        carList[carNum-1-car].update()
        posList.append(carList[carNum-1-car].x)

#clean alternative display
    for i in range(L):
        if i not in posList:
            for j in range(5):
                rect(SZ*i,SZ*j,SZ,SZ)
                fill(255)

#set alternative display
    for car in range(carNum):
        carList[car].alt_display()

#next time step
    if t < T:
        t += 1
