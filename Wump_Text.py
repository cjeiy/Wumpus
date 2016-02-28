
#Carl-Johan Larsson
#910307-3152
#04-11-2013

import random
import sys
import time
import os
from random import choice
from operator import itemgetter, attrgetter


class Run():
    """1. Takes in different functions and start values of essential variables
       2. Creates sub-class objects and updates strings for game info_string
       3. It returns start values, and holds important information during gameplay"""
    def __init__(self):
        self.room_list=create_room_list()
        self.difficulty=read_difficulty()
        self.wdiff = int(self.difficulty)
        self.danger_list=create_danger_list(self.difficulty)
        self.room=create_rooms(self.room_list,self.danger_list)
        self.player1 = Player(random.randrange(0,20),5,0,self.room_list)
        self.room_list_arrow = self.room_list + [666]
        self.arrow1  = Arrow(20,self.room_list_arrow)
        if self.wdiff == 3 :
            self.wumpus1 = Wumpus(random.randrange(0,20))
        else:
            self.wumpus1 = Wumpus(wumpus_position_easy_normal(self.danger_list))
        self.highscore_moves=0
        self.which_danger = 0
        self.shootormovelist = ["Y","y","N","n","S","s","M","m"]
        self.keep_playing = True
        self.win = False
        self.danger_close = 0
        

    
class Wumpus():
    """A class that sees to that a wumpus object is given a random position on every turn of gameplay"""
    def __init__(self,position):
        self.position = position
#Enables Wumpus to move when playing on expert
    def move(self):
        self.position = random.randrange(0,20)


#Class for player, contains the necessary attributes for the player. 
class Player():
    """1. Takes position,arrows_left,what dangers are close,and a list of the roomnumbers
       2. holds information on the player object which represents the user
       3. Gives back information on nearby dangers """
    def __init__(self,position,arrows_left,danger,room_list):
        self.position = position
        self.arrowsleft = arrows_left
        self.danger = danger
        self.room = room_list[position]
        self.room_list = room_list
        
#Enables the player to move and store new location
    def movement(self,new_position):
        self.position = new_position
        self.room = self.room_list[new_position]
#Enables the player to recognize what dangers he stumble upon
    def catch_danger(self,danger):
        self.danger=danger
        return danger

#Class for arrow, enables seperate movement not effecting the players position
class Arrow():
    """See Player class"""
    def __init__(self, position,room_list_arrow):
        self.position = position
        self.room = room_list_arrow[position]
        self.room_list_arrow = room_list_arrow
#Enable the arrow to move and store location since every arrow goes through 3 rooms.        
    def movement(self,new_room):
        self.position = new_room
        self.room = self.room_list_arrow[new_room]
#On startup the rooms are given different attributes, what danger they contain, what dangers there are in the surrounding rooms
#And which the surrounding rooms are   
class Room_class():
    """ 1. Is given the matrice which creats the "map"
        2. Assigns the necessary information to every room object
        3. Holds the information during gameplay"""
    def __init__(self,room_ind,roomnumber,south,north,east,west,danger,danger_close):
        self.room_ind = room_ind
        self.roomnumber = roomnumber
        self.south = south
        self.north = north
        self.east = east
        self.west = west
        self.danger_close = danger_close
        self.danger = danger


class Highscore(object):
    """Holds the information on the players actions during gameplay ==> Score when won"""
    def __init__(self, name, moves,arrowsleft,difficulty,score):
        self.name=name
        self.moves=moves
        self.arrowsleft=arrowsleft
        self.difficulty=difficulty
        self.score=int(score)

    def __str__(self):
        return "%11s" %str(self.name)+"%7s"  %str(self.moves)+"%8s" %str(self.arrowsleft)+"%7s" %str(self.difficulty)+"%8s"  %str(self.score)
       # ("%12s" %"Name:" + "%10s" %"Moves" + "%12s" %"Arrowsleft:" +"%12s"  %"Difficulty:" +"%10s"  %"Score:"+"\n")

def read_highscore():
    """Reads the highscore information from file and appends different attributes to a list"""
    highscore = open(os.path.dirname(os.path.realpath(__file__))+"\\highscore.txt")
    highscore_list = highscore.readlines()
    highscore_obj = []

    for line in highscore_list:
        high_strip = line.rstrip()
        highscore_attribute=high_strip.split()

        try:
            score=int(highscore_attribute[4])
            highscore_obj.append(Highscore(highscore_attribute[0],highscore_attribute[1],highscore_attribute[2],highscore_attribute[3],highscore_attribute[4]))
            highscore_attribute=[]

        except IndexError or ValueError:
            pass

    return highscore_obj

