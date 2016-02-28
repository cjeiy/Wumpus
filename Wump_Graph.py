
import sys
from tkinter import *
import random
import sys
import time
import os
from random import choice
from operator import attrgetter

root = Tk()
root.after(1000, lambda: root.focus_force())
root.wm_attributes("-topmost", 1)
root.geometry("500x400")
root.wm_title("Wumpus")
root.configure(background='black')


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
        self.danger_close = []
        self.enviromental_string = ""
        self.event_string =  "You have been placed in a random room with 5 arrows"
        self.info_string = ""
        self.room_string = ""
        self.arrow_count = 0
        self.play_again = 1


    def update_strings(self):
        """1. Takes in information of nearby dangers, and immidiate event_string
           2. Updates the strings which give information to the user
           3. Through the class object it returns updated strings"""


        current_room = str(self.player1.room)
        current_position = self.player1.position
        what_danger = self.which_danger
        self.enviromental_string=""
        self.event_string =""
        self.info_string = ""
        run1.danger_close=check_danger_close()


        if what_danger == 1 :
            self.event_string=("A bat grabs you and drops you in room " + current_room)
            print(self.enviromental_string)
        elif what_danger == 3:
            run1.player1.position = run1.wumpus1.position
            self.event_string=("A BIG WUMPUS COMES OUT OF THE DARK AND"+"\n"+"HITS YOU IN THE FACE"+"\n"+"\n"+"BETTER LUCK NEXT TIME"+"\n")
        elif what_danger == 2:
            self.event_string=("- WAHHHHHHHHHHhhhhhhhhh........"+"\n"+"\n"+"***You fell down a bottomless pit***"+"\n"+"BETTER LUCK NEXT TIME!"+"\n"+"\n")
        elif what_danger == 4:
            self.event_string=("You hit Wumpus! You win!")
        elif what_danger == 5:
            self.event_string=("The arrow comes back into room "+ current_room +"\n"+"and hits you right in the chest, YOU DIE")
        elif what_danger == 8:
            self.event_string=("You found an arrow!")
        elif what_danger == 7:
            self.event_string=("One of Wumpus small minions comes out from the dark and steals one of your arrows")
        elif what_danger == 9:
            self.event_string=("You Found a Flute!"+"\n"+ "You play a short tune and hear Wumpus moving towards you!"+"\n"+" He might be in one of the nearby rooms!")

        self.info_string = ("Room  : " +str(self.player1.room)+"\n"+"\n"+"Arrows : "+str(self.player1.arrowsleft)+"\n"+"\n"+"Moves  : "+str(self.highscore_moves))



        if 1 in run1.danger_close:
            self.enviromental_string+=(" - You can hear BATS flapping nearby!!"+"\n"+"\n")
        if 2 in run1.danger_close:
            self.enviromental_string+=(" - You can feel the wind from a PIT!!"+"\n"+"\n")
        if 3 in run1.danger_close:
            self.enviromental_string+=(" - You can hear a furious WUMPUS-growl echoing throughout the catacombs!"+"\n"+"\n")

        self.room_string = ("North: "+ str(run1.room_list[(run1.room[current_position].north)])+"\n"+ "South: "+ str(run1.room_list[(run1.room[current_position].south)])+"\n"+ "East : "+ str(run1.room_list[(run1.room[current_position].east)])+"\n"+ "West : " +str(run1.room_list[(run1.room[current_position].west)]))

    def update_enviromental_info(self):
        """See update_strings"""
        self.enviromental_string=""
        self.info_string = ""
        run1.danger_close=check_danger_close()

        self.info_string = ("Room  : " +str(self.player1.room)+"\n"+"\n"+"Arrows : "+str(self.player1.arrowsleft)+"\n"+"\n"+"Moves  : "+str(self.highscore_moves))



        if 1 in run1.danger_close:
            self.enviromental_string+=(" - You can hear BATS flapping nearby!!"+"\n"+"\n")
        if 2 in run1.danger_close:
            self.enviromental_string+=(" - You can feel the wind from a PIT!!"+"\n"+"\n")
        if 3 in run1.danger_close:
            self.enviromental_string+=(" - You can hear a furious WUMPUS-growl echoing throughout the catacombs!"+"\n"+"\n")



