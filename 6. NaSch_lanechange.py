#LIBRARIES
from random import uniform, randint

#MENU
file_name = input('File name: ')

loop = True
while loop == True:
    settings = input('Use default settings? (y - yes / n - no) ')

#DEFAULT
    if settings == 'y':
        flowList = [900,900,900,900,900,900,900,900,900,900,900,900] #entry flow in each lane [lane 1, lane 2, lane 3...] in veic/hour
        L = 1000 #number of cells 
        T = 10 #number of seconds for the simulation
        DENSITY = 0.25 #how many cars
        vmax = 5 #maximum car speed 
        p = 0.25 #probability of random stop
        tp = 0.3 #truck/total ratio
        n_lanes = 1 #number of n_lanes in each direction
        display_lane = 0 #lane for the space-time diagram
        loop = False

#CUSTOM
    elif settings == 'n':
        T = int(input('Period of simulation (T): '))
        p = float(input('Probability of random stop (range 0-1): '))
        tp = float(input('Percentage of trucks (range 0-1): '))
        L = round(float(input('Lenght of the simulation in km (L): '))/7.5,0) #NEED TO ROUND UP THE L VALUE
        n_lanes = int(input('Number of lanes in each direction: '))
        vmax = round((float(input('Maximum car speed in km/h (vmax): '))/(3.6*7.5)),0)
        DENSITY = float(input('Initial car density (if you wish to start with an empty road, type 0): '))
        flowList = []
        lane = 0
   #     for lane in range(2*n_lanes):
    #        print('Flow in lane ',lane,': ')
    #        x = int(input())
    #        flowList.append(x)
        display_lane = int(input('Which lane should be displayed in time-space diagram? '))
        loop = False
    
    else:
        print('Invalid answer! Please use only "y" or "n".')

#TEST FLOW
flowList = [150,150]
change_t = [100,200,300,400,500,600,700,800,900,1000]
changecount = 0

#LISTS AND VARIABLES
driver_type = [0.0,0.1,0.2,0.3,0.4]
n_driver_type = len(driver_type)
veicNum = int(DENSITY*L)
entry_count = []
veicList = []
gapList = []
posMatrix = []
density = []
v_count = 0
leader = 0
t = 0
        
#DEFINING CLASSES
class Road:
	def __init__(self,direction,x):
		self.dir = direction #TRUE (LEFT) OR FALSE (RIGHT)
		self.x = x

#USEFUL FEATURES TO HAVE:
#driver slack factor -> tendency to revert to the right lane (bigger in trucks)

class Veic:
    def __init__(self,lane,id,ty,ag,v,x):
#       self.col = color(random(255),random(140),random(255))
        self.id = id #VEIHCLE ID
        self.type = ty #VEIHCLE TYPE, FOLLOWING: 0 = car, 1 = truck 
        self.lane = lane #CURRENT LANE
        self.ag = ag #DRIVER AGGRESSIVENESS (tendency to change lanes when blocked by another veihcle)
#        self.slack = slack #DRIVER SLACKNESS (tendency to go to the righter lanes)
        self.v = v #SPEED
        self.x = x #REAR BUMPER POSITION

    #DRIVING RULES
    def update(self):
    #STEP 1: acceleration 
    # All cars that have not already reached the maximal velocity vmax acceleration by one unit: v -> v+1         
        if self.v < vmax-self.type:
            self.v += 1        
        
    #STEP 2: lane change and safety distance
    #If a car has d empty cells in front of it and is its velocity v (after step 1) larger then d, then it reduces the velocity to d: v -> min{d,v}        
        gapList = safe_distances(self.id)
        d = gapList[4] - self.type
                    
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
        
    	#leaving the system
        if self.x > (L-1):
            veicList[self.lane].remove(self)


    #LANE CHANGE (both inside the veihcle's info and in the veicList
    def lane_change(self,move):
        list_lane_change(self.id,move)
        self.lane += move
   	
