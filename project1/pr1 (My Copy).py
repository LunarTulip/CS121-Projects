import random #Imports a library, presumably one used for generation of pseudo-random numbers
import math #Imports a library with advanced math operations
import pr1testing #Imports a library, possibly from the file system rather than the cloud?
random.seed() #Defines a seed for pseudo-random operations based on the computer clock

#Note for future readers: before even starting to add my own code, I systematically commented up the preexisting code.

def roll(): #Function that rolls 1 6-sided die, returning an integer between 0 and 5
    return random.randint(0,5) #Rolls 1d6-1

def play(): #Function which plays the game
    player1 = input("Name of Player 1?") #Defines Player 1's name
    player2 = input("Name of Player 2?") #Defines Player 2's name
    score1 = 0 #Zeros Player 1's score
    score2 = 0 #Zeros Player 2's score
    last = False #Labels that the game isn't in "make final move before the end" mode
    while True: #Starts a loop which ends when the game ends
        print() #Prints a blank line
        print(player1 + ": " + str(score1) + "   " + player2 + ": " + str(score2)) #Prints both players' scores
        print('It is', player1 + "'s turn.") #States that it's Player 1's turn
        numDice = int(input("How many dice do you want to roll?")) #Player 1 inputs an integer number of dice to roll
        diceTotal = 0 #Says that the dice's value before rolling is 0
        diceString = "" #Says that the list of values rolled is the empty string
        i = numDice #Defines the number of dice to roll
        while i > 0: #Starts a loop which ends when Player 1 has run out of dice to roll
            d = roll() #Uses the roll function defined above to roll 1d6-1
            diceTotal += d #Adds the roll to the total number of points the player gains this turn
            diceString = diceString + " "  + str(d) #Adds the roll to the list of values of dice rolled this turn
            i = i-1 #Reduces the number of dice to roll by one
        print("Dice rolled: ", diceString) #Lists the values of all dice rolled this turn
        print("Total for this turn: ", str(diceTotal)) #Lists the total value of dice rolled this turn
        score1 += diceTotal #Increases Player 1's score by the value of the dice they rolled this turn
        if score1 > 100 or last: #If the game is supposed to end at this point...
            break #Ends the loop
        if numDice == 0: #If Player 1 rolled 0 dice...
            last = True #Marks a trigger for the game to end after Player 2's next turn
        print() #Prints a blank line
        print(player1 + ": " + str(score1) + "   " + player2 + ": " + str(score2)) #Prints both players' scores
        print('It is', player2 + "'s turn.") #States that it's Player 2's turn
        numDice = int(input("How many dice do you want to roll?")) #Player 2 inputs an integer number of dice to roll
        diceTotal = 0 #Says that the dice's value before rolling is 0
        diceString = "" #Says that the list of values rolled is the empty string
        i = numDice #Defines the number of dice to roll
        while i > 0: #Starts a loop which ends when Player 2 has run out of dice to roll
            d = roll() #Uses the roll function defined above to roll 1d6-1
            diceTotal += d #Adds the roll to the total number of points the player gains this turn
            diceString = diceString + " "  + str(d) #Adds the roll to the list of values of dice rolled this turn
            i = i-1 #Reduces the number of dice to roll by one
        print("Dice rolled: ", diceString) #Lists the values of all dice rolled this turn
        print("Total for this turn: ", str(diceTotal)) #Lists the total value of dice rolled this turn
        score2 += diceTotal #Increases Player 2's score by the value of the dice they rolled this turn
        if score2 > 100 or last: #If the game is supposed to end at this point...
            break #Ends the loop
        if numDice == 0: #If Player 2 rolled 0 dice...
            last = True #Marks a trigger for the game to end after Player 1's next turn
    print(player1 + ": " + str(score1) + "   " + player2 + ": " + str(score2)) #Prints both players' scores
    if score1 > 100: #If Player 1 has gone over 100 points...
        print(player2 + " wins.") #Prints that Player 2 wins
        return 2 #Returns that Player 2 wins
    elif score2 > 100: #Otherwise, if Player 2 has gone over 100 points...
        print(player1 + " wins.") #Prints that Player 1 wins
        return 1 #Returns that Player 1 wins
    elif score1 > score2: #Otherwise, if Player 1 has more points than Player 2...
        print(player1 + " wins.") #Prints that Player 1 wins
        return 1 #Returns that Player 1 wins
    elif score2 > score1: #Otherwise, if Player 2 has more points than Player 1...
        print(player2 + " wins.") #Prints that Player 2 wins
        return 2 #Returns that Player 2 wins
    else:
        print("Tie.") #Otherwise, print that it was a tie
        return 3 #Return that it was a tie

