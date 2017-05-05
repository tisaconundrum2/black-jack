import sys

import newBlackJacUI
from UIfunctions import *
from gamefunctions import *


class main(QtGui.QWidget):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)  # Starting the mainWindow
        self.ui = newBlackJacUI.Ui_Blackjack()  # getting the UI framework the Blackjack UI and putting it into ui
        self.ui.setupUi(self)  # calling the function from Ui_Blackjack

        self.ui.btnBet.clicked.connect(self.betClicked)  # connecting the bet Button from the Ui_Blackjack class
        self.ui.btnStay.clicked.connect(self.stayClicked)  # connecting stay button
        self.ui.btnDouble.clicked.connect(self.doubleClicked)  # connecting double button
        self.ui.btnHit.clicked.connect(self.hitClicked)  # connecting hit button

        self.deck = deck()
        self.shoe = create_shoe(self.deck, 1)  # creates a deck of cards to be used during the game

        # sets up the initial game conditions
        self.money = 500
        self.ui.betSpinBox.setMaximum(int(self.ui.labMoney.text()))
        self.ui.labMoney.setText(str(self.money))
        self.hands = []
        self.bet = 0

        # list of card graphics in the ui
        self.dealer_hand = [self.ui.dCard_0, self.ui.dCard_1, self.ui.dCard_2, self.ui.dCard_3, self.ui.dCard_4,
                            self.ui.dCard_5, self.ui.dCard_6, self.ui.dCard_7, self.ui.dCard_8, self.ui.dCard_9]
        self.player_hand = [self.ui.pCard_0, self.ui.dCard_1, self.ui.pCard_2, self.ui.pCard_3, self.ui.pCard_4,
                            self.ui.pCard_5, self.ui.pCard_6, self.ui.pCard_7, self.ui.pCard_8, self.ui.pCard_9]

        # disables all buttons that control the hand
        buttoncontrol(self.ui)

    def betClicked(self):
        try:
            if self.money <= 0:
                self.money = 500
                self.ui.labWarning.setText("Here's some more money to play with. Have fun.")
                self.ui.labMoney.setText(str(self.money))
                self.ui.betSpinBox.setMaximum(self.money)
            elif int(self.ui.betSpinBox.text()) > self.money or int(self.ui.betSpinBox.text()) < 0:
                self.ui.labWarning.setText("Please enter a number less than " + str(self.money) + " and greater than 0")
            else:
                betfunction(self)
        except:
            self.ui.labWarning.setText("Please enter a number less than " + str(self.money) + " and greater than 0")

        self.ui.betSpinBox.clear()

    def hitClicked(self):
        '''adds card to the ui showing the card that was just added to the hand'''
        self.ui.btnDouble.setEnabled(False)
        hit(self.hands[1], self.shoe)

        # determines the position of the last card added to the hand and shows it
        i = len(self.hands[1]) - 1
        showcard(self.player_hand[i], self.hands[1][i])
        self.ui.labPlayer.setText(str(hand_points(self.hands[1])))

        # if player busts takes player to end of the game automatically
        if (hand_points(self.hands[1]) > 21):
            self.stayClicked()

    def doubleClicked(self):
        '''handles the case where the player doubles the bet by adding to the bet and getting one more card'''
        self.money -= self.bet
        self.bet *= 2
        self.ui.labMoney.setText(str(self.money))
        hit(self.hands[1], self.shoe)
        i = len(self.hands[1]) - 1
        showcard(self.player_hand[i], self.hands[1][i])
        self.ui.labPlayer.setText(str(hand_points(self.hands[1])))
        self.stayClicked()

    def stayClicked(self):
        '''handles endgame situation and has the dealer play out hand and calculates winnings'''
        # turns off all play buttons and activates btnBet
        buttoncontrol(self.ui)
        winner = calculations(self.hands[0], self.hands[1], self.shoe)  # calls function to see which hand won

        # shows the dealers cards and how many points it is worth in the ui
        self.ui.labDealer.setText(str(hand_points(self.hands[0])))
        for i in range(0, len(self.hands[0])):
            showcard(self.dealer_hand[i], self.hands[0][i])

        self.money += winnings(self.bet, winner)  # updates self.money based on bet
        self.ui.labMoney.setText(str(self.money))
        self.ui.betSpinBox.setMaximum(self.money)  # update the maximum withdrawal


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)  # Specify that we are working with a QApplication
    Window = main()  # set the class main() int Window
    Window.show()  # have this main() be displayed
    app.exec_()  # execute the app