#*****CHANGE CAR LANE INSIDE VEICLIST*****
def list_lane_change(id,move):
	
	#SAVE CURRENT CAR INFO
	veihcle = search_car(id)
	lane = veihcle.lane
	new_lane = lane + move
	gapList = safe_distances(id)
	left_right = 0
	if move == +1:
		left_right = 2
	
	#CURRENT POSITION INSIDE LIST
	pos = 0
	while veicList[lane][pos] != veihcle:
		pos+=1

	#DESIRED POSITION IN NEW LIST
	entrance_pos = 0
	while veicList[new_lane][entrance_pos].x < veihcle.x:
		entrance_pos+=1

   	#INSERT CAR IN DESIRED POSITION
	car = 0
	done = False
	new_car_list = []
	while car < len(veicList[new_lane]):
		new_car_list.append(veicList[new_lane][car])

		#REQUIREMENTS FOR LANE CHANGE: 
		# the next driver in the desired lane is faster then the current next driver (it is desired to change lanes).
		# there is room for the changing manouver (gap check).
		# the change has not yet been made

		if veicList[new_lane][entrance_pos+1].v > veicList[lane][pos+1].v and gapList[left_right+1] >= 0 and gapList[left_right] >= 0 and done == False:
			new_car_list.append(veihcle)
			veicList[lane].remove(veihcle)
			done = True
		car += 1

	veicList[new_lane].append(veihcle) #same size
	veicList[new_lane] = new_car_list
	
#*****FIND CAR BASED ON ID*****
def search_car(id):
    car = 0
    lane = 0
    for lane in range(2*n_lanes):
        for car in range(len(veicList[lane])):
            if veicList[lane][car].id == id:
                return veicList[lane][car]
 
#*****GAP ACCEPTANCE*****
def safe_distances(id):
    car = search_car(id)
    lane = car.lane
    n = len(veicList[lane])
    leader = veicList[lane][n-1].id
    
    #FIND CURRENT POSITION
    pos = 0 
    while id != veicList[lane][pos].id:
        pos += 1
    

    #ADVANCING

    #CHECK SAFETY FRONT DISTANCE
    #CASE 1: veihcle is leading:
    if id == leader:
        d = vmax - veicList[lane][pos].type #if it's a truck, it's speed is reduced by 1

    #CASE 2: veihcle is following:
    else:
        d = veicList[lane][pos+1].x - veicList[lane][pos].x - 1 - veicList[lane][pos].type

    #FIND SHOLDERS
    if lane < n_lanes:
        left_sholder = 0
        right_sholder = n_lanes-1
    else:
        left_sholder = n_lanes
        right_sholder = 2*n_lanes-1

    #CHECK BORDER SAFETY DISTANCES    
    #create gapList to hold border safety distances (front-left, back-left, front-right and back-right)
    dList = [] 
    for i in range(4):
        dList.append(0)

    #SINGLE LANE
    if n_lanes == 1:
        dList[0] = -1 #FRONT-LEFT
        dList[1] = -1 #BACK-LEFT
        dList[2] = -1 #FRONT-RIGHT
        dList[3] = -1 #BACK-RIGHT
        
    #TWO OR MORE LANES    
    elif n_lanes == 2:
        #check if RIGHT or LEFT
        if lane == left_shoulder: 
            dList[0] = -1 #FRONT-LEFT
            dList[1] = -1 #BACK-LEFT
            dList[2] = gap(0,1,veicList[lane][pos]) #FRONT-RIGHT
            dList[3] = gap(1,1,veicList[lane][pos]) #BACK-RIGHT

        elif lane == right_shoulder:
            dList[0] = gap(0,0,veicList[lane][pos]) #FRONT-LEFT
            dList[1] = gap(1,0,veicList[lane][pos]) #BACK-LEFT
            dList[2] = -1 #FRONT-RIGHT
            dList[3] = -1 #BACK-RIGHT
            
        else: 
            dList[0] = gap(0,0,veicList[lane][pos]) #FRONT-LEFT
            dList[1] = gap(1,0,veicList[lane][pos]) #BACK-LEFT
            dList[2] = gap(0,1,veicList[lane][pos]) #FRONT-RIGHT
            dList[3] = gap(1,1,veicList[lane][pos]) #BACK-RIGHT

    dList.append(d)
    return dList