def autoplayLoud(strat1, strat2): #Function which has two AI strategies play the game and displays their moves
    score1, score2 = 0, 0 #Zeros the players' scores
    last = False #Ensures that the game doesn't end after the first move
    while True: #Starts a loop which doesn't end until I tell it to
        print() #Prints a blank line
        print("Player 1: "+str(score1)+"   Player 2: "+str(score2)) #Prints both players' scores
        print("It is Player 1's turn.") #Says that it's Player 1's turn
        numDice = strat1(score1, score2, last) #Player 1 selects how many dice to roll.
        diceTotal = 0 #Zeros the roll's value
        diceString = "" #Empties the list of rolls
        i = numDice #Defines the number of dice to roll
        while i > 0: #Starts a loop which ends when all the dice have been rolled
            d = roll() #Rolls 1d6-1
            diceTotal += d #Tracks the total points gained across all rolls this turn
            diceString = diceString+" "+str(d) #Adds the number rolled this turn to the list of numbers rolled this turn
            i = i-1 #Redefines the number of dice to roll to be one lower
        print(str(numDice)+" dice chosen.") #Says how many dice Player 1 rolled
        print("Dice rolled:"+diceString) #Lists the individual values of the dice Player 1 rolled; no space after the colon because diceString starts with a space
        print("Total for this turn: "+str(diceTotal)) #Says how many points Player 1 got from its rolls
        score1 += diceTotal #Increases Player 1's score by the combined value of its rolls this turn
        if score1 > 100 or last: #If the game is supposed to end at this point...
            break #The game ends
        if numDice == 0: #If Player 1 passes this turn...
            last = True #Marks a trigger for the game to end after Player 2's next turn
        print() #Prints a blank line
        print("Player 1: "+str(score1)+"   Player 2: "+str(score2)) #Prints both players' scores
        print("It is Player 2's turn.") #Says that it's Player 2's turn
        numDice = strat2(score2, score1, last) #Player 2 selects how many dice to roll.
        diceTotal = 0 #Zeros the roll's value
        diceString = "" #Empties the list of rolls
        i = numDice #Defines the number of dice to roll
        while i > 0: #Starts a loop which ends when all the dice have been rolled
            d = roll() #Rolls 1d6-1
            diceTotal += d #Tracks the total points gained across all rolls this turn
            diceString = diceString+" "+str(d) #Adds the number rolled this turn to the list of numbers rolled this turn
            i = i-1 #Redefines the number of dice to roll to be one lower
        print(str(numDice)+" dice chosen.") #Says how many dice Player 2 rolled
        print("Dice rolled: "+diceString) #Lists the individual values of the dice Player 2 rolled
        print("Total for this turn: "+str(diceTotal)) #Says how many points Player 2 got from its rolls
        score2 += diceTotal #Increases Player 2's score by the combined value of its rolls this turn
        if score2 > 100 or last: #If the game is supposed to end at this point...
            break #The game ends
        if numDice == 0: #If Player 2 passes this turn...
            last = True #Marks a trigger for the game to end after Player 1's next turn
    print("Player 1: "+str(score1)+"   Player 2: "+str(score2)) #Prints both players' scores
    if score1 > 100: #If Player 1 has gone over 100 points...
        print("Player 2 wins.") #Prints that Player 2 wins
    elif score2 > 100: #Otherwise, if Player 2 has gone over 100 points...
        print("Player 1 wins.") #Prints that Player 1 wins
    elif score1 > score2: #Otherwise, if Player 1 has more points than Player 2...
        print("Player 1 wins.") #Prints that Player 1 wins
    elif score2 > score1: #Otherwise, if Player 2 has more points than Player 1...
        print("Player 2 wins.") #Prints that Player 2 wins
    else:
        print("Tie.") #Otherwise, print that it was a tie