def startup():
    """creates the class object "run" which contains all the vital information"""
    global run1
    run1=Run()


class Wumpus():
    """A class that sees to that a wumpus object is given a random position on every turn of gameplay"""
    def __init__(self,position):
        self.position = position
#Enables Wumpus to move when playing on expert
    def move(self):
        self.position = random.randrange(0,20)



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

    def movement(self,new_position):
        self.position = new_position
        self.room = self.room_list[new_position]

    def catch_danger(self,danger):
        self.danger=danger
        return danger

class Arrow():
    """See Player class"""
    def __init__(self, position,room_list_arrow):
        self.position = position
        self.room = room_list_arrow[position]
        self.room_list_arrow = room_list_arrow
     
    def movement(self,new_room):
        self.position = new_room
        self.room = self.room_list_arrow[new_room]

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

def highscore_sorting(highscore_obj):
    highscore_sort = sorted(highscore_obj, key = attrgetter("score"),reverse = True)
    
    return highscore_sort


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

def active_difficulty():
    """Interperter for active difficulty"""
    file= open(os.path.dirname(os.path.realpath(__file__))+"\\difficulty.txt", "r")
    difficulty=int(file.readline())
    if difficulty == 1:
        return "Easy"
    elif difficulty == 2:
        return "Normal"
    elif difficulty == 3:
        return "Expert"
    

def read_highscore():
    """Reads the highscore information from file and appends different attributes to a list"""
    highscore = open(os.path.dirname(os.path.realpath(__file__))+ "\\highscore.txt")
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

def show_highscore():
    """The GUI for the Highscore window"""
    top2 = Toplevel(takefocus=True)
    top2.title("Highscore")
    top2.after(1000, lambda: top2.focus_force())
    top2.wm_attributes("-topmost", 1)
    top2.configure(background='black')
    top2.geometry=("400x1200")

    photo = PhotoImage(file=os.path.dirname(os.path.realpath(__file__))+"\\wumpus_hunter1.gif")

    highscore_string=("%10s" %"Name:" + "%7s" %"Moves:" + "%8s" %"Arrows:" +"%7s"  %"Diff:" +"%8s"  %"Score:")

    label = Label(top2,image=photo)
    label.image = photo # keep a reference!
    label.pack(side="top")
    Message(top2, text=("Highscore"),font=("Lucia Grande" ,20), foreground = "red" , background="black", width=200).pack(side="top")
    #Message(top2, text=("RRRRRR"),font=("Lucia Grande" ,100), foreground = "black" , background="black", width=400).grid(column=2,row=20)
    highscore_sort=highscore_sorting(read_highscore())
    Message(top2, text=("%6s" %" "+highscore_sort[0].name+" has the current highscore!!"),font=("Lucia Grande" ,20),width=400, foreground = "red" , background="black").pack(side="top")
    Message(top2, text=(highscore_string),font=("Lucia Grande" ,15),width=400, foreground = "red" , background="black").pack(side="top")
    for a in range(0,9):
        Message(top2, text=(highscore_sort[a]),font=("Lucia Grande" ,15), foreground = "red" , background="black",width=400).pack(side="top")




#The difficulty saves/reads to a file, since this operation is only done when switching difficulty it doesn't take unnecessary memory.
def save_difficulty(diff):
        file = open(os.path.dirname(os.path.realpath(__file__))+"\\difficulty.txt", "w" )
        file.write(diff)
        
def read_difficulty():
    file= open(os.path.dirname(os.path.realpath(__file__))+ "\\difficulty.txt", "r")
    difficulty=int(file.readline())
    return difficulty


