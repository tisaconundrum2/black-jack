from gamestart import *
base_deck = deck()

def initial_cards(shoe):
    '''deals 2 cards to player and dealer returns dealer hand as
    first hand player hand as second in a list'''
    player_hand = [deal_card(shoe)]
    dealer_hand = [deal_card(shoe)]
    player_hand.append(deal_card(shoe))
    dealer_hand.append(deal_card(shoe))
    return [dealer_hand, player_hand]

def dealt_blackjack(hands):
    '''checks to see if either of the first hands dealt are blackjack'''
    if hand_points(hands) == 21:
        return True
    else:
        return False        

def split(hand, shoe):
    '''if hand size is < 2, will add card else check for equal rank if
    they will it will offer to split and then create append that to hands
    update bet to represent this as well.  Returns 0 if no split else returns
    the card'''
    
    if len(hand) == 2 and hand[0].getrank() == hand[1].getrank():
        action = input("Would you like to split?\n")
        if action == 'y':
            card = hand.pop()
            hit(hand,shoe)
            return card
    return 0
    
# def double(hand, shoe):
#     '''checks if player would like to double their bet and provides a hit'''
#     action = input("Would you like to double? \n")
#     if action == 'y':
#         hit(hand, shoe)
#         return 2
#     else:
#         return 0

def hit(hand, shoe):
    '''adds a card to the hand, performs a hit'''
    hand.append(deal_card(shoe))
    return hand
       
def dealer_play(dealer_hand, shoe):
    '''lets dealer play with standard rule of hit on 16 stay on 17'''
    total = hand_points(dealer_hand)
    
    if total < 17:
        dealer_hand=(hit(dealer_hand, shoe))              
        dealer_play(dealer_hand, shoe)       #recurrsive call to hit again
        
    else:
        return

def hand_points(hand):
    '''gives the value of the hand'''
    total = 0
    for cards in hand:
        total += cards.getpoint()   #gets values for cards

    if total > 21:
        for cards in hand:   #makes ace =1 if 21 is overshot
            if cards.getrank() == 'A':
                total -= 10
                if total <= 21:
                    break
    
    return total

def calculations(dealer, player, shoe):
    '''calculates the values for each hand and returns the rate of return of the hand'''
    player_total = hand_points(player)
    if player_total > 21:  #lose condition
        return 0

    else:
        dealer_play(dealer, shoe)
        dealer_total = hand_points(dealer)
        
        if dealer_total > 21:
            return 2
        elif dealer_total < player_total: #win condition
            return 2
        elif dealer_total == player_total:  #push condition
            return 1
        else:  #lose conition
            return 0
        
def winnings(bet, rate):
    '''Updates the amount of money the player has based on how much they won'''
    return bet * rate