def autoplay(strat1, strat2): #Copy of autoplayLoud, except the Print lines are gone and it returns a value at the end
    score1, score2 = 0, 0 #Zeros the players' scores
    last = False #Ensures that the game doesn't end after the first move
    while True: #Starts a loop which doesn't end until I tell it to
        numDice = strat1(score1, score2, last) #Player 1 selects how many dice to roll.
        diceTotal = 0 #Zeros the roll's value
        diceString = "" #Empties the list of rolls
        i = numDice #Defines the number of dice to roll
        while i > 0: #Starts a loop which ends when all the dice have been rolled
            d = roll() #Rolls 1d6-1
            diceTotal += d #Tracks the total points gained across all rolls this turn
            diceString = diceString+" "+str(d) #Adds the number rolled this turn to the list of numbers rolled this turn
            i = i-1 #Redefines the number of dice to roll to be one lower
        score1 += diceTotal #Increases Player 1's score by the combined value of its rolls this turn
        if score1 > 100 or last: #If the game is supposed to end at this point...
            break #The game ends
        if numDice == 0: #If Player 1 passes this turn...
            last = True #Marks a trigger for the game to end after Player 2's next turn
        numDice = strat2(score2, score1, last) #Player 2 selects how many dice to roll.
        diceTotal = 0 #Zeros the roll's value
        diceString = "" #Empties the list of rolls
        i = numDice #Defines the number of dice to roll
        while i > 0: #Starts a loop which ends when all the dice have been rolled
            d = roll() #Rolls 1d6-1
            diceTotal += d #Tracks the total points gained across all rolls this turn
            diceString = diceString+" "+str(d) #Adds the number rolled this turn to the list of numbers rolled this turn
            i = i-1 #Redefines the number of dice to roll to be one lower
        score2 += diceTotal #Increases Player 2's score by the combined value of its rolls this turn
        if score2 > 100 or last: #If the game is supposed to end at this point...
            break #The game ends
        if numDice == 0: #If Player 2 passes this turn...
            last = True #Marks a trigger for the game to end after Player 1's next turn
    if score1 > 100: #If Player 1 has gone over 100 points...
        return 2 #Returns that Player 2 wins
    elif score2 > 100: #Otherwise, if Player 2 has gone over 100 points...
        return 1 #Returns that Player 1 wins
    elif score1 > score2: #Otherwise, if Player 1 has more points than Player 2...
        return 1 #Returns that Player 1 wins
    elif score2 > score1: #Otherwise, if Player 2 has more points than Player 1...
        return 2 #Returns that Player 2 wins
    else:
        return 3 #Returns that it was a tie

def manyGames(strat1, strat2, n): #Runs autoplay betweeen strat1 and strat2 n times and reports win counts
    p1wins, p2wins, ties = 0, 0, 0 #Zeros all win counts
    i = n #Defines the number of games to run
    while i > 0: #Loops until it's run n games
        if i % 2 == 1: #if there's an odd number of games remaining...
            outcome = autoplay(strat1, strat2) #Run a game with strat1 going first
            if outcome == 1: #If strat1 wins...
                p1wins += 1 #Mark down a win for strat1
            elif outcome == 2: #If strat2 wins...
                p2wins += 1 #Mark down a win for strat2
            elif outcome == 3: #If the players tie...
                ties += 1 #Mark down a tie
        else: #If there's a not-odd number of games remaining (in practice even because i should always be an integer)...
            outcome = autoplay(strat2, strat1) #Run a game with strat2 going first
            if outcome == 1: #If strat2 wins...
                p2wins += 1 #Mark down a win for strat2
            elif outcome == 2: #If strat1 wins...
                p1wins += 1 #Mark down a win for strat1
            elif outcome == 3: #If the players tie...
                ties += 1 #Mark down a tie
        i -= 1 #Reduces the count of games to run by one
        #print("1: "+str(p1wins)+"  2: "+str(p2wins)+"  3: "+str(ties)) #Debug line to see intermediate score counts
    print("Player 1 wins: "+str(p1wins)) #Prints how many times strat1 wins
    print("Player 2 wins: "+str(p2wins)) #Prints how many times strat2 wins
    print("Ties:          "+str(ties)) #Prints how many times they tie

def sample1(myscore, theirscore, last): #First sample strategy. Super-weak.
    if myscore > theirscore: #If my score is higher than my opponent's...
        return 0 #Pass.
    else: #If my score isn't higher than my opponent's...
        return 12 #Roll 12 dice.

def sample2(myscore, theirscore, last): #Second sample strategy. Still not great, but better than the first.
    if myscore <= 50: #If my score is under 51...
        return 30 #Roll 30 dice.
    elif myscore <= 80: #Otherwise, if my score is under 81...
        return 10 #Roll 10 dice.
    else: #If my score is above 80...
        return 0 #Pass.

def improve(strat1): #Given a strategy, returns that strategy modified to always pass when its score is 100
    def improved(myscore, theirscore, last): #Defines the new strategy to be output
        if myscore == 100: #If my score is 100...
            return 0 #Pass.
        else: #If my score isn't 100...
            return strat1(myscore, theirscore, last) #Do exactly the same thing the input strategy would do.
    return improved #Returns the new strategy-which-always-passes-at-100

