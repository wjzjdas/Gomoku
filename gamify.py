#Project 1

#(g) initializing all global variables
def initialize():
    global hedon
    global hedon_duration
    global health
    global health_duration
    global star
    global star_attribute
    star = [0,0,0,0]
    health_duration = [0,0] #0 in second index represent resting, 1 represent running, 2 represent textbooks
    hedon_duration = [120,0,0] #Index 0 represents resting, 1 represents running, 2 represents textbooks
    star_attribute = None
    hedon = 0
    health = 0

#(a) a function that returns the number of hedon points
def get_cur_hedons():
    global hedon
    return hedon
    
#(b) a function that returns the number of health points
def get_cur_health():
    global health
    return health

#(c) a function that offer star for user's performed activity
def offer_star(activity):
    global star
    global star_attribute
    if(activity == 'running' or activity == 'textbooks' or activity == 'resting'):
        star[0] += 1
        star[3] = star[2]
        star[2] = star[1]
        star[1] = 0
        star_attribute = activity
        
#(d) a function that simulates the user’s performing activity for duration minutes
def perform_activity(activity, duration):
    global health
    global hedon
    global star
    global star_attribute
    global health_duration
    global hedon_duration
    #---------------------Here is the section where we look at running. This line here serves as a bookmark to improve readability of the program ----------------------------------
    if(activity == 'running'):
        
        hedon_duration[2] = 0
        hedon_duration[1] += duration
        
        if(hedon_duration[0] >= 120):
            if(hedon_duration[1] - duration >= 10):

                hedon -= duration * 2 #If the user is not tired, running gives 2 hedons per minute for the first 10 minutes of running, 
                                                            #and -2 hedons per minute for every minute after the first 10
            elif(hedon_duration[1] - duration < 10 and hedon_duration[1] > 10):   
                hedon += (-2)*(hedon_duration[1] - 10) + (duration + 10 - hedon_duration[1])*2   
            else:
                hedon += duration * 2
                
                
        else:
            
            hedon -= 2 * duration
        
        if(star_can_be_taken(activity)):
            if(duration > 10):
                hedon += 30
            else:
                hedon += 3 * duration
        
        #-------------------------------------------
        #Now we start to deal with the health points
        
        if(health_duration[1] != 1): #point of this line is to record number of minutes accumulated doing the same activity, if activity changes, the accumulation resets
            health_duration[0] = duration
            health_duration[1] = 1
        else:
            health_duration[0] += duration
        
        if(health_duration[0] - duration >= 180):
            health += duration #Running gives 3 health points per minute for up to 180 minutes, 
                                #and 1 health point per minute for every minute over 180 minutes that the user runs.
        elif (health_duration[0] - duration < 180 and health_duration[0] > 180):
            health += health_duration[0] - 180 + (duration + 180 - health_duration[0])*3
            
        else:
            health += duration * 3
            
        
        hedon_duration[0] = 0 #Reset resting minutes because user is tired
    
    #---------------------Here is the section where we look at TEXTBOOKS. This line here serves as a bookmark to improve readability of the program ----------------------------------
    elif(activity == 'textbooks'):
        
        hedon_duration[1] = 0
        hedon_duration[2] += duration
        
        if(hedon_duration[0]  >= 120):
            if(hedon_duration[2] - duration >= 20):
                hedon -= duration #If the user is not tired, textbooks gives 1 hedons per minute for the first 20 minutes, 
                                    #and -1 hedons per minute for every minute after the first 20    
            elif (hedon_duration[2] - duration < 20 and hedon_duration[2] > 20):  
                hedon += (-1) * (hedon_duration[2] - 20) + (duration + 20 - hedon_duration[2])                   
            else:
                hedon += duration 
        else:
            hedon -= 2 * duration
        
        if(star_can_be_taken(activity)):
            if(duration > 10):
                hedon += 30
            else:
                hedon += 3 * duration
        
        #-------------------------------------------
        #Now we start to deal with the health points
        
        if(health_duration[1] != 2): #point of this line is to record number of minutes accumulated doing the same activity, if activity changes, the accumulation resets
            health_duration[0] = duration
            health_duration[1] = 2
        else:
            health_duration[0] += duration
        
        health += duration * 2 #Carrying textbooks always gives 2 health points per minute.
    
        hedon_duration[0] = 0 #Reset resting minutes because user is tired
        
    #---------------------Here is the section where we look at resting. This line here serves as a bookmark to improve readability of the program ----------------------------------
    elif(activity == 'resting'):
        
        hedon_duration[1] = 0
        hedon_duration[2] = 0
        hedon_duration[0] += duration #The minute of resting that user gets
        
        #-------------------------------------------
        #Now we start to deal with the health points
        
        if(health_duration[1] != 0): #point of this line is to record number of minutes accumulated doing the same activity, if activity changes, the accumulation resets
            health_duration[0] = duration
            health_duration[1] = 0
        else:
            health_duration[0] += duration
    
    if(star[0] >= 1):
        star[1] += duration #Track the time interval when the last star was offered
    
    star_attribute = None #Reseting star_attribute such that program knows that a star doesn't apply across multiple activities
        
#(e) The function that determines if a star could be used. Also resets the value in star_attribute once it is successfully called.  
def star_can_be_taken(activity):
    global star
    global star_attribute
    if(activity == star_attribute):
        if(star[1] == 0):
            if(star[0] <= 2):
                return True
            elif(star[1] + star[2] + star[3] > 120):
                return True
            else:
                pass
        else:
            pass
    
    return False

#(f) A function that returns the activity that gives the most hedons if the person performed it for one minute at the current time
def most_fun_activity_minute():
    running = 0
    textbook = 0
    resting = 0
    if (hedon_duration[0] >= 120):
        if(hedon_duration[1] > 10):
            running = -2
        else:
            running = 2
        if(hedon_duration[2] > 20):
            textbook = -1
        else:
            textbook = 1
    else:
        running = -2
        textbook = -2
    
    if(star_can_be_taken('running')):
        running += 3
    elif(star_can_be_taken('textbooks')):
        textbook += 3
    else:
        pass

    if (running == max(running,textbook,resting)):
        return 'running'
    elif (textbook == max(running,textbook,resting)):
        return 'textbooks'
    else:
        return 'resting'

#Main program starts here
if __name__ == "__main__":
    
    initialize()