def difficulty():
    """The GUI for the Difficulty window"""
    top4 = Toplevel(takefocus=True)
    top4.title("Instructions")
    top4.after(1000, lambda: top4.focus_force())
    top4.wm_attributes("-topmost", 1)
    top4.configure(background='black')
    top4.geometry=("400x1200")

    photo = PhotoImage(file=os.path.dirname(os.path.realpath(__file__))+"\\wumpus_hunter1.gif")

    label = Label(top4,image=photo)
    label.image = photo # keep a reference!
    label.pack()
    diff_var = IntVar()
    diff_var.set(2)

    Message(top4, text=("Difficulty:"),font=("Lucia Grande" ,18), foreground = "red" , background="black", width=200).pack(side="top")
    Easy_button = Radiobutton(top4,variable=diff_var,value=1,highlightbackground="red",foreground = "red",highlightcolor="red",background="green",height=2,width=10,command=lambda: save_difficulty(str(1)), text="Easy").pack(side="top")
    Normal_button = Radiobutton(top4,variable=diff_var,value=2,highlightbackground="red",foreground = "red",highlightcolor="red",background="orange",height=2,width=10,command=lambda: save_difficulty(str(2)), text="Normal").pack(side="top")
    Hard_button = Radiobutton(top4,variable=diff_var,value=3,highlightbackground="red",foreground = "red",highlightcolor="red",background="red",height=2,width=10,command=lambda: save_difficulty(str(3)), text="Expert").pack(side="top")



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



def wumpus_position_easy_normal(danger_list):
    """Sees to that wumpus is identified att the right position when he's not moving ( easy and normal)"""
    for a in range(0,20):
        if danger_list[a] == 3:
            index = a 
    return index

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
    #shuffled list 0-19
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


def check_danger_close():
    """Checks for nearby dangers"""
    new_dangerlist=[]
    danger = run1.room[run1.player1.position].danger_close
    if 1 in danger:
        new_dangerlist.append(1)
    if 2 in danger:
        new_dangerlist.append(2)
    if ((run1.wumpus1.position == run1.room[run1.player1.position].north) or (run1.wumpus1.position == run1.room[run1.player1.position].south) or (run1.wumpus1.position == run1.room[run1.player1.position].east) or (run1.wumpus1.position == run1.room[run1.player1.position].west)) or (3 in danger):
        new_dangerlist.append(3)
    return new_dangerlist




def consequence(what_danger):
    """1. Reads information for the run objects
       2. processes the infomation and takes the appropriate action
       3. Returns new information to run/player class"""
    if run1.which_danger != 0:

        if what_danger == 1:
            #Adds a random danger, but not a bottomless hole or wumpus instead of bat. Can be bat (1) again.
            run1.room[run1.player1.position].danger = choice([0,1,1,1,7,8])
            run1.player1.position = random.randrange(0,20)
            run1.player1.room = run1.room_list[run1.player1.position]

        elif (run1.which_danger == 2) or (run1.which_danger==3):
            game_over()

        elif what_danger == 8:
            run1.player1.arrowsleft += 1
            run1.room[run1.player1.position].danger = 0

        elif what_danger == 7:
            if run1.player1.arrowsleft >= 0:
                run1.player1.arrowsleft -= 1
            run1.room[run1.player1.position].danger = 0
            
        elif what_danger == 9:
            run1.wumpus1.position = run1.player1.position +1
            if run1.wumpus1.position == 20:
                run1.wumpus1.position = 19
            run1.room[run1.player1.position].danger = choice([0,1,1,1,7,8])
            
        else:
            pass




def wumpus_danger(which_danger):
    """Gives the correct information when walking into the same room as wumpus"""
    if (run1.player1.position == run1.wumpus1.position) and (run1.wdiff == 3):
        which_danger=3
    return which_danger


def move(direction,current_position):
    """Interprets the information given from the user"""

    if (direction.upper() == "N"):
        run1.player1.movement(run1.room[current_position].north)
    elif (direction.upper() == "S"):
        run1.player1.movement(run1.room[current_position].south)
    elif (direction.upper() == "E"):
        run1.player1.movement(run1.room[current_position].east)
    elif (direction.upper() == "W"):
        run1.player1.movement(run1.room[current_position].west)

    run1.which_danger=int(run1.player1.catch_danger(run1.room[run1.player1.position].danger))
    run1.which_danger = wumpus_danger(run1.which_danger)
    consequence(run1.which_danger)
    