def myStrategy(myscore, theirscore, last): #The best strategy I could come up with. Beats all test strategies given large n, plus beats my other strategies-able-to-beat-all-test-strategies-given-large-n given large n.
    leeway = 100 - myscore #Establishes how many points I can gain without losing. Useful in further calculations.
    if last: #If the opponent rolled 0 the previous turn, figures out optimal response. As far as I can tell, my setup here places me at the theoretical maximum possible win:loss ratio; I can't see any areas in which it gets less than the maximum possible win% for a given set of scores.
        if theirscore > myscore: #If their score is higher than mine, calculates the midpoint between their score and 100, then rolls the number of dice whose expected value is closest to that midpoint.
            theirlead = theirscore - myscore #Establishes gap between their score and mine.
            errormargin = leeway - theirlead #Establishes gap between their score and 100. Uses a slightly roundabout method to do so, but since leeway is 100 - myscore and theirlead is theirscore - myscore, the myscores cancel and the result becomes the same as 100 - theirscore.
            target = theirlead + (0.5 * errormargin) #Determines how many points I'd have to gain to be at the exact midpoint between their score and 100.
            return max(round(target / 2.5), 1) #Rolls the number of dice whose expected value (2.5 times the number rolled) will place me closest to the previously-calculated midpoint. If the midpoint less than 1.25 above my score, rolls 1 anyway, because rolling 0 has no chance of moving my score above theirs.
        elif theirscore == myscore: #If their score is equal to mine, rolls the number of dice which returns, to a first approximation, the highest ratio of wins to losses.
            saferoll = int(leeway * 0.2) #This is how many dice I can roll with absolutely no chance of going over 100.
            if myscore > 97: #If my score is above 97, any roll will have a higher chance of putting me over 100 than of putting me over my current score but not-over-100, and it's thus not worth rolling at all.
                return 0 #Rolls 0 dice for the reason described in the line above.
            elif myscore % 5 == 2 and saferoll < 4: #If my score is two above the minimum at which a given roll is safe, and I'm not rolling many dice, the probabilities add up such that the increased chance of going over 100 if I roll one die more than is safe is less than the lowered chance of rolling 0 and getting a draw, and it's thus worth adding the extra die. Starting at a roll of 4, the probabilities turn around; at 4 they change by exactly-equal amounts, and at 5 and onward the loss chance increases by more than the win chance decreases.
                return saferoll + 1 #Rolls the safe number plus one for the reason described in the line above.
            elif myscore % 5 == 1: #If my score is one above the minimum at which a given roll is safe, similar considerations apply to if it's two above, except the ratio never drops into unfavorability, at least within the bounds of the game, so there's no need to limit the saferoll values like I did when it was two above.
                return saferoll + 1 #Rolls the safe number plus one for the reason described in the line above.
            else: #If my score is neither one nor two above the minimum at which a given roll is safe, then the added risk of extra dice beyond the safe number is always equal to or greater than the added reward, so I just roll the safe number.
                return saferoll #Rolls the safe number for the reason described in the line above.
        else: #If their score is neither greater than nor equal to mine, it's below mine, so I don't need to roll anything; I'm already there.
            return 0 #Rolls 0, because there's no point in wasting processing time figuring out if other rolls are safe or not when there's no benefit to doing so.
    elif myscore == 0: #If my score is 0, I roll 33 dice, because I found through extensive testing of different possible numbers (25-35) that 33 was the spot which got me the most wins.
        return 33 #Rolls 33 for the reason described in the line above.
    elif myscore == 97 and theirscore == 97: #Ordinarily, rolling 0 given a score of 97 helps more than it hurts; however, if their score is also 97, and they're using a reasonably strong last-move strategy like mine above, they'll win more if I roll 0 than they will if I roll 1. Thus, this specific condition is an exception to the usual rolling-0-at-97-points-is-good rule. I specifically roll 1 because it's much less likely than rolling 2 would be to put me over 100 points.
        return 1 #Rolls 1 for the reason described in the line above.
    elif leeway > 3 or theirscore > myscore: #If my score is below 97, it's too easy for the opponent to catch up to me in their single remaining turn should I roll 0 (at least given a competent opponent whose score is also reasonably high), so it's in my interest to increase it further. If their score is above mine, rolling 0 guarantees me a loss, so it's similarly in my interest to increase my score. The specific number of .29 times my leeway arose from testing; I tested all numbers from .25 to .35, and .29 came out on top.
        return max(int(leeway * 0.29), 1) #Rolls .29 times my leeway (rounded down) for the reason described in the line above. If the rounding-down would lead to rolling 0, rolls 1 anyway, because I don't want to pass if I'm running this line.
    else: #If my score is 97 or above and the opponent's isn't, or my score is 98 or above and the opponent isn't above me, and it's not the last turn, rolling further would be counterproductive. The point at which rolling further is counterproductive is the point at which it becomes optimal to pass, so that's exactly what I do.
        return 0 #Rolls 0 for the reason described in the line above.

#play() #Commented out because automatically starting a human-versus-human game every time I want to test a strategy was extremely annoying. Left commented out in submission because Adam said doing so was fine, and possibly even encouraged.
#This line and everything below it is mine and not part of my answer to the official problem

