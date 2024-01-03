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
        self.board = np.zeros((14,8), dtype=int)

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
            self.board[1:10, 0] = [27, 25, 23, 18, 16, 14, 9, 7, 5]
            self.board[1:10, 1] = [28, 26, 21, 19, 17, 12, 10, 8, 3]
            self.board[1:10, 2] = [29, 24, 22, 20, 15, 13, 11, 6, 4]
            self.board[1:4, 3] = [-1, -2, -3]
            self.board[1:4, 4] = [-1, -2, -3]
            self.board[1:4, 5] = [-1, -2, -3]
            self.board[1:4, 6] = [-1, -2, -3]
            self.board[1, 7] = 1
        elif status != 'empty':
            raise ValueError('Invalid status: ' + status)

    def __repr__(self):
        '''
        Print the board
        '''
        text = '-'*60 + '\n'
        # print the first line
        for i in range(8):
            text += Board._print_card(self.board[0][i])
            text += '\t'
        text += '\n' + '-'*60 + '\n'
        # print the board
        for i in range(1,14):
            for j in range(8):
                text += Board._print_card(self.board[i][j])
                text += '\t'
            text += '\n'
        return '\n' + text.strip() + '\n'

    def _print_card(ID):
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

    def _find_head(column):
        '''
        Returns the head position of a column of cards. If no head exists, the last card becomes a single head to tail.
        Returns 0 if the column is empty.
        column: a size (14,) array of cards. The first element will be ignored.
        '''
        # if the column is empty
        if column[1] == 0:
            return 0

        i = 13 # last card
        while i > 1:
            if column[i] == 0:
                i -= 1
                continue # traverse to the last nonempty spot
            # if the next card is special card
            if column[i-1] < 3:
                return i
            # if the next card doesn't connect with the current card
            elif (column[i-1]//3 != column[i]//3+1) or (column[i-1]%3 == column[i]%3):
                return i
            # if the next card connects with the current card
            else:
                i -= 1
        return i

    def _find_last(column):
        '''
        Returns the position of the last element in a column of cards.
        If the column is empty, returns 0.
        column: a size (14,) array of cards. The first element will be ignored.
        '''
        i = 13
        while i > 0:
            if column[i] != 0:
                return i
            i -= 1
        return i

    def _can_connect(tail, head):
        '''
        Checks if the head can connect behind the tail
        tail, head (int): card IDs
        '''
        # Special cards
        if tail not in range(0,30) or head not in range(0,30):
            return False
        # Normal cards
        if (tail//3-1 == head//3) and (tail%3 != head%3):
            return True
        else:
            return False

    def valid_moves(self):
        '''
        Returns a list of valid manual moves. Each move is a tuple of (start, end) except collecting special cards,
        which is an int of value -1,-2,-3.
        '''
        # Generate reused info about board
        # Last elements
        last_elements = [(Board._find_last(self.board[:,i]), i) for i in range(8)]
        empty_columns = [element[1] for element in last_elements if element[0]==0]
        last_elements = [element for element in last_elements if element[0]!=0] # Non empty column
        # Top rows
        caches = [(0,0), (0,1), (0,2)]
        full_caches = [cache for cache in caches if self.board[cache]!=0] # full cache
        empty_caches = [cache for cache in caches if self.board[cache]==0] # empty cache
        # heads
        max_heads = [(Board._find_head(self.board[:,i]), i) for i in range(8)]
        max_heads = [head for head in max_heads if head[0]!=0]
        # Every item below a head can also be a head
        heads = []
        for max_head in max_heads:
            for i in range(max_head[0], 14):
                if self.board[i, max_head[1]] == 0:
                    break
                heads.append((i, max_head[1]))
        
        # Generate valid moves
        moves = []
        # Move last element to empty cache
        for element in last_elements:
            for cache in empty_caches:
                moves.append((element, cache))
        # Move last element to discard pile
        for element in last_elements:
            if self.board[element] not in range(3,30):
                continue
            # the card can connect to the corresponding discard pile
            if self.board[0,5+self.board[element]%3]//3 == self.board[element]//3-1:
                moves.append((element, (0,5+self.board[element]%3)))
        # Move cache to empty column
        for cache in full_caches:
            for column in empty_columns:
                moves.append((cache, (1, column)))
        # Move cache to connecting tail
        for cache in full_caches:
            for tail in last_elements:
                if Board._can_connect(self.board[tail], self.board[cache]):
                    moves.append((cache, (tail[0]+1, tail[1])))
        # Move cache to discard pile
        for cache in full_caches:
            if self.board[cache] not in range(3,30):
                continue
            # the card can connect to the corresponding discard pile
            if self.board[0,5+self.board[cache]%3]//3 == self.board[cache]//3-1:
                moves.append((cache, (0,5+self.board[cache]%3)))
        # Move any head to empty column
        for head in heads:
            for column in empty_columns:
                moves.append((head, (1, column)))
        # Move any head to connecting tail
        for head in heads:
            for tail in last_elements:
                if Board._can_connect(self.board[tail], self.board[head]):
                    moves.append((head, (tail[0]+1, tail[1])))
        # Collect four special cards
        vals = [self.board[element] for element in last_elements] + [self.board[cache] for cache in caches]
        for val in range(-3,0):
            if vals.count(val) == 4:
                moves.append(val)

        return moves



if __name__ == '__main__':
    board = Board(status='sorted')
    board.board[9][0:3] = [0,0,0]
    board.board[0][0:3] = [5,4,3]
    print(board)
    print(board.board)
    print('\n')

    print(board.valid_moves())
    # print(Board._find_head(board.board[:,6]))