def save_highscore(name,moves,arrowsleft,difficulty):
    """1. Is given information from the players round
       2. Creats a string and saves it to file
       3. Returns the score"""
    score=((300*arrowsleft+500*(difficulty))-(40*moves))
    string_score = str(score)
    moves=str(moves)
    arrowsleft=str(arrowsleft)
    difficulty=str(difficulty)
    file = open(os.path.dirname(os.path.realpath(__file__))+"\\highscore.txt", "a" )
    file.write("%10s" %name[:10] + "%3s" %moves[:2] + "%3s" %arrowsleft[:2] +"%7s"  %(active_difficulty())[:6] +"%5s"  %string_score[:5]+"\n")
    return string_score

def highscore_sorting(highscore_obj):
    highscore_sort = sorted(highscore_obj, key = attrgetter("score"),reverse = True)
    
    return highscore_sort

#Input check when changing difficulty, only 1-3 will change difficulty.
def change_difficulty(difficulty):
    while True:
        if (difficulty == "1") or (difficulty == "2") or (difficulty == "3"):
            break
        else:
            difficulty=input("Choose an alternative[1,2,3] : ")
    return difficulty

#The difficulty saves/reads to a file, since this operation is only done when switching difficulty it doesn't take unnecessary memory.
def save_difficulty(diff):
        file = open(os.path.dirname(os.path.realpath(__file__))+"\\difficulty.txt", "w" )
        file.write(diff)
        
def read_difficulty():
    file= open(os.path.dirname(os.path.realpath(__file__)) +"\\difficulty.txt", "r")
    difficulty=int(file.readline())
    return difficulty




#Gives information on what difficulty is selected when in Main Menu
def active_difficulty():
    file= open(os.path.dirname(os.path.realpath(__file__))+"\\difficulty.txt", "r")
    difficulty=int(file.readline())
    if difficulty == 1:
        return "Easy"
    elif difficulty == 2:
        return "Normal"
    elif difficulty == 3:
        return "Expert"
    
#Creates different lists depending on difficulty, 0=Nothing, 1=Bat, 2=Bottomless Hole, 3=Wumpus(normal,easy he is not moving), 7=lose one arrow, 8=new arrow

def create_danger_list(diff):
    """Creates a list containing danger values for different difficulty"""
    diff = int(diff)
    if diff == 1:
        danger_list = [9,0,0,0,7,8,8,8,8,1,1,1,1,1,1,0,0,2,2,3]
    elif diff == 2:
        danger_list = [9,0,0,0,7,7,8,8,8,1,1,1,1,1,1,2,2,2,2,3]
    elif  diff == 3:
        danger_list = [9,0,0,0,7,7,7,8,8,1,1,1,1,1,1,2,2,2,2,0]
    random.shuffle(danger_list)
    return danger_list
    

def create_room_list():
    room_list=[]
    for i in range(0,20):
        room_list.append(i)
    random.shuffle(room_list)
    return room_list

def create_rooms(room_list, danger_list):
    """1. Takes in a list containing 0-19 and list with danger values
       2. Links the different rooms together with a danger value and creates room objects using the class Room_class
       3. returns a list containg the room objects"""
    room_list=[]
    for i in range(0,20):
        room_list.append(i)
    random.shuffle(room_list)
    #The room objects are give attributes p = room index, u = roomnumber, i,j,k,l = Nearby rooms index in room_list
    room=[]
    for a in range(0,20):
        p=a
        u=room_list[a]
        #The nearby rooms will be controlled by which index they have
        i=a+1
        j=a-1
        k=a+2
        l=a-2
        #Room 0 is connected to room 19, etc..
        if i == 20:
            i = 0
        if j == -1:
            j = 19
        if k == 21:
            k=1
        if k == 20:
            k=0
        if l==-1:
            l=19
        if l==-2:
            l=18
        v=danger_list[a]
        danger_close=[]
        danger_close.append(danger_list[i])
        danger_close.append(danger_list[j])
        danger_close.append(danger_list[k])
        danger_close.append(danger_list[l])
        #Creates the room-objects
        room.append(Room_class(p,u,i,j,k,l,v,danger_close))
    return room


