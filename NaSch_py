#LIBRARIES
from random import uniform, randint

#STANDARD
flowList = [900,900,900,900,900,900,900,900,900,900,900,900] #entry flow in each lane [lane 1, lane 2, lane 3...] in veic/hour
L = 300 #number of cells 
T = 10 #number of seconds for the simulation
DENSITY = 0.20 #how many cars
vmax = 6 #maximum car speed 
p = 0.6 #probability of random stop
t = 0 #current time step ~ 1 s
tp = 0.5 #truck/total ratio
n_lanes = 1 #number of n_lanes in each direction
display_lane = 0 #lane for the space-time diagram
leader = 0 #set first leader
veicNum = int(DENSITY*L)


#INPUT VALUES
file_name = input('File name: ')
#T = int(input('Period of simulation (T): '))
#p = float(input('Probability of random stop (range 0-1): '))
#tp = float(input('Percentage of trucks (range 0-1): '))
#L = round(float(input('Lenght of the simulation in km (L): '))/7.5,0) #NEED TO ROUND UP THE L VALUE
#n_lanes = int(input('Number of lanes in each direction: '))
#vmax = round((float(input('Maximum car speed in km/h (vmax): '))/(3.6*7.5)),0)
#DENSITY = float(input('Initial car density (if you wish to start with an empty road, type 0): '))
#flowList = []
#lane = 0
#for lane in range(2*n_lanes):
#    print('Flow in lane ',lane,': ')
#    x = int(input())
#    flowList.append(x)
#display_lane = int(input('Which lane should be displayed in time-space diagram? '))


#LISTS
entry_count = []
veicList = []
posMatrix = []
density = []
        
#DEFINING VEIHCLES
class Veic:
    def __init__(self,ln,id,ty,v,x):
        self.type = ty # 0 = car, 1 = truck
        self.id = id
        self.v = v
        self.x = x
        self.lane = ln

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
        
    #STEP 5: exiting
        if self.x > (L-1):
            veicList[self.lane].remove(self)

#CHECK SAFE DISTANCE
def safe_dist(ln,id):
    n = len(veicList[ln])
    leader = veicList[ln][n-1].id
    pos = (n-1)+leader-id
        
    #CASE 1: veihcle is leading:
    if id == leader:
        d = vmax

    #CASE 2: veihcle is following:
    else:
        d = veicList[ln][pos+1].x - veicList[ln][pos].x - 1
    return d
          
#SIMULATION SETUP
lane = 0
while lane < 2*n_lanes:

#CREATE LISTS FOR EACH LANE
    veicList.append([])
    posMatrix.append([])
    entry_count.append(0)
    
#INSERT CARS IN EACH LANE
        
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

    #NEXT LANE
    lane += 1

#FILE HANDLING
    
#NAME FILES
sim_file = file_name+'.csv'
data_file = file_name+'_dat.csv'
diagram_file = []
for lane in range(2*n_lanes):
    diagram_file.append(file_name + '_0' + str(lane) + '.txt')

#OPEN FILES
try:
    sim_hand = open(sim_file,'w')
except:
    print('File cannot be opened: ',sim_file)
    exit()    

print('Starting...')
sim_hand.write('t,ID,type,lane,pos\n')   

#RUN SIMULATION
while t < T:
    print('t: ',t)

    lane = 0
    while lane < 2*n_lanes:
    
        #ENTRY FLOW
        n = len(veicList[lane])
        if (t*flowList[lane]/3600-entry_count[lane]) > 1 and veicList[lane][0].x > 0:
            ty = 0
            if uniform(0,1) < tp:
                ty = 1
            new_veicList = [Veic(lane,veicList[lane][0].id+1,ty,0,0)]
            
            #adding veihcles
            i=0
            while i < len(veicList[lane]):
                new_veicList.append(veicList[lane][i])
                i+=1
                
            veicList[lane] = new_veicList
            entry_count[lane] += 1
    
        #UPDATE POSITIONS
        i = 0
        n = len(veicList[lane])
        while i < len(veicList[lane]):
            veicList[lane][n-1-i].update()
            sim_hand.write(str(t)+','+str(veicList[lane][i].id)+','+str(veicList[lane][i].type)+','+str(veicList[lane][i].lane)+','+str(veicList[lane][i].x)+'\n')
            if veicList[lane][i].type == 1:
                sim_hand.write(str(t)+','+str(veicList[lane][i].id)+','+str(veicList[lane][i].type)+','+str(veicList[lane][i].lane)+','+str(veicList[lane][i].x+1)+'\n')
            i += 1  
    
        lane += 1  

    #STEP DATA
    density.append(n/L)
    
    t += 1

print('Done!')
sim_hand.close()

#SIMULATION REPORT
    
#0PEN DATA FILE
try:
    data_hand = open(data_file,'w')
except:
    print('File cannot be opened: ',data_file)
    exit()  

data_hand.write('t,k,\n')

t = 0
while t < T:
    data_hand.write(str(t)+','+str(density[t])+'\n')
    t += 1
        
data_hand.close() 