def shoot_code(direction):
    """1. Is gives direction from the user
       2. If 3 arrows has already been shot, it will remove an arrow. Sends the information to shoot_action()
       3. returns nothing """

    if run1.arrow_count == 3:
        run1.player1.arrowsleft -=1
        run1.arrow_count=0
        run1.arrow1.position = run1.player1.position 
        run1.arrow1.room     = run1.room_list[run1.player1.position]
    elif run1.arrow_count==0 :
        run1.arrow1.position = run1.player1.position 
        run1.arrow1.room     = run1.room_list[run1.player1.position]


    shoot_action(direction)
    run1.arrow_count+=1
    
def shoot_action(direction):
    """1. Takes in direction from user input
       2. Will send the direction to the interpreter and check if you have won or lost
       3. returns values to the run object"""


    run1.win=False
    #Sends player input to interpreter, see function shoot
    run1.event_string=("The arrow is leaving room "+str(run1.arrow1.room)+" in what direction?[N,S,E,W]? You have " +str((3-run1.arrow_count))+" curves left!")
    shoot(direction, run1.arrow1.position)
    #If Wumpus gets hit the loop is broken, If you curve the arrow back at yourself the loop is broken
    if (run1.arrow1.position == run1.wumpus1.position):
        run1.which_danger = 4
        win()
    elif (run1.arrow1.position == run1.player1.position):
        run1.which_danger=5
        game_over()
    elif (run1.wumpus1.position==run1.player1.position):
        run1.which_danger = 2
        game_over()
        

def shoot(direction,current_position):
    """Interprets the information given from the user"""


    print(run1.player1.arrowsleft)

    if (direction.upper() == "N") :
        run1.arrow1.movement(run1.room[current_position].north)
    elif (direction.upper() == "S"):
        run1.arrow1.movement(run1.room[current_position].south)
    elif (direction.upper() == "E"):
        run1.arrow1.movement(run1.room[current_position].east)
    elif (direction.upper() == "W"):
        run1.arrow1.movement(run1.room[current_position].west)







def gameplay():
    """The gameplay window, contains teh GUI for gameplay with buttons and messages"""
    global top3
    top3 = Toplevel(takefocus=True)
    top3.title("Instructions")
    top3.after(1000, lambda: top3.focus_force())
    top3.wm_attributes("-topmost", 1)
    top3.configure(background='black')
    top3.geometry=("400x1200")
    top3.columnconfigure(0, minsize=350)
    top3.columnconfigure(1, minsize=350)
    top3.columnconfigure(2, minsize=350)
    top3.rowconfigure(2, minsize=150)
    top3.rowconfigure(3, minsize=50)




    startup()

    photo = PhotoImage(file=os.path.dirname(os.path.realpath(__file__))+"\\wumpus_hunter1.gif")

    label = Label(top3,image=photo)
    label.image = photo # keep a reference!
    label.grid(column=1,row=0)
    run1.update_strings()
    enviromental_string = StringVar()
    enviromental_string.set(run1.enviromental_string)
    event_string = StringVar()
    event_string.set(run1.event_string)
    info_string = StringVar()
    info_string.set(run1.info_string)
    room_string = StringVar()
    room_string.set(run1.room_string)


  

        

    shootormove = StringVar()
    shootormove.set("M")

    Message(top3, text=("Enviromental Info:"),font=("Lucia Grande" ,20), foreground = "red" , background="black", width=300).grid(column=0,row=1,sticky=W)
    Message(top3, textvariable=enviromental_string,font=("Lucia Grande" ,14), foreground = "red" , background="black", width=300).grid(column=0,row=2,sticky=N)
    Message(top3, textvariable=info_string,font=("Lucia Grande" ,20), foreground = "white" , background="black", width=300).grid(column=1,row=2,sticky=N)
    Message(top3, text=("Event:"),font=("Lucia Grande" ,20), foreground = "red" , background="black", width=300).grid(column=2,row=1)
    Message(top3, textvariable=event_string,font=("Lucia Grande" ,14), foreground = "red" , background="black", width=300).grid(column=2,row=2,sticky=N)
    Message(top3, text=("Nearby Rooms:"),font=("Lucia Grande" ,18), foreground = "red" , background="black", width=300).grid(column=1,row=4,sticky=N)
    Message(top3, textvariable=room_string,font=("Lucia Grande" ,16), foreground = "red" , background="black", width=300).grid(column=1,row=5,sticky=N)
    

    shoot_button = Radiobutton(top3,variable=shootormove,value = "S",highlightbackground="red",foreground = "orange",highlightcolor="red",background="orange", text="Shoot").grid(column=1,row=10,sticky=S)
    move_button  = Radiobutton(top3,variable=shootormove,value = "M",highlightbackground="red",foreground = "green",background="green",highlightcolor="green", text="Move ").grid(column=1,row=10,sticky=N)
    button_west = Button(top3, text="West",highlightbackground="black",bd="4",command = lambda: (execute("W",shootormove.get()),enviromental_string.set(run1.enviromental_string),event_string.set(run1.event_string),info_string.set(run1.info_string),room_string.set(run1.room_string)) ,font=("Lucia Grande" ,15),width=12,relief="raised").grid(column=0,row=10)
    button_east = Button(top3, text="East",highlightbackground="black",bd="4",command = lambda: (execute("E",shootormove.get()),enviromental_string.set(run1.enviromental_string),event_string.set(run1.event_string),info_string.set(run1.info_string),room_string.set(run1.room_string)),height=3,font=("Lucia Grande" ,15),width=12,relief="raised").grid(column=2,row=10)
    button_north = Button(top3, text="North",highlightbackground="black",bd="4",command = lambda: (execute("N",shootormove.get()),enviromental_string.set(run1.enviromental_string),event_string.set(run1.event_string),info_string.set(run1.info_string),room_string.set(run1.room_string)),font=("Lucia Grande" ,15),width=12,relief="raised").grid(column=1,row=8,sticky=S)
    button_south = Button(top3, text="South",highlightbackground="black",bd="4",command = lambda: (execute("S",shootormove.get()),enviromental_string.set(run1.enviromental_string),event_string.set(run1.event_string),info_string.set(run1.info_string),room_string.set(run1.room_string)),font=("Lucia Grande" ,15),width=12,relief="raised").grid(column=1,row=12,sticky=N)


	