#Ignores wumpus movement when on easy or Normal
def wumpus_position_easy_normal(danger_list):
    """Sees to that wumpus is identified att the right position when he's not moving ( easy and normal)"""
    for a in range(0,20):
        if danger_list[a] == 3:
            index = a 
    return index


#Sweeps the nearby rooms for dangers, and Wumpus when not difficulty=Expert.
def check_danger_close(current_position):
    """Checks for nearby dangers"""
    new_dangerlist=[]
    danger= run1.room[current_position].danger_close
    if 1 in danger:
        new_dangerlist.append(1)
    if 2 in danger:
        new_dangerlist.append(2)
    if ((run1.wumpus1.position == run1.room[run1.player1.position].north) or (run1.wumpus1.position == run1.room[run1.player1.position].south) or (run1.wumpus1.position == run1.room[run1.player1.position].east) or (run1.wumpus1.position == run1.room[run1.player1.position].west)) or (3 in danger):
        new_dangerlist.append(3)
    return new_dangerlist

#The different prints triggered by what dangers are close
def print_danger_close():
    """Identifies danger and prints appropriate string"""
    print("\n"+"**Environment Info**")
    if 1 in run1.danger_close:
        print("You can hear BATS flapping nearby!!")
    if 2 in run1.danger_close:
        print("You can feel the wind from a PIT!!")
    if 3 in run1.danger_close:
        print("You can hear a furious WUMPUS-growl echoing throughout the catacombs!")
        
#The interperter for all the scenarios which can happen during gameplay, string formatting since object-data most be brutally handled.
def consequence(what_danger):
        """1. Reads information for the run objects
       2. processes the infomation and takes the appropriate action
       3. Returns new information to run/player class"""
    
        if what_danger == 1:
            #Adds a random danger, but not a bottomless hole or wumpus instead of bat. Can be bat (1) again.
            run1.room[run1.player1.position].danger = choice([0,1,1,1,7,8])
            run1.player1.position = random.randrange(0,20)
            run1.player1.room = run1.room_list[run1.player1.position]
        
        elif what_danger == 8:
            run1.player1.arrowsleft += 1
            run1.room[run1.player1.position].danger = 0
        
        elif what_danger == 7:
            if run1.player1.arrowsleft > 0:
                run1.player1.arrowsleft -= 1
            run1.room[run1.player1.position].danger = 0
            
        elif what_danger == 9:
            run1.wumpus1.position = run1.player1.position +1
            if run1.wumpus1.position == 20:
                run1.wumpus1.position = 19
            run1.room[run1.player1.position].danger = choice([0,1,1,1,7,8])
            
        else:
            pass

def danger_print_consequence(what_danger,position):
    current_room = position
    current_room = str(current_room)
    if what_danger == 1:
        return "\n"+"\n"+"**EVENT**"+"\n"+"A bat grabs you and drops you in room " + current_room
    elif what_danger == 3:
        run1.player1.position = run1.wumpus1.position
        return "\n"+"A BIG WUMPUS COMES OUT OF THE DARK AND HITS YOU IN THE FACE"+"\n"+"\n"+"BETTER LUCK NEXT TIME"+"\n"+"\n"
    elif what_danger == 2:
        return "\n"+"- WAHHHHHHHHHHHHHhhhhhhhhhhh........"+"\n"+"\n"+"***You fell down a bottomless pit***"+"\n"+"BETTER LUCK NEXT TIME!"+"\n"+"\n"
    elif what_danger == 4:
        return "\n"+"You hit Wumpus! You win!"
    elif what_danger == 5:
        return "\n"+"The arrow comes back into room "+ current_room +" and hits you right in the chest, YOU DIE"
    elif what_danger == 8:
        return "\n"+"\n"+"**EVENT**"+"\n"+"You found an arrow!"
    elif what_danger == 7:
        return "\n"+"\n"+"**EVENT**"+"\n"+"One of Wumpus small minions comes out from the dark and steals one of your arrows"
    elif what_danger == 9:
        return "\n"+"\n"+"**EVENT**"+"\n"+"You Found a Flute! You play a short tune and immediatley you hear Wumpus moving towards you!"+"\n"+" He might be in one of the nearby rooms!"
        

