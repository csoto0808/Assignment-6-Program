#!/usr/bin/env python3

#----------------------------------------------------------------------
# blackjack.py
# Cornelio Soto
# 10/28/19
#----------------------------------------------------------------------

from graphics import *
from Blackjack.CardDeck import *

#----------------------------------------------------------------------
def drawCard(filename: str, x: int, y: int, window: GraphWin):

    """draw image specified by filename centered at (x, y) in window"""

    p = Point(x, y)
    prefixes = ['cardset/', '../cardset/', './']
    for prefix in prefixes:
        fname = '{}{}'.format(prefix, filename)
        try:
            image = Image(p, fname)
            image.draw(window)
            return image
        except:
            pass

#----------------------------------------------------------------------
def cardInfo(cardNumber) -> (int, str):

    """returns the blackjack value and and filename for card specified
    by cardNumber

    0-12 are the Ace-King of clubs
    13-25 are the Ace-King of spades
    26-38 are the Ace-King of hearts
    39-51 are the Ace-King of diamonds
    
    the blackjack value for the cards 2-9 are the corresponding
    number; 10, Jack, Queen, and King all have blackjack values of 10
    and an Ace has a value of 11
    
    filename is of the form: ##s.gif
    where ## is a two digit number (leading 0 if less than 10)
    and s is a letter corresponding to the suit value
    c for clubs, s for spades, h for hearts, d for diaomnds"""

    # calculate suit and face numbers
    suitNum = cardNumber // 13 # suitNum = 0-3
    faceNum = cardNumber % 13  # faceNum = 0-12

    # calculate blackjack value (0-51)
    value = faceNum + 1
    if value > 10:
        value = 10
    elif value == 1:
        value = 11

    # calculate name of file
    # face is a number from 1 to 13 with leading zeros for 1-9
    suits = 'cshd'
    filename = '{:>02}{}.gif'.format(faceNum + 1, suits[suitNum])
    return value, filename

#----------------------------------------------------------------------
def winLoseConditions(win, playerScore:int, dealerScore:int, winCount:int, loseCount:int, tieCount:int)->(int,int,int):

    """
    function determines the appropriate win/lose condition, displays the appropriate
    text and updates the counters for each outcome

    :param win: win
    :param playerScore: final player score
    :param dealerScore: final dealer score
    :param winCount: current win count total
    :param loseCount: current lose count total
    :param tieCount: current tie count total
    :return: returns winCount, loseCount, and tieCount for use in next game
    """
    # create specific texts for each win/lose condition
    dealerWinText = Text(Point(500, 200), "Dealer Wins!")
    dealerLoseText = Text(Point(500, 200), "Dealer Loses!")
    dealerBustText = Text(Point(500, 200), "Dealer Busts!")

    playerWinText = Text(Point(500, 400), "You Win!")
    playerLoseText = Text(Point(500, 400), "You lose!")
    playerBustText = Text(Point(500, 400), "You Bust!")

    tieText = Text(Point(500,400), "Tie")

    # finds the appropriate win/lose condition by comparing dealer/player scores to each other
    if (playerScore < 22) and (dealerScore < 22):   # if both don't bust
        if playerScore > dealerScore:
            # condition: player wins, dealer loses
            playerWinText.draw(win)
            dealerLoseText.draw(win)
            winCount +=1
            print("player wins, dealer loses")

        elif dealerScore > playerScore:
            # condition: dealer wins, player loses
            dealerWinText.draw(win)
            playerLoseText.draw(win)
            loseCount += 1
            print("dealer wins, player loses")

        elif playerScore == dealerScore:
            # condition: tie
            tieCount += 1
            tieText.draw(win)
            print("tie")

    elif playerScore > 21 or dealerScore > 21:  #if one or the other busts
        if playerScore > 21:
            # condition: player busts, dealer wins
            playerBustText.draw(win)
            dealerWinText.draw(win)
            loseCount += 1
            print("player busts, dealer wins")

        elif dealerScore > 21:
            #condition: dealer busts, player wins
            playerWinText.draw(win)
            dealerBustText.draw(win)
            winCount += 1
            print("dealer busts, player wins")
    return winCount, loseCount, tieCount

