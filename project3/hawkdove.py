import random
import tkinter
random.seed()

def plot(xvals, yvals):
    # This is a function for creating a simple scatter plot.  You will use it,
    # but you can ignore the internal workings.
    root = tkinter.Tk()
    c = tkinter.Canvas(root, width=700, height=400, bg='white') #was 350 x 280
    c.grid()
    #create x-axis
    c.create_line(50,350,650,350, width=3)
    for i in range(5):
        x = 50 + (i * 150)
        c.create_text(x,355,anchor='n', text='%s'% (.5*(i+2) ) )
    #y-axis
    c.create_line(50,350,50,50, width=3)
    for i in range(5):
        y = 350 - (i * 75)
        c.create_text(45,y, anchor='e', text='%s'% (.25*i))
    #plot the points
    for i in range(len(xvals)):
        x, y = xvals[i], yvals[i]
        xpixel = int(50 + 300*(x-1))
        ypixel = int(350 - 300*y)
        c.create_oval(xpixel-3,ypixel-3,xpixel+3,ypixel+3, width=1, fill='red')
    root.mainloop()

#Constants: setting these values controls the parameters of your experiment.
injurycost = 10 #Cost of losing a fight  
displaycost = 1 #Cost of displaying   
foodbenefit = 8 #Value of the food being fought over   
init_hawk = 0
init_dove = 0
init_defensive = 0
init_evolving = 150

########
# Your code here
########

class World:
    def __init__(self):
        self.birdlist = []
    def update(self):
        for bird in self.birdlist:
            bird.update()
    def free_food(self, foodcount):
        while foodcount > 0:
            birdchoice = random.randint(0, (len(self.birdlist) - 1))
            self.birdlist[birdchoice].eat()
            foodcount -= 1
    def conflict(self, foodcount):
        while foodcount > 0:
            birdchoice1 = random.randint(0, (len(self.birdlist) - 1))
            birdchoice2 = random.randint(0, (len(self.birdlist) - 1))
            while birdchoice1 == birdchoice2:
                birdchoice2 = random.randint(0, (len(self.birdlist) - 1))
            bird1 = self.birdlist[birdchoice1]
            bird2 = self.birdlist[birdchoice2]
            bird1.encounter(bird2)
            foodcount -= 1
    def status(self):
        birds = {}
        for bird in self.birdlist:
            if bird.species in birds:
                birds[bird.species] += 1
            else:
                birds[bird.species] = 1
        for species in birds:
            print(species+'s remaining: '+str(birds[species]))
    def evolvingPlot(self):
        xweight = []
        yaggression = []
        for bird in self.birdlist:
            if bird.species == 'Evolving bird':
                xweight.append(bird.weight)
                yaggression.append(bird.aggression)
        plot(xweight, yaggression)

class Bird:
    def __init__(self, world):
        world.birdlist.append(self)
        self.world = world
        self.health = 100
    def eat(self):
        self.health += foodbenefit
    def injured(self):
        self.health -= injurycost
    def display(self):
        self.health -= displaycost
    def die(self):
        self.world.birdlist.remove(self)
    def update(self):
        self.health -= 1
        if self.health <= 0:
            self.die()

class Dove(Bird):
    species = 'Dove'
    def update(self):
        Bird.update(self)
        if self.health >= 200:
            self.health -= 100
            Dove(self.world)
    def defend_choice(self):
        return False
    def encounter(self, opponent):
        opponentdefends = opponent.defend_choice()
        if opponentdefends:
            opponent.eat()
        else:
            self.display()
            opponent.display()
            winner = random.randint(0, 1)
            if winner:
                self.eat()
            else:
                opponent.eat()

class Hawk(Bird):
    species = 'Hawk'
    def update(self):
        Bird.update(self)
        if self.health >= 200:
            self.health -= 100
            Hawk(self.world)
    def defend_choice(self):
        return True
    def encounter(self, opponent):
        opponentdefends = opponent.defend_choice()
        if not opponentdefends:
            self.eat()
        else:
            winner = random.randint(0, 1)
            if winner:
                opponent.injured()
                self.eat()
            else:
                self.injured()
                opponent.eat()

class Defensive(Bird):
    species = 'Defensive bird'
    def update(self):
        Bird.update(self)
        if self.health >= 200:
            self.health -= 100
            Defensive(self.world)
    def defend_choice(self):
        return True
    def encounter(self, opponent):
        opponentdefends = opponent.defend_choice()
        if opponentdefends:
            opponent.eat()
        else:
            self.display()
            opponent.display()
            winner = random.randint(0, 1)
            if winner:
                self.eat()
            else:
                opponent.eat()

class Evolving(Bird):
    species = 'Evolving bird'
    def __init__(self, world, parentaggression = None, parentweight = None):
        Bird.__init__(self, world)
        self.parentaggression = parentaggression
        self.parentweight = parentweight
        if self.parentaggression == None:
            self.parentaggression = random.uniform(0, 1)
        if self.parentweight == None:
            self.parentweight = random.uniform(1, 3)
        self.aggression = self.parentaggression + random.uniform(-0.05, 0.05)
        if self.aggression < 0:
            self.aggression = 0
        elif self.aggression > 1:
            self.aggression = 1
        self.weight = self.parentweight + random.uniform(-0.1, 0.1)
        if self.weight < 1:
            self.weight = 1
        elif self.weight > 3:
            self.weight = 3
    def update(self):
        self.health -= (0.4 + (0.6 * self.weight))
        if self.health <= 0:
            self.die()
        if self.health >= 200:
            self.health -= 100
            Evolving(self.world, self.aggression, self.weight)
    def defend_choice(self):
        if random.random() >= self.aggression:
            return False
        else:
            return True
    def encounter(self, opponent):
        selffights = self.defend_choice()
        opponentfights = opponent.defend_choice()
        if selffights:
            if opponentfights:
                winchance = self.weight / (self.weight + opponent.weight)
                winner = (random.random() < winchance)
                if winner:
                    opponent.injured()
                    self.eat()
                else:
                    self.injured()
                    opponent.eat()
            else:
                self.eat()
        else:
            if opponentfights:
                opponent.eat()
            else:
                self.display()
                opponent.display()
                winner = random.randint(0, 1)
                if winner:
                    self.eat()
                else:
                    opponent.eat()

########
# The code below actually runs the simulation.  You shouldn't have to do anything to it.
########
w = World()
for i in range(init_dove):
    Dove(w)
for i in range(init_hawk):
    Hawk(w)
for i in range(init_defensive):
    Defensive(w)
for i in range(init_evolving):
    Evolving(w)

for t in range(10000):
    w.free_food(10) 
    w.conflict(50)
    w.update()
    #print('Cycle '+str(t)+' finished.') #Debug line
w.status()
w.evolvingPlot()  #This line adds a plot of evolving birds. Uncomment it when needed.