#The interpeter for the commands given by the player when walking
def move(direction,current_position):
    while True:
        if (direction.upper() == "N"):
            run1.player1.movement(run1.room[current_position].north)
            break
        elif (direction.upper() == "S"):
            run1.player1.movement(run1.room[current_position].south)
            break
        elif (direction.upper() == "E"):
            run1.player1.movement(run1.room[current_position].east)
            break
        elif (direction.upper() == "W"):
            run1.player1.movement(run1.room[current_position].west)
            break
        else:
            direction = input("Enter a direction! [N,S,E,W]: ")

    
#The interpreter for direction selection when shooting arrows

def shoot(direction, current_position):
    while True:
        if (direction.upper() == "N") :
            run1.arrow1.movement(run1.room[current_position].north)
            break
        elif (direction.upper() == "S"):
            run1.arrow1.movement(run1.room[current_position].south)
            break
        elif (direction.upper() == "E"):
            run1.arrow1.movement(run1.room[current_position].east)
            break
        elif (direction.upper() == "W"):
            run1.arrow1.movement(run1.room[current_position].west)
            break
        else:
            direction = input("Enter a direction! [N,S,E,W]: ")


        
#The information which always is available to the player

def position_and_nearby_rooms(current_position):
    position_and_arrows=str("**Your current position is room "+ str(run1.player1.room)+"**\n" +"Arrows Left: "+ str(run1.player1.arrowsleft)+"\n")
    
    nearby_rooms=str("The rooms you can go to are: " +"\n"+ "North: "+ str(run1.room_list[(run1.room[current_position].north)])+"\n"+ "South: "+ str(run1.room_list[(run1.room[current_position].south)])+"\n"+ "East : "+ str(run1.room_list[(run1.room[current_position].east)])+"\n"+ "West : " +str(run1.room_list[(run1.room[current_position].west)]))
    
    info=position_and_arrows+"\n"+nearby_rooms
    return info


#Interperter for user input

def play_again(choice):
    while True:
        if (choice.upper() == "Y"):
            return True
            break
        elif (choice.upper() == "N"):
            return False
            break
        else:
            choice=input("\n"+"Choose YES[Y] or NO[N]: ")
        
def out_of_arrows():
    
    os.system("clear")
    restart=input("You are out of arrows, restart[press r+enter],quit[press q+enter] or wait[press w+enter] for Wumpus to eat you: ")
    if restart.upper() == "R":
        startup()
        print("You will been placed in a random room with 5 new arrows!")
        time.sleep(2)
    elif restart.upper() == "Q":
        sys.exit("You quit Wumpus, hope you had a blast!")
    elif restart.upper() == "W":
        pass
    
def shoot_again():
    
    shootormove = input("\n"+"Do you want to shoot again? You have "+str(run1.player1.arrowsleft)+" arrows left. [Y or N]")
        
    while (shootormove.upper() != "N") and (shootormove.upper() != "Y") :
        shootormove = input("\n"+"Do you want to shoot again? You have "+str(run1.player1.arrowsleft)+" arrows left. [Y or N]: ")
    if (shootormove.upper() ==  "Y"):
        shootormove = "S"
        
        if run1.wdiff == 3:
            run1.wumpus1.move()
    return shootormove

def you_win():
    #Prints the game over message
    print(danger_print_consequence(4,run1.player1.room))
    time.sleep(2)
    #Stores your name and score to file
    your_highscore=save_highscore((input("Write your name: ").replace(" ", "")),run1.highscore_moves,run1.player1.arrowsleft,run1.wdiff)
    print("You scored : "+your_highscore+" points!")
    time.sleep(2)
    os.system("clear")
    
    yes_or_no=play_again(input("Do you want to play again?[Y or N]"))
    if yes_or_no:
        startup()
        return True
    elif not yes_or_no:
        return False   
    
def event(which_danger):
    #Prints what happend
    consequence(which_danger)
    print(danger_print_consequence(which_danger,run1.player1.room))
    if which_danger == 9:
        time.sleep(2)
    time.sleep(2)
    
def wumpus_danger(which_danger):
    if (run1.player1.position == run1.wumpus1.position) and (run1.wdiff == 3):
        which_danger=3
    return which_danger

def startup():
    global run1
    run1=Run()
    
def you_lose(which_danger):
    
    #Prints what happend
    print(danger_print_consequence(which_danger,run1.player1.room))
    time.sleep(2)
    os.system('clear')
    #Sends player input to interpreter, see function play_again
    yes_or_no=play_again(input("Do you want to play again?[Y or N]"))
    if yes_or_no:
        startup()
        return True
    elif not yes_or_no:
        return False   
    