#----------------------------------------------------------------------

def findSpecialAValue(value:int, score:int)->int:

    """
    determines if A is added to total as an 1 or as a 11 (special case)
    :param value: face value of card
    :param score: current player/dealer score
    :return: correct value for drawn ace (1 or 11)
    """
    # changes value for a if its busts player/dealer, changes value of a to 1
    # if value is anything other than A, it is not changed or affected
    total = 0
    if value == 11:
        if (total + score + value) > 21:    #checks to see if a as 11 + value is over 21
            value = 1   #if true, changes a to 1
            return value
        else:           #else, returns 11
            return value
    return value    #if not a, returns the original card value

#----------------------------------------------------------------------

def cardDraw(win, card, cardCount:int, y:int, score:int):
    """
    draws a card from the deck, returns the score
    :param win: win
    :param card: card item from list deck
    :param cardCount: number of cards already drawn by dealer/player, used to draw the x for point
    :param y: y value needed to draw card (specific to either player or dealer)
    :param score: current score for dealer/player
    :return: value for recently drawn card is added to player/dealer score and is returned
    """
#parameters: window, card for dealOne(), cardCount for dealer/player, y position, and dealer/player score
    value, filename = cardInfo(card)
    drawCard(filename, 100 * cardCount, y, win)
    score = score + findSpecialAValue(value, score)
    return score

#----------------------------------------------------------------------
def drawDecorations(win):

    """
    function takes care of drawing all the graphical elements of the code not essential to running the game
    :param win:
    :return: none
    """
    # function draws all the decorative elements of the blackjack game

    # draw "deck" in top right corner
    drawCard("back01.gif", 675, 480, win)
    drawCard("back01.gif", 673, 478, win)
    drawCard("back01.gif", 671, 476, win)
    drawCard("back01.gif", 669, 474, win)

    # create and draw decorative elements
    decorativeSquare = Rectangle(Point(50, 130), Point(560, 560))
    decorativeSquare.setOutline("white")
    decorativeSquare.draw(win)
    decorativeSquare2 = Rectangle(Point(590, 130), Point(760, 560))
    decorativeSquare2.setOutline("white")
    decorativeSquare2.draw(win)

    # draw hit me button
    hitMeBox = Rectangle(Point(600, 350), Point(750, 400))  # draw box
    hitMeBox.setFill("white")
    hitMeBox.draw(win)
    hitMeText = Text(Point(675, 375), "Hit Me!")  # draw text
    hitMeText.draw(win)

    # draw quit game button
    quitGameBox = Rectangle(Point(600, 250), Point(750, 300))
    quitGameBox.setFill("white")
    quitGameBox.draw(win)
    quitText = Text(Point(675, 275), "Quit Game.")
    quitText.draw(win)

# ----------------------------------------------------------------------

def drawScoreKeeper(win, winCount:int, loseCount:int, tieCount: int):

    """
    draws and displays the current game totals in top right of window
    :param win: win
    :param winCount: current win total
    :param loseCount: current lose total
    :param tieCount: current tie total
    :return: none
    """
    # added 4/16/21, win/lose/tie counter in top right of window
    scoreCounter = Text(Point(660, 570), f'Win: {winCount} / Lose: {loseCount} / Tie: {tieCount}')
    scoreCounter.setFill("white")
    scoreCounter.draw(win)

#----------------------------------------------------------------------

