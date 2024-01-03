import numpy as np
import random
from termcolor import colored

class Board:
    def __init__(self, status='random'):
        '''
        Create an empty new board.
        status (str):
            'empty': no cards on the board
            'random': cards on the board are randomly dealt
            'sorted': cards on the board are sorted
        '''
        # self.board[0][:3] stores -4, -8, -12
        # self.board[0][4:] stores 0, and the three discard piles
        # self.board[0][3] is left blank
        self.board = np.zeros((10,8), dtype=int)

        # Set the status of the board
        if status == 'random':
            # Create a list of all the cards
            cards = list(range(3, 30))
            cards = cards + [-1, -2, -3]*4
            cards = cards + [1]
            # Deal the cards to the board
            random.shuffle(cards)
            cards = np.reshape(cards, (5,8))
            self.board[1:6, :] = cards
        elif status == 'sorted':
            self.board[1:, 0] = [27, 25, 23, 18, 16, 14, 9, 7, 5]
            self.board[1:, 1] = [28, 26, 21, 19, 17, 12, 10, 8, 3]
            self.board[1:, 2] = [29, 24, 22, 20, 15, 13, 11, 6, 4]
        elif status != 'empty':
            raise ValueError('Invalid status: ' + status)

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
        for i in range(1,10):
            for j in range(8):
                text += Board.print_card(self.board[i][j])
                text += '\t'
            text += '\n'
        return '\n' + text.strip() + '\n'

    def print_card(ID):
        '''
        convert card ID to colored string
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




if __name__ == '__main__':
    board = Board(status='sorted')
    print(board)