# A Thingy for Solitaire in Shenzhen-I/O
not sure what this is about yet, still under development

## Features
* Read board status from game
* Calculate moves
* Return recommendation

## Board Representation
* Deck representation using modulo
    * 饼=0, 条=1, 万=2
    * Deck ID = 数值*3 + 花色
    * 数值 = Deck ID // 3
    * 花色 = Deck ID % 3
    * Deck ID is a value from 3 to 29, inclusive
* Special Cards
    * 中=-1, 发=-2, 白=-3, 花=1, empty=0
* Board structure
    * 14*8 matrix to represent board\
        * consider the longest column: 5 cards dealt ending with 9, and then 8-1 following behind. Together with the first row for cache the column number is 14.
    * 7 element list to represent top row
    * If a 中 is just put on the top row it is represented by -1. If four 中 is collected on the top row it is represented by -4 (-1*4). This can be quickly checked by value//4==0.
* Other terms
    * A `head` to `tail` is a sequence of cards from a larger number to a smaller number in one column, with varying colors. `head` and `tail` represents the position of the largest and smallest card in the sequence, respectively. 

## Moves
* Operations
    * New Board = Operation(Board)
    * Operations = valid(Board), returns list of valid operations
* Score(Operation)
    * A function that measures how good an operation is
    * Forming a new head to tail: length of the connection
    * Stacking four 中发白: some constant C1
    * Making an empty column: some constant C2
    * If a board returns to a previous board state in the tree, penalize with some large negative constant C0
    * If a board has no valid operations, penalize with some large negative constant C0
* Algorithm
    * Traverses a tree of boards connected by operations up to a certain depth n, pick board with largest sum of operations

## Operations
* Each operation includes manual operation and automatic operation
* Manual operation:
    * Moving a set of cards from one column to another
    * Moving one card from board to top row
    * Moving one card from top row to board
Collecting all four 中发白
* Automatic operation happens after manual operation:
    * Moving 花 from board to top row
    * Moving cards with small values to the top row
    * Score(Operation) = Score(Manual) + Score (Automatic)