def manyGamesNuanced(strat1, strat2, n): #Runs autoplay betweeen strat1 and strat2 n times and reports win counts
    p1turn1wins, p1turn2wins, p2turn1wins, p2turn2wins, p1firstties, p2firstties = 0, 0, 0, 0, 0, 0 #Zeros all win counts
    i = n #Defines the number of games to run
    while i > 0: #Loops until it's run n games
        if i % 2 == 1: #if there's an odd number of games remaining...
            outcome = autoplay(strat1, strat2) #Run a game with strat1 going first
            if outcome == 1: #If strat1 wins...
                p1turn1wins += 1 #Mark down a win for strat1
            elif outcome == 2: #If strat2 wins...
                p2turn2wins += 1 #Mark down a win for strat2
            elif outcome == 3: #If the players tie...
                p1firstties += 1 #Mark down a tie
        else: #If there's a not-odd number of games remaining (in practice even because i should always be an integer)...
            outcome = autoplay(strat2, strat1) #Run a game with strat2 going first
            if outcome == 1: #If strat2 wins...
                p2turn1wins += 1 #Mark down a win for strat2
            elif outcome == 2: #If strat1 wins...
                p1turn2wins += 1 #Mark down a win for strat1
            elif outcome == 3: #If the players tie...
                p2firstties += 1 #Mark down a tie
        i -= 1 #Reduces the count of games to run by one
    print("When Player 1 went first...")
    print("Player 1 wins: "+str(p1turn1wins)) #Prints how many times strat1 wins
    print("Player 2 wins: "+str(p2turn2wins)) #Prints how many times strat2 wins
    print("Ties:          "+str(p1firstties)) #Prints how many times they tie
    print("When Player 2 went first...")
    print("Player 1 wins: "+str(p1turn2wins)) #Prints how many times strat1 wins
    print("Player 2 wins: "+str(p2turn1wins)) #Prints how many times strat2 wins
    print("Ties:          "+str(p2firstties)) #Prints how many times they tie

def autoplayCheat(strat1, strat2, score1, score2): #Copy of autoplayLoud, except the Print lines are gone and it returns a value at the end
    last = False #Ensures that the game doesn't end after the first move
    while True: #Starts a loop which doesn't end until I tell it to
        numDice = strat1(score1, score2, last) #Player 1 selects how many dice to roll.
        diceTotal = 0 #Zeros the roll's value
        diceString = "" #Empties the list of rolls
        i = numDice #Defines the number of dice to roll
        while i > 0: #Starts a loop which ends when all the dice have been rolled
            d = roll() #Rolls 1d6-1
            diceTotal += d #Tracks the total points gained across all rolls this turn
            diceString = diceString+" "+str(d) #Adds the number rolled this turn to the list of numbers rolled this turn
            i = i-1 #Redefines the number of dice to roll to be one lower
        score1 += diceTotal #Increases Player 1's score by the combined value of its rolls this turn
        if score1 > 100 or last: #If the game is supposed to end at this point...
            break #The game ends
        if numDice == 0: #If Player 1 passes this turn...
            last = True #Marks a trigger for the game to end after Player 2's next turn
        numDice = strat2(score2, score1, last) #Player 2 selects how many dice to roll.
        diceTotal = 0 #Zeros the roll's value
        diceString = "" #Empties the list of rolls
        i = numDice #Defines the number of dice to roll
        while i > 0: #Starts a loop which ends when all the dice have been rolled
            d = roll() #Rolls 1d6-1
            diceTotal += d #Tracks the total points gained across all rolls this turn
            diceString = diceString+" "+str(d) #Adds the number rolled this turn to the list of numbers rolled this turn
            i = i-1 #Redefines the number of dice to roll to be one lower
        score2 += diceTotal #Increases Player 2's score by the combined value of its rolls this turn
        if score2 > 100 or last: #If the game is supposed to end at this point...
            break #The game ends
        if numDice == 0: #If Player 2 passes this turn...
            last = True #Marks a trigger for the game to end after Player 1's next turn
    if score1 > 100: #If Player 1 has gone over 100 points...
        return 2 #Returns that Player 2 wins
    elif score2 > 100: #Otherwise, if Player 2 has gone over 100 points...
        return 1 #Returns that Player 1 wins
    elif score1 > score2: #Otherwise, if Player 1 has more points than Player 2...
        return 1 #Returns that Player 1 wins
    elif score2 > score1: #Otherwise, if Player 2 has more points than Player 1...
        return 2 #Returns that Player 2 wins
    else:
        return 3 #Returns that it was a tie

