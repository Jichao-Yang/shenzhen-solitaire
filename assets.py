import numpy as np
import random
from termcolor import colored

class Board:
    def __init__(self):
        '''
        Create an empty new board
        '''
        # self.board[0][:3] stores -4, -8, -12
        # self.board[0][4:] stores 0, and the three discard piles
        # self.board[0][3] is left blank
        self.board = np.zeros((6,8), dtype=int)

    def randomize(self):
        '''
        Deal 40 cards randomly to the board
        '''
        # Create a list of all the cards
        cards = list(range(3, 30))
        cards = cards + [-1, -2, -3]*4
        cards = cards + [1]

        # Deal the cards to the board
        random.shuffle(cards)
        cards = np.reshape(cards, (5,8))
        self.board[1:, :] = cards

    def print_card(ID):
        '''
        Print the colored value of card given ID
        '''
        colors = ['red', 'green', 'black']
        specials = ['中', '發', '白']

        # Empty cards
        if ID == 0:
            return ' '

        # Normal cards
        if ID in range(3, 30):
            return colored(str(ID//3), colors[ID%3], attrs=['bold'])
        
        # Special cards
        if ID in range(-3, 0):
            return colored(specials[-ID-1], colors[-ID-1])
        elif ID == 1:
            return '🌸'
        
        # Pile of cards
        if ID < 0 and ID//4 != 0:
            return colored(specials[-ID//4-1] + '*4', colors[-ID//4-1])
            
    def __repr__(self):
        '''
        Print the board
        '''
        text = '-'*60 + '\n'
        # print the first line
        for i in range(8):
            text += Board.print_card(self.board[0][i])
            text += '\t'
        text += '\n' + '-'*60 + '\n'
        # print the board
        for i in range(1,6):
            for j in range(8):
                text += Board.print_card(self.board[i][j])
                text += '\t'
            text += '\n'
        return text


if __name__ == '__main__':
    board = Board()
    board.randomize()
    board.board[0][0] = -4
    board.board[0][1] = -8
    print(board)