def blackjackGame(winCount:int, loseCount:int, tieCount:int):

    """
    function carries out the code responsible for running the blackjack game and interactions with user
    :param winCount: current win total
    :param loseCount: current lose total
    :param tieCount: current tie total
    :return: none, can close and relaunch game 
    """
    # create window, card deck and shuffle it
    win = GraphWin("Blackjack Game", 800, 600)
    win.setCoords(0, 0, 800, 600)
    win.setBackground("green")
    deck = CardDeck()
    deck.shuffle()

    # initialize scores for both player and dealer as well as the text
    playerScore = 0
    dealerScore = 0

    drawDecorations(win)
    drawScoreKeeper(win, winCount, loseCount, tieCount)

    # initialize player/dealer score text under area where drawn cards go
    dealerScoreText = Text(Point(100, 200), "")
    dealerScoreText.draw(win)

    playerScoreText = Text(Point(100, 400), "")
    playerScoreText.draw(win)

    # set up dealers initial card
    dealerCardCount = 1
    card = deck.dealOne()
    dealerScore = cardDraw(win, card, dealerCardCount, 300, dealerScore)
    # update/change score text for dealer after drawn card
    dealerScoreText.setText(f'Score: {dealerScore}')

    # deal 2 cards for player during beginning of game
    for i in range(1,3):
        playerCardCount = i
        card = deck.dealOne()
        playerScore = cardDraw(win, card, playerCardCount, 500, playerScore)
        # update/change score text for player after each drawn card
        playerScoreText.setText(f'Score: {playerScore}')

    # deal the rest of the cards
    playerCardCount = 2
    while playerScore <= 21:
        # break if playerScore is greater than 21
        playerCardCount += 1
        if playerCardCount > 5:
        # card count breaks while loop if it goes over 5
            break

        p1 = win.getMouse() # get a mouse click from player

        #quit button----------------------------------------------------------------------
        if ((p1.getX() > 600) and (p1.getX() < 750)) and \
            ((p1.getY() > 250) and (p1.getY() < 300)):  #checks if point is within quit box
                quit(main)
        #hit me button--------------------------------------------------------------------
        if ((p1.getX() > 600) and (p1.getX() < 750)) and \
            ((p1.getY() < 400) and (p1.getY() > 350)):  #checks if point is within hitMe box
                    if True:    #if true, deal card
                        card = deck.dealOne()
                        playerScore = cardDraw(win, card, playerCardCount, 500, playerScore)
                        playerScoreText.setText(f'Score: {playerScore}')
                        if playerScore > 21:
                            break
        #stand (click anywhere else)------------------------------------------------------
        else:
            break

    # deal the rest of the cards for dealer
    while dealerScore < 17:     #breaks if dealerScore is greater than 17
        if playerScore > 21:    #breaks if player busts
            break
        dealerCardCount += 1    #dealer card count goes up by 1
        if dealerCardCount > 5:
            break
        card = deck.dealOne()
        dealerScore = cardDraw(win, card, dealerCardCount, 300, dealerScore)
        dealerScoreText.setText(f'Score: {dealerScore}')

    # draw the win/lose condition, added win/lose/tie
    winCount, loseCount, tieCount = winLoseConditions(win, playerScore, dealerScore, winCount, loseCount, tieCount)

    #play Again button--------------------------------------------------------------------
    anotherGameBox = Rectangle(Point(600,150),Point(750,200))
    anotherGameBox.setFill("white")
    anotherGameBox.draw(win)
    playAgainText = Text(Point(675,175),"Play Again?")
    playAgainText.draw(win)

    # determine mouse click actions
    p1 = win.getMouse()
    if ((p1.getX() > 600) and (p1.getX() < 750)) and \
            ((p1.getY() < 200) and (p1.getY() > 150)):
        if True:
            #close current window and start new game
            win.close()
            blackjackGame(winCount, loseCount, tieCount)
            #main()
    else:
        #close window
        win.close()
        # wait for mouse click before closing window
    
#----------------------------------------------------------------------

def main(): # created main to contain the calling of other functions
    # set counters to 0
    winCount = 0
    loseCount = 0
    tieCount = 0

    # start game and pass counters
    blackjackGame(winCount, loseCount, tieCount)

# ----------------------------------------------------------------------
if __name__ == '__main__':
    main()
