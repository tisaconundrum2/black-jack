import sys
from PyQt4 import QtCore
from Qtickle import Qtickle
import blackjackui
from UIfunctions import *
from gamefunctions import *


class main(QtGui.QWidget):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)  # Starting the mainWindow
        self.ui = blackjackui.Ui_Blackjack()  # getting the UI framework the Blackjack UI and putting it into ui
        self.ui.setupUi(self)  # calling the function from Ui_Blackjack

        self.ui.btnBet.clicked.connect(self.betClicked)  # connecting the bet Button from the Ui_Blackjack class
        self.ui.btnStay.clicked.connect(self.stayClicked)  # connecting stay button
        self.ui.btnDouble.clicked.connect(self.doubleClicked)  # connecting double button
        self.ui.btnHit.clicked.connect(self.hitClicked)  # connecting hit button
        self.ui.btnSave.clicked.connect(self.saveClicked)
        self.ui.btnLoad.clicked.connect(self.loadClicked)

        self.deck = deck()
        self.shoe = create_shoe(self.deck, 1)  # creates a deck of cards to be used during the game

        # sets up the initial game conditions
        self.money = 500  # give the player 500 dollars
        self.ui.betSpinBox.setMaximum(self.money)  # set the maximum spinbox value
        self.ui.labMoney.setText(str(self.money))  # set the label for the amount of money available
        self.hands = []  # clear the hands of both the dealer and player
        self.bet = 0  # set the initial value for the bet

        # make a list of card graphics in the UI
        self.dealer_hand = [self.ui.dCard_0, self.ui.dCard_1, self.ui.dCard_2, self.ui.dCard_3, self.ui.dCard_4,
                            self.ui.dCard_5, self.ui.dCard_6, self.ui.dCard_7, self.ui.dCard_8, self.ui.dCard_9]
        self.player_hand = [self.ui.pCard_0, self.ui.pCard_1, self.ui.pCard_2, self.ui.pCard_3, self.ui.pCard_4,
                            self.ui.pCard_5, self.ui.pCard_6, self.ui.pCard_7, self.ui.pCard_8, self.ui.pCard_9]

        buttoncontrol(self.ui)  # disables all buttons that control the hand
        self.qtickle = Qtickle(self.ui, QtCore.QSettings('saved.ini', QtCore.QSettings.IniFormat))


    def loadClicked(self):
        self.qtickle.guirestore()

    def saveClicked(self):
        self.qtickle.guisave()

    def betClicked(self):
        try:
            if self.money <= 0:  # if the user ran out of money
                self.money = 500  # give them some more
                self.ui.labWarning.setText("Here's some more money to play with. Have fun.")
                self.ui.labMoney.setText(str(self.money))  # change the label of the amount of money that is available
                self.ui.betSpinBox.setMaximum(self.money)  # set the maximum spinbox value
            elif int(self.ui.betSpinBox.text()) > self.money or int(
                    self.ui.betSpinBox.text()) < 0:  # Alert the user when they go out of bounds
                self.ui.labWarning.setText("Please enter a number less than " + str(self.money) + " and greater than 0")
            else:
                betfunction(self)  # Call the betfunction from UIfunctions
        except:
            self.ui.labWarning.setText("Please enter a number less than " + str(self.money) + " and greater than 0")

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
