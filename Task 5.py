import numpy as np
from numpy import inf

#given values for the problems
d = np.array([[0,10,12,11,14]
              ,[10,0,13,15,8]
              ,[12,13,0,9,14]
              ,[11,15,9,0,16]
              ,[14,8,14,16,0]])

iteration = 100
n_ants = 5
n_citys = 5

# intialization part
m = n_ants
n = n_citys
e = .5      #evaporation rate
alpha = 1   #pheromone factor
beta = 2    #visibility factor

#calculating the visibility of the next city visibility(i,j)=1/d(i,j)
visibility = 1/d
visibility[visibility == inf ] = 0

#intializing pheromne present at the paths to the cities
# *** NOTE: Pheromone matrix should be (n, n) not (m, n) ***
# All ants update the *same* shared pheromone trails.
pheromne = .1*np.ones((n,n)) # Corrected from (m, n) to (n, n)

#intializing the rute of the ants with size rute(n_ants,n_citys+1) 
#note adding 1 because we want to come back to the source city
rute = np.ones((m,n+1))

for ite in range(iteration):
    
    rute[:,0] = 1          #initial starting positon of every ants '1' i.e city '1'
    # Set the return city to 1 as well
    rute[:,n] = 1          # This makes the tour complete: 1 -> ... -> 1
    
    for i in range(m):
        
        temp_visibility = np.array(visibility)    #creating a copy of visibility
        
        # Loop n-1 times to select the next n-1 cities
        for j in range(n-1):
            
            combine_feature = np.zeros(n)   # Must be size n (5)
            cum_prob = np.zeros(n)        # Must be size n (5)
            
            cur_loc = int(rute[i,j]-1)      #current city of the ant (0-indexed)
            
            temp_visibility[:,cur_loc] = 0     #making visibility of the current city as zero
            
            # *** CORRECTION 1: Swapped alpha and beta ***
            p_feature = np.power(pheromne[cur_loc,:], alpha)  # Pheromone ^ alpha
            v_feature = np.power(temp_visibility[cur_loc,:], beta)  # Visibility ^ beta
            
            #no need to add new axis, features are already (5,)
            
            combine_feature = np.multiply(p_feature,v_feature) #calculating the combine feature
                                    
            total = np.sum(combine_feature)                  #sum of all the feature
            
            # Handle division by zero if ant gets trapped
            if total == 0:
                total = 1e-10 # Add a small value to avoid NaN

            probs = combine_feature/total   #finding probability of element
            
            cum_prob = np.cumsum(probs)     #calculating cummulative sum
            r = np.random.random_sample()   #randon no in [0,1)
            
            try:
                city = np.nonzero(cum_prob>r)[0][0]+1  #finding the next city (1-indexed)
            except IndexError:
                # Fallback if all probabilities were 0 (e.g., ant trapped)
                # Find any city not yet visited
                visited_cities = set(rute[i, :j+1])
                all_cities = set(range(1, n + 1))
                non_visited = list(all_cities - visited_cities)
                city = non_visited[0] if non_visited else 1 # Pick first non-visited, or 1 as last resort

            rute[i,j+1] = city              #adding city to route 
            
        # *** CORRECTION 2: Removed redundant 'left' calculation ***
        # The loop above already fills the entire route from rute[i,1] to rute[i,n-1]
        # The lines below were incorrect and redundant.
        # left = list(set([i for i in range(1,n+1)])-set(rute[i,:-2]))[0]
        # rute[i,-2] = left
       
    rute_opt = np.array(rute)          #making a copy of current routes
    
    dist_cost = np.zeros((m,1))        #intializing total_distance_of_tour with zero 
    
    for i in range(m):
        
        s = 0
        # *** CORRECTION 3: Loop 'n' times to get complete tour cost ***
        for j in range(n): # Was (n-1), which missed the last leg
            
            s = s + d[int(rute_opt[i,j])-1,int(rute_opt[i,j+1])-1]  #calcualting total tour distance
        
        dist_cost[i]=s               #storing distance of tour for 'i'th ant
          
    dist_min_loc = np.argmin(dist_cost)           #finding location of minimum of dist_cost
    dist_min_cost = dist_cost[dist_min_loc]       #finging min of dist_cost
    
    best_route = rute[dist_min_loc,:]           #saving best route
    pheromne = (1-e)*pheromne                     #evaporation of pheromne
    
    for i in range(m):
        # *** CORRECTION 4: Loop 'n' times to update all pheromones ***
        for j in range(n): # Was (n-1), which missed the last leg
            
            dt = 1/dist_cost[i] # dt is based on the *complete* tour cost
            
            start_node = int(rute_opt[i,j])-1
            end_node = int(rute_opt[i,j+1])-1
            
            pheromne[start_node, end_node] = pheromne[start_node, end_node] + dt
            #updating the pheromne with delta_distance

print('route of all the ants at the end :')
print(rute_opt.astype(int)) # Print as integers for clarity
print()
print('best path :', best_route.astype(int))

# *** CORRECTION 5 & 6: Fixed print statement and removed syntax error ***
# The cost is now calculated correctly, so no need to add the last leg manually.
print('cost of the best path', int(dist_min_cost[0]))