def manyGamesCheat(strat1, strat2, score1, score2, n): #Runs autoplay betweeen strat1 and strat2 n times and reports win counts
    p1wins, p2wins, ties = 0, 0, 0 #Zeros all win counts
    i = n #Defines the number of games to run
    while i > 0: #Loops until it's run n games
        if i % 2 == 1: #if there's an odd number of games remaining...
            outcome = autoplayCheat(strat1, strat2, score1, score2) #Run a game with strat1 going first
            if outcome == 1: #If strat1 wins...
                p1wins += 1 #Mark down a win for strat1
            elif outcome == 2: #If strat2 wins...
                p2wins += 1 #Mark down a win for strat2
            elif outcome == 3: #If the players tie...
                ties += 1 #Mark down a tie
        else: #If there's a not-odd number of games remaining (in practice even because i should always be an integer)...
            outcome = autoplayCheat(strat2, strat1, score1, score2) #Run a game with strat2 going first
            if outcome == 1: #If strat2 wins...
                p2wins += 1 #Mark down a win for strat2
            elif outcome == 2: #If strat1 wins...
                p1wins += 1 #Mark down a win for strat1
            elif outcome == 3: #If the players tie...
                ties += 1 #Mark down a tie
        i -= 1 #Reduces the count of games to run by one
        #print("1: "+str(p1wins)+"  2: "+str(p2wins)+"  3: "+str(ties)) #Debug line to see intermediate score counts
    print("Player 1 wins: "+str(p1wins)) #Prints how many times strat1 wins
    print("Player 2 wins: "+str(p2wins)) #Prints how many times strat2 wins
    print("Ties:          "+str(ties)) #Prints how many times they tie

def manyGamesCheatNuanced(strat1, strat2, score1, score2, n): #Runs autoplay betweeen strat1 and strat2 n times and reports win counts
    p1turn1wins, p1turn2wins, p2turn1wins, p2turn2wins, p1firstties, p2firstties = 0, 0, 0, 0, 0, 0 #Zeros all win counts
    i = n #Defines the number of games to run
    while i > 0: #Loops until it's run n games
        if i % 2 == 1: #if there's an odd number of games remaining...
            outcome = autoplayCheat(strat1, strat2, score1, score2) #Run a game with strat1 going first
            if outcome == 1: #If strat1 wins...
                p1turn1wins += 1 #Mark down a win for strat1
            elif outcome == 2: #If strat2 wins...
                p2turn2wins += 1 #Mark down a win for strat2
            elif outcome == 3: #If the players tie...
                p1firstties += 1 #Mark down a tie
        else: #If there's a not-odd number of games remaining (in practice even because i should always be an integer)...
            outcome = autoplayCheat(strat2, strat1, score1, score2) #Run a game with strat2 going first
            if outcome == 1: #If strat2 wins...
                p2turn1wins += 1 #Mark down a win for strat2
            elif outcome == 2: #If strat1 wins...
                p1turn2wins += 1 #Mark down a win for strat1
            elif outcome == 3: #If the players tie...
                p2firstties += 1 #Mark down a tie
        i -= 1 #Reduces the count of games to run by one
    print("When Player 1 went first...")
    print("Player 1 wins: "+str(p1turn1wins)) #Prints how many times strat1 wins
    print("Player 2 wins: "+str(p2turn2wins)) #Prints how many times strat2 wins
    print("Ties:          "+str(p1firstties)) #Prints how many times they tie
    print("When Player 2 went first...")
    print("Player 1 wins: "+str(p1turn2wins)) #Prints how many times strat1 wins
    print("Player 2 wins: "+str(p2turn1wins)) #Prints how many times strat2 wins
    print("Ties:          "+str(p2firstties)) #Prints how many times they tie

def StratDiff(strat1, strat2, scorefloor, scoreceiling):
    i1 = scorefloor
    while i1 <= scoreceiling:
        i2 = scorefloor
        while i2 <= scoreceiling:
            output1 = strat1(i1, i2, False)
            output2 = strat2(i1, i2, False)
            if output1 != output2:
                print("Given myscore "+str(i1)+" and theirscore "+str(i2)+", strat1 outputs "+str(output1)+" and strat2 outputs "+str(output2))
            i2 += 1
        i1 += 1

def StratDiffLast(strat1, strat2, scorefloor, scoreceiling):
    i1 = scorefloor
    while i1 <= scoreceiling:
        i2 = scorefloor
        while i2 <= scoreceiling:
            output1 = strat1(i1, i2, True)
            output2 = strat2(i1, i2, True)
            if output1 != output2:
                print("Given myscore "+str(i1)+" and theirscore "+str(i2)+", strat1 outputs "+str(output1)+" and strat2 outputs "+str(output2))
            i2 += 1
        i1 += 1

def practice1(myscore, theirscore, last): #Beats test1-test2
    leeway = 100 - myscore
    if leeway > 20:
        return int(leeway * (3 / 10))
    elif leeway > 5:
        return int(leeway * (1 / 5))
    else:
        return 0

def practice2(myscore, theirscore, last): #Beats test1-test4
    leeway = 100 - myscore
    if leeway > 20 or last:
        return int(leeway * (3 / 10))
    elif leeway <= 20 and (myscore - theirscore) > 40:
        return 0
    elif leeway > 5:
        return int(leeway * (1 / 5))
    else:
        return 0

