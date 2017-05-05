class Card(object):
    def __init__ (self, rank, suit, points, graphic):
        self.rank = rank
        self.suit = suit
        self.points = points
        self.graphic = graphic
        
    def __repr__ (self):
        return self.suit + self.rank

    def getpoint (self):
        return int(self.points)

    def getrank(self):
        return str(self.rank)

    def getgraphic(self):
        return self.graphic

    
def deck():
    '''creates a deck of cards'''
                             
    from PyQt4 import QtGui
    import os
    
    #creates a dictionary of all ranks and values
    rank = {'A':11, '2': 2, '3':3, '4':4, '5':5, '6':6,'7': 7,'8':8 ,'9':9 , '10':10, 'J':10, 'Q':10, 'K':10} 
    suit = ['S', 'C', 'D', 'H']

    new_deck = []    #creating a blank list for the deck
    path = os.getcwd()  #gets the current directory to use to find the image of the cards
    for key in rank:
        for s in suit:
            image = QtGui.QImage(path + '/cards/' + s + key + '.png')
            new_deck.append(Card(str(key),s,rank[key], image))
    return new_deck

def create_shoe(deck, size):
    '''creates size number decks in a blackjack shoe in the form of a dictionary with the Card string
    and the number of the card left in the deck'''
    shoe = {}
    for card in deck:
        shoe[card]= size
    return shoe

def deal_card(shoe):
    '''deals a card from the deck'''
    from random import choice
    dealt_card = choice(list(shoe.keys()))  #randomly draws a card from the base deck
    while shoe[dealt_card] == 0 and sum(shoe.values()) > 0: # check to see if the card is a zero and that we haven't run out of cards to play with.
        dealt_card = choice(list(shoe.keys()))  # randomly draws a card from the base deck
    else:
        shoe[dealt_card] -=1    #reduces the number of that card in the shoe and
        return dealt_card       #returns the card