def shoot_action(arrow_count):
    what_danger = 0
    run1.win=False
    arrow_pos=run1.arrow1.room
    arrow_pos=str(arrow_pos)
    #Sends player input to interpreter, see function shoot
    shoot(input("The arrow is leaving room " +arrow_pos+" in what direction? [N,S,E,W]: "), run1.arrow1.position)
    
    #If Wumpus gets hit the loop is broken, If you curve the arrow back at yourself the loop is broken
    if (run1.arrow1.position == run1.wumpus1.position):
        run1.win="win"
        what_danger = 4
        arrow_count=3
    elif (run1.arrow1.position == run1.player1.position):
        what_danger=5
        run1.win="Game_over"
        arrow_count=3
    elif (run1.wumpus1.position==run1.player1.position):
        what_danger = 2
        run1.win="Game_over"
        arrow_count=3
        
    return_list=[arrow_count,run1.win,what_danger]
    return return_list

def instruction_string():
    instruction_string = """
    Instructions:
            
    You are deep down under KTH in the old catacombes where the evil Wumpus lives.
    
    To avoid beeing eaten you have to shoot Wumpus with your bow before he finds you.
    The catacombs consists of 20 rooms with tunnels between them, the tunnels can lead back to the same room you came from.
    
    Inside the catacombs you will find:
    
     - Bottomless holes
     - Bats which will pick you up and drop you in another room
     - Wumpus, who will eat you as soon as he gets a chance
     - Extra arrows
     
    You move around with the keyboard using the letter corresponding to the direction you want to walk.
    When shooting you will be able to bend the arrows through 3 rooms.
    Q will quit the game.
    
    Difficultys:
    
    Easy   -  Less chance of falling down Bottomless Holes, Higher chance of finding extra arrows
    Normal -  Intermediate chance of finding arrows and falling down Bottomless Holes
    Expert -  Wumpus moves out from is cave and tries to find you, low chance of finding extra arrows.
     
     Good Luck!
     
     *Press Enter to go back*"""

    return instruction_string   
        
        

        
        

def expert_move(shootormove):
    if (run1.wdiff == 3) and (shootormove in run1.shootormovelist) and (run1.which_danger != 9):
        run1.wumpus1.move()            


def move_code():
    
    #Takes player inputs and sends to interperter, see function: move
    move(input("Choose Direction [N,S,E,W]: "),run1.player1.position)
    #Catches what danger you find in the room
    run1.which_danger=int(run1.player1.catch_danger(run1.room[run1.player1.position].danger))
    #When playing on expert wumpus may have walked into the same room you are in.
    run1.which_danger = wumpus_danger(run1.which_danger)
    #If there is a danger we go in to this if statement.
    if run1.which_danger != 0:
        #BATS, ARROWS
        if (run1.which_danger == 1) or (run1.which_danger == 8) or (run1.which_danger == 7) or (run1.which_danger == 9):
            event(run1.which_danger)
            return_list=[run1.which_danger,False]
            return return_list
        #Wumpus or Bottomless Hole
        elif (run1.which_danger == 2) or (run1.which_danger==3):
            run1.win="Game_over"
            return_list=[run1.which_danger,"Game_over"]
            return return_list
    else:
        return_list=[run1.which_danger,False]
        return return_list


def shoot_code(shootormove):
    while True:
    #Sees to that there are arrowsleft, and checks that shootormove == S, since if you dont choose to shoot again
    #shootormove == N
        if (run1.player1.arrowsleft > 0) and ((shootormove.upper() == "S")  and (run1.wumpus1.position != run1.player1.position)):
            arrow_count=0
            run1.arrow1.position = run1.player1.position 
            run1.arrow1.room     = run1.room_list[run1.player1.position]
        
        #Will loop the 3 times you can bend the arrow through 3 different rooms
            while arrow_count<3:
                info = shoot_action(arrow_count)
                arrow_count = info[0]
                run1.win = info[1]
                run1.which_danger = info[2]
                arrow_count+=1
        
        #So that you later dont accidently walk into the room where the arrow object was last, which would result in loosing
        run1.arrow1.position=666
        if run1.player1.arrowsleft > 0:
            run1.player1.arrowsleft -=1
        #If wumpus gets hit
        if (run1.win=="win"):
            return  run1.win,run1.which_danger
        elif run1.win == "Game_over":
            return  run1.win,run1.which_danger
        #If you have arrows left you can shoot again directly
        elif (run1.player1.arrowsleft >0) and (run1.win != "Game_over"):
            shootormove=shoot_again()
            
        if shootormove.upper() == "N":
            return run1.win,run1.which_danger
        
        #Last possibility when you are out of arrows, you can still keep playing
        elif (run1.player1.arrowsleft <= 0) and (run1.player1.position != run1.wumpus1.position):
            out_of_arrows()
            return run1.win,run1.which_danger
    
    #END OF SHOOT CODE

       