def practice3(myscore, theirscore, last): #Beats test1-test5
    leeway = 100 - myscore
    if last:
        theirlead = theirscore - myscore
        errormargin = leeway - theirlead
        target = theirlead + int(0.5 * errormargin)
        return int(target / 2.5)
    elif leeway > 20:
        return int(leeway * 0.3)
    elif leeway <= 20 and (myscore - theirscore) > 40:
        return 0
    elif leeway >= 5:
        return int(leeway * 0.2)
    else:
        return 0

def practice4(myscore, theirscore, last): #Beats test1-test5
    leeway = 100 - myscore
    if last:
        theirlead = theirscore - myscore
        errormargin = leeway - theirlead
        target = theirlead + int(0.5 * errormargin)
        if theirscore > myscore:
            return max(int(target / 2.5), 1)
        else:
            return 0
    elif leeway > 20:
        return int(leeway * 0.3)
    elif leeway <= 20 and (myscore - theirscore) > 40:
        return 0
    elif leeway >= 5:
        return int(leeway * 0.2)
    else:
        return 0

def practice5(myscore, theirscore, last): #Beats test1-test7
    leeway = 100 - myscore
    if last:
        theirlead = theirscore - myscore
        errormargin = leeway - theirlead
        target = theirlead + int(0.5 * errormargin)
        if theirscore > myscore:
            return max(int(target / 2.5), 1)
        else:
            return 0
    elif leeway > 20:
        return int(leeway * 0.3)
    elif leeway <= 20 and (myscore - theirscore) > 40:
        return 0
    elif leeway >= 5 or theirscore > myscore:
        return max(int(leeway * 0.2), 1)
    else:
        return 0

def practice6(myscore, theirscore, last): #Beats test1-test7
    leeway = 100 - myscore
    if last:
        theirlead = theirscore - myscore
        errormargin = leeway - theirlead
        target = theirlead + (0.5 * errormargin)
        if theirscore > myscore:
            return max(round(target / 2.5), 1)
        elif theirscore == myscore:
            if myscore > 97:
                return 0
            else:
                return 1
        else:
            return 0
    elif leeway > 20:
        return int(leeway * 0.3)
    elif leeway <= 20 and (myscore - theirscore) > 40:
        return 0
    elif leeway >= 5 or theirscore > myscore:
        return max(int(leeway * 0.2), 1)
    else:
        return 0

def practice7(myscore, theirscore, last): #Beats test1-test7 consistently and test8 inconsistently
    leeway = 100 - myscore
    if last:
        if theirscore > myscore:
            theirlead = theirscore - myscore
            errormargin = leeway - theirlead
            target = theirlead + (0.5 * errormargin)
            return max(round(target / 2.5), 1)
        elif theirscore == myscore:
            if myscore > 97:
                return 0
            else:
                return max(int(leeway * 0.2), 1)
        else:
            return 0
    elif leeway > 15:
        return int(leeway * 0.3)
    elif leeway >= 5 or theirscore > myscore:
        return max(int(leeway * 0.2), 1)
    else:
        return 0

def practice8(myscore, theirscore, last): #Beats test1-test8 and test10
    leeway = 100 - myscore
    if last:
        if theirscore > myscore:
            theirlead = theirscore - myscore
            errormargin = leeway - theirlead
            target = theirlead + (0.5 * errormargin)
            return max(round(target / 2.5), 1)
        elif theirscore == myscore:
            if myscore > 97:
                return 0
            else:
                return max(int(leeway * 0.2), 1)
        else:
            return 0
    elif leeway > 15:
        return int(leeway * 0.3)
    elif leeway > 2 or theirscore > myscore:
        return max(int(leeway * 0.2), 1)
    else:
        return 0

def practice9(myscore, theirscore, last): #Beats test1-test10
    leeway = 100 - myscore
    if last:
        if theirscore > myscore:
            theirlead = theirscore - myscore
            errormargin = leeway - theirlead
            target = theirlead + (0.5 * errormargin)
            return max(round(target / 2.5), 1)
        elif theirscore == myscore:
            if myscore > 97:
                return 0
            else:
                return max(int(leeway * 0.2), 1)
        else:
            return 0
    elif leeway > 2 or theirscore > myscore:
        return max(int(leeway * 0.3), 1)
    else:
        return 0

def practice10(myscore, theirscore, last): #Beats test1-test10
    leeway = 100 - myscore
    if last:
        if theirscore > myscore:
            theirlead = theirscore - myscore
            errormargin = leeway - theirlead
            target = theirlead + (0.5 * errormargin)
            return max(round(target / 2.5), 1)
        elif theirscore == myscore:
            if myscore > 97:
                return 0
            else:
                return max(int(leeway * 0.2), 1)
        else:
            return 0
    elif leeway > 2 or theirscore > myscore:
        return max(int(leeway * 0.31), 1)
    else:
        return 0