def execute(direction,shootormove):
    """1. Takes in user input from button clicks
       2. Interprets user input as shoot or move
       3. sends through information to shoot or move functions"""
    if shootormove == "M":
        run1.highscore_moves+=1
        if run1.arrow_count != 0:
            run1.arrow_count = 0
            run1.player1.arrowsleft -=1
            run1.arrow1.position = 666
        move(direction,run1.player1.position)
        run1.update_strings()
    elif (shootormove == "S") and (run1.player1.arrowsleft > 0):
        if run1.arrow_count == 3:
            run1.wumpus1.move()
        run1.update_enviromental_info()
        shoot_code(direction)
    elif (shootormove == "S") and (run1.player1.arrowsleft == 0):
        run1.event_string=("You are out of arrows!!!")



def win():

    """The GUI popup when win, takes user input for highscore nicknames and calls function to save it to file"""
    top6 = Toplevel(takefocus=True)
    top6.title("Instructions")
    top6.after(1000, lambda: top6.focus_force())
    top6.wm_attributes("-topmost", 1)
    top6.configure(background='black')
    top6.geometry=("400x1200")

    run1.update_strings()
    top3.destroy()

    score=((300*run1.player1.arrowsleft+500*(run1.wdiff))-(40*run1.highscore_moves))
    string_score = str(score)

    e=Entry(top6)
    e.grid(column=3,row=3)
    e.focus_set()

    buttons=[]

    button_save=Button(top6, text="Save", width=10, command= lambda: (buttons[0].config(state="disabled"),save_highscore(e.get().replace(" ", ""),run1.highscore_moves,run1.player1.arrowsleft,run1.wdiff)))
    buttons.append(button_save)
    button_save.grid(column=3,row=4)
    Message(top6, text=("You WIN! Score : "+string_score),font=("Lucia Grande" ,20), foreground = "red" , background="black", width=300).grid(column=1,row=0,sticky=N)
    Message(top6, text=run1.event_string,font=("Lucia Grande" ,14), foreground = "red" , background="black", width=300).grid(column=1,row=1,sticky=N)
    Message(top6, text=("Do you want to play again?"),font=("Lucia Grande" ,16), foreground = "red" , background="black", width=300).grid(column=1,row=2,sticky=N)
    button_no = Button(top6,text="NO",highlightbackground="black",bd="4",command = lambda: top6.destroy()).grid(column=2,row=3,sticky=N)
    button_yes = Button(top6,text="YES",highlightbackground="black",bd="4",command = lambda:  gameplay()==None & top6.destroy()==None).grid(column=0,row=3,sticky=N)
    button_close = Button(top6,text="CLOSE",highlightbackground="black",bd="4",command = lambda: top6.destroy()).grid(column=1,row=3,sticky=N)
    