def gameplay(shootormove):
        a=0
        #START OF MAIN GAMEPLAY-CODE 
        os.system("clear")
        while True:
            if a>0:        
                #Makes Wumpus move every iteration       
                expert_move(shootormove)     
                #Checks if you have won or lost or can keep playing 
                if (run1.win == "Game_over") or (run1.win == "Game_over_wumpus"):
                    run1.keep_playing=you_lose(run1.which_danger)
                elif (run1.win == "win"):
                    run1.keep_playing=you_win()
                if not run1.keep_playing:
                    break
            a+=1
            os.system("clear")
            
            #Printing out main information, see functions: position_and_nearby_rooms.
            #Checks for nearby dangers and prints them, see functions: check_danger_close and print_danger_close
            print(position_and_nearby_rooms(run1.player1.position))
            run1.danger_close=check_danger_close(run1.player1.position)
            print_danger_close()
            
            #Choice, shoot or move, different parts of the code will activate.
            shootormove = input("\n"+"**Action**"+"\n"+"Do you want to shoot or move? [press S or M]")
            
            #START OF MOVEMENT CODE
            if (shootormove.upper() == "M"):
                #Adds a move for scorekeeping
                run1.highscore_moves+=1
                move_info=move_code()
                run1.which_danger = move_info[0]
                run1.win = move_info[1]
                #END OF MOVEMENT CODE
            
            
            #START OF SHOOT CODE
            elif (shootormove.upper() =="S"):
                shoot_info=shoot_code(shootormove)
                run1.win = shoot_info[0]
                run1.which_danger = shoot_info[1]
   
            elif (shootormove.upper() == "Q"):
                os.system("clear")
                break            

        
#MAIN Menu
def main():
    while True:
        menuchoice=input("****MAIN MENU****"+"\n"+"\n"+"Difficulty: "+str(active_difficulty())+"\n"+"\n"+"1. Play Wumpus!"+"\n"+"2. Change Difficulty"+"\n"+"3. Highscore "+"\n"+"4. Instructions"+"\n"+"5. Exit"+"\n"+"Enter Choice: ")
        os.system("clear")
        
        #START OF MAIN GAMEPLAY-CODE
        if menuchoice == "1":
            startup()    
            gameplay(shootormove=0)
                            #END OF MAIN GAMEPLAY-CODE
                            
    #Choose difficulty                                
        elif menuchoice == "2":
     
    
            print("\n"+"Active Difficulty: "+str(active_difficulty())+"\n")
            diff=input(
                       
                       """
    Difficulty:
            
    1. Easy
    2. Normal
    3. Expert
    
    Enter choice: """)
            diff=change_difficulty(diff)
            os.system("clear")
            save_difficulty(diff)
    #Read highscore (Not finished)
        elif menuchoice == "3":
            print("%28s" %"**HIGHSCORE**"+"\n")
            highscore_sort=highscore_sorting(read_highscore())
            print("%6s" %" "+highscore_sort[0].name+" has the current highscore!!"+"\n")
            print("%11s" %"Name:" + "%7s" %"Moves:" + "%8s" %"Arrows:" +"%7s"  %"Diff:" +"%8s"  %"Score:"+"\n")

            for a in range(0,9):
                print(highscore_sort[a])
            input("\n"+"%9s" %" "+ "***Press Enter to go Back***"+"\n")
            os.system("clear")
    #Get instruction on how to play
        elif menuchoice == "4":
            input(instruction_string())
            os.system("clear")
    #QUIT
        elif menuchoice == "5":
            sys.exit("\n"+"**You quit Wumpus, hope you had a blast!**"+"\n")
        else:
            pass
    
main()    