def practice11(myscore, theirscore, last): #Beats test1-test10
    leeway = 100 - myscore
    if last:
        if theirscore > myscore:
            theirlead = theirscore - myscore
            errormargin = leeway - theirlead
            target = theirlead + (0.5 * errormargin)
            return max(round(target / 2.5), 1)
        elif theirscore == myscore:
            if myscore > 97:
                return 0
            else:
                return max(int(leeway * 0.2), 1)
        else:
            return 0
    elif myscore == 0:
        return 33
    elif leeway > 2 or theirscore > myscore:
        return max(int(leeway * 0.3), 1)
    else:
        return 0

def practice12(myscore, theirscore, last): #Beats test1-test10
    leeway = 100 - myscore
    if last:
        if theirscore > myscore:
            theirlead = theirscore - myscore
            errormargin = leeway - theirlead
            target = theirlead + (0.5 * errormargin)
            return max(round(target / 2.5), 1)
        elif theirscore == myscore:
            if myscore > 97:
                return 0
            else:
                return max(int(leeway * 0.2), 1)
        else:
            return 0
    elif myscore == 0:
        return 33
    elif leeway > 2 or theirscore > myscore:
        return max(int(leeway * 0.29), 1)
    else:
        return 0

def practice12cheat(myscore, theirscore, last): #like practice12, but it hijacks test11's moves a lot of the time
    leeway = 100 - myscore
    if last:
        if theirscore > myscore:
            theirlead = theirscore - myscore
            errormargin = leeway - theirlead
            target = theirlead + (0.5 * errormargin)
            return max(round(target / 2.5), 1)
        elif theirscore == myscore:
            if myscore > 97:
                return 0
            else:
                return max(int(leeway * 0.2), 1)
        else:
            return 0
    elif myscore == 0:
        return 33
    elif leeway > 2 or theirscore > myscore:
        return pr1testing.test11(myscore, theirscore, last)
    else:
        return 0

def practice13(myscore, theirscore, last): #Beats all tests
    leeway = 100 - myscore
    if last:
        if theirscore > myscore:
            theirlead = theirscore - myscore
            errormargin = leeway - theirlead
            target = theirlead + (0.5 * errormargin)
            return max(round(target / 2.5), 1)
        elif theirscore == myscore:
            if myscore > 97:
                return 0
            else:
                return max(int(leeway * 0.2), 1)
        else:
            return 0
    elif myscore == 0:
        return 33
    elif leeway > 3 or theirscore > myscore:
        return max(int(leeway * 0.29), 1)
    else:
        return 0

def practice14(myscore, theirscore, last): #Beats all tests
    leeway = 100 - myscore
    if last:
        if theirscore > myscore:
            theirlead = theirscore - myscore
            errormargin = leeway - theirlead
            target = theirlead + (0.5 * errormargin)
            return max(round(target / 2.5), 1)
        elif theirscore == myscore:
            if myscore > 97:
                return 0
            else:
                return max(int(leeway * 0.2), 1)
        else:
            return 0
    elif myscore == 0:
        return 33
    elif myscore == 97 and theirscore == 97:
        return 1
    elif leeway > 3 or theirscore > myscore:
        return max(int(leeway * 0.29), 1)
    else:
        return 0

def practice15(myscore, theirscore, last): #Beats all tests
    leeway = 100 - myscore
    if last:
        if theirscore > myscore:
            theirlead = theirscore - myscore
            errormargin = leeway - theirlead
            target = theirlead + (0.5 * errormargin)
            return max(round(target / 2.5), 1)
        elif theirscore == myscore:
            saferoll = int(leeway * 0.2)
            if myscore > 97:
                return 0
            elif (myscore % 5) == 1 or (myscore % 5) == 2:
                return saferoll + 1
            else:
                return saferoll
        else:
            return 0
    elif myscore == 0:
        return 33
    elif myscore == 97 and theirscore == 97:
        return 1
    elif leeway > 3 or theirscore > myscore:
        return max(int(leeway * 0.29), 1)
    else:
        return 0

def practice16(myscore, theirscore, last): #Beats all tests
    leeway = 100 - myscore
    if last:
        if theirscore > myscore:
            theirlead = theirscore - myscore
            errormargin = leeway - theirlead
            target = theirlead + (0.5 * errormargin)
            return max(round(target / 2.5), 1)
        elif theirscore == myscore:
            saferoll = int(leeway * 0.2)
            if myscore > 97:
                return 0
            elif myscore % 5 == 2 and saferoll < 4:
                return saferoll + 1
            elif myscore % 5 == 1:
                return saferoll + 1
            else:
                return saferoll
        else:
            return 0
    elif myscore == 0:
        return 33
    elif myscore == 97 and theirscore == 97:
        return 1
    elif leeway > 3 or theirscore > myscore:
        return max(int(leeway * 0.29), 1)
    else:
        return 0