#*****DRIVER PERCEPTION*****
def gap(lr,fb,car):

    posList = []
    car = 0
    
    #RIGHT OR LEFT LANE? #makes a list of all the occupied positions inside the lane the car is willing to turn to
    if lr == 0:
        for car in veicList[car.lane+1]:
            posList.append(veicList[car.lane+1][car].x)

    else:
        for car in veicList[car.lane-1]:
            posList.append(veicList[car.lane+1][car].x)

    #FRONT OR BACK? #finds distance to desired neighbor in the new lane by growing "dist" till it finds an occupied space  
    dist = 0
    while x not in posList:
        dist += 1
        if fb == 0:
            x += 1
        else:
            x -= 1

    #SIZE? #reduce the distance in 1 in case it's a truck going foward
    if fb == 0:
        dist = dist - car.type

    return dist 


#*****SIMULATION SETUP*****
lane = 0
while lane < 2*n_lanes:

	#CREATE LISTS FOR EACH LANE
    veicList.append([])
    posMatrix.append([])
    entry_count.append(0)
    
        
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
        veicList[lane].append(Veic(lane,veicNum-1-i+v_count,ty,randint(0,n_driver_type-1),randint(0,vmax),posMatrix[lane][i]))
        i += 1

    #NEXT LANE
    v_count += i
    lane += 1

#*****FILE HANDLING*****
    
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
sim_hand.write('t,ID,type,lane,driver_type,pos,speed\n')   

#*****RUN SIMULATION***** (creates the main file)

while t < T:
    print('t: ',t)
    
    #ADVANCE PHASE
    #update posMatrix after lane change
    veic = 0
    lane = 0
    posMatrix = []
    while lane < 2*n_lanes:
        posMatrix.append([])
        while veic < len(veicList[lane]):
            posMatrix[lane].append(veicList[lane][veic].x)
            veic += 1
        lane += 1
            
    #update cars from Upstream to Downstream.
    cell = (L-1)
    while cell > -1:
        lane = 0
        while lane < 2*n_lanes:
            if cell in posMatrix[lane]:
                pos = 0
                while veicList[lane][pos].x != cell:
                    pos+=1
                veicList[lane][pos].update()
                sim_hand.write(str(t)+','+str(veicList[lane][pos].id)+','+str(veicList[lane][pos].type)+','+str(veicList[lane][pos].lane)+','+str(veicList[lane][pos].ag)+','+str(veicList[lane][pos].x)+','+str(veicList[lane][pos].v)+'\n')
            lane += 1
        cell -= 1
    	
    #ENTRY FLOW
        lane = 0
        while lane < 2*n_lanes:
            #check if it's time to add a new veic and if there is space for such
            if (t*flowList[lane]/3600-entry_count[lane]) > 1 and veicList[lane][0].x > 0:
                
                #check type of new veihcle
                ty = 0
                if uniform(0,1) < tp:
                    ty = 1
	            
	        #create veihcle alone inside new lists
                v_count += 1
                new_veicList = [Veic(lane,v_count,ty,randint(0,n_driver_type-1),0,0)]


	        #update old lists (this is made so that the new veihcle is inserted in position "0")
                veihcle = 0
                while veihcle < len(veicList[lane]):
                    new_veicList.append(veicList[lane][veihcle])
                    veihcle += 1
                    veicList[lane] = new_veicList
                    entry_count[lane] += 1


    #COLECTING DATA FROM THE TIME-STEP  (intended for the "_dat" file)
    density.append(n/L)
    
    #NEXT TIME STEP
    t += 1

print('Done!')
sim_hand.close()

#****SIMULATION REPORT**** (in progress, creates the "_dat" file)
    
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


    #LANE CHANGE PHASE (left movements in even time-steps and right movements in odd time-steps) 
    #needs to be done BEFORE allowing the cars to move to avoid accidents.
    
 #   lane = 0
 #   while lane < 2*n_lanes:
#	car = len(veicList[lane])-1
#	while car > -1: 
 #           if t%2 == 0:

	    #GET CAR DATA



	    #IF IT FITS THE REQUIREMENTS, ORDER LANE CHANGE
#	    if #fill the requirements:
	#    	veicList[lane][car].lane_change(-1)
	#    	else:
	    		#(...)
	#    	car -= 1
	#    lane += 1