def game_over():
    """The GUI when losing"""

    top5 = Toplevel(takefocus=True)
    top5.title("Instructions")
    top5.after(1000, lambda: top5.focus_force())
    top5.wm_attributes("-topmost", 1)
    top5.configure(background='black')
    top5.geometry=("400x1200")

    run1.update_strings()
    top3.destroy()

    Message(top5, text=("GAME OVER"),font=("Lucia Grande" ,20), foreground = "red" , background="black", width=300).grid(column=1,row=0,sticky=N)
    Message(top5, text=run1.event_string,font=("Lucia Grande" ,14), foreground = "red" , background="black", width=300).grid(column=1,row=1,sticky=N)
    Message(top5, text=("Do you want to play again?"),font=("Lucia Grande" ,16), foreground = "red" , background="black", width=300).grid(column=1,row=2,sticky=N)
    button_south = Button(top5,text="NO",highlightbackground="black",bd="4",command = lambda: top5.destroy()).grid(column=2,row=3,sticky=N)
    button_south = Button(top5,text="YES",highlightbackground="black",bd="4",command = lambda:  gameplay()==None & top5.destroy()==None).grid(column=0,row=3,sticky=N)
    button_south = Button(top5,text="CLOSE",highlightbackground="black",bd="4",command = lambda: top5.destroy()).grid(column=1,row=3,sticky=N)





def instructions():

    """The GUI for instructions"""
    top1 = Toplevel(takefocus=True)
    top1.title("Instructions")
    top1.after(1000, lambda: top1.focus_force())
    top1.wm_attributes("-topmost", 1)
    top1.configure(background='black')

    photo = PhotoImage(file=os.path.dirname(os.path.realpath(__file__))+"\\wumpus_hunter1.gif")

    label = Label(top1,image=photo)
    label.image = photo # keep a reference!
    label.pack(side="top")

    #logo1 = PhotoImage(file="wumpus_hunter1.gif")
    #w1=Label(top1, 
    #compound = CENTER, 
    #image=logo1).pack(side="top")

    msg0 = Message(top1, text="Instructions",font=("Lucia Grande" ,20), foreground = "red" , background="black",width=200).pack(side="top")

    msg1 = Message(top1, text="""
        
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

    Good Luck!""", foreground = "blue" ,background="black").pack(side="left")


    Button(top1,highlightbackground="black", text="Close", command=top1.destroy).pack(side="bottom")
	



photo = PhotoImage(file=os.path.dirname(os.path.realpath(__file__))+"\\wumpus_hunter.gif")

label = Label(root,image=photo)
label.image = photo # keep a reference!
label.pack(side="top")

button_wumpus = Button(root, text="Play Wumpus",highlightbackground="black",bd="4",command=lambda: gameplay(),font=("Lucia Grande" ,15),width=16,relief="raised").pack()
button_difficulty = Button(root, text="Change Difficulty",highlightbackground="black",bd="4",command=lambda:difficulty(),font=("Lucia Grande" ,15),width=16,relief="raised").pack()
button_highscore = Button(root, text="Higscore",highlightbackground="black",command=lambda:show_highscore(),bd="4",font=("Lucia Grande" ,15),width=16,relief="raised").pack()
button_instructions = Button(root, text="Instructions",highlightbackground="black",bd="4",command=lambda: instructions(),font=("Lucia Grande" ,15),width=16,relief="raised").pack()
button_exit = Button(root, text="Exit",highlightbackground="black",bd="4",font=("Lucia Grande" ,15),command=lambda: sys.exit(),width=16,relief="raised").pack()



root.mainloop()



