"""
An implementation of Stonehenge.
"""

from typing import List
from math import ceil
from game import Game
from game_state import GameState


class StoneHenge(Game):
    """
    StoneHenge Game.
    p1_starts: whether p1 starts or not
    current_state: StoneHengeState
    """
    p1_starts: bool

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.
        """
        size = int(input("Enter the side-length (1-5): "))
        self.current_state = StoneHengeState(p1_starts, size)

    def get_instructions(self) -> str:
        """
        Return the instructions for this Game.
        """
        k = """
------------------------------INSTRUCTIONS-------------------------------------
Players take turns claiming cells (Letters). When a player captures at least 
half of the cells in a ley-line (@'s with a line connecting it to cells)
then the player captures that ley-line. The first player to capture at least
half of the ley-lines is the winner.

A ley-line, once claimed, cannot be taken by the other player.
-------------------------------------------------------------------------------
        """
        return k
    def is_over(self, state: "StoneHengeState") -> bool:
        """
        Return whether or not this game is over at state.
        """
        total = len(state.left_diagonal +
                    state.right_diagonal + state.horizontal)
        p1l = state.left_diagonal.count(1)
        p2l = state.left_diagonal.count(2)
        p1r = state.right_diagonal.count(1)
        p2r = state.right_diagonal.count(2)
        p1h = state.horizontal.count(1)
        p2h = state.horizontal.count(2)

        if sum([p1l, p1r, p1h]) >= int(ceil(total/2)) or \
                sum([p2l, p2r, p2h]) >= int(ceil(total/2)):
            return True
        return False

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.
        """
        return (self.current_state.get_current_player_name() != player
                and self.is_over(self.current_state))

    def str_to_move(self, string: str) -> str:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.
        """
        if not string.isalpha() and not string.isupper():
            return 'Z'
        return string


class StoneHengeState(GameState):
    """
    The state of StoneHenge at a certain point in time.

    size - the side-length of the stonehenge grid
    p1_turn - whether it is p1's turn or not
    """
    size: int
    p1_turn: bool
    constant_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                        'U', 'V', 'W', 'X', 'Y', 'Z']

    def __init__(self, is_p1_turn: bool, size: int) -> None:
        """
        Extends __init__ method from class GameState

        Initialize a StoneHenge Game State.
        Set the current player based on is_p1_turn and
        sets side_length of StoneHenge

        Precondition: 1 <= size <= 5
        """
        self.p1_turn = is_p1_turn
        self.size = size
        initial = 2
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                   'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
                   'X', 'Y', 'Z']

        self.grid = []
        for _ in range(self.size + 1):
            self.grid.append([letters.pop(0) for _ in range(initial)])
            if initial > self.size:
                initial -= 1
            else:
                initial += 1

        self.left_diagonal = []
        self.right_diagonal = []
        self.horizontal = []
        for _ in range(self.size + 1):
            self.left_diagonal.append('@')
            self.right_diagonal.append('@')
            self.horizontal.append('@')

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        bl1 = \
            """\
                  @11   @10
                 /   /
            @30 - A - B
                 \\ / \\
              @31 - C   @21
                   \\
                    @20"""
        bl2 = \
            """\
                    @12   @11
                   /   /
              @30 - A - B   @10
                 / \\ / \\ /
            @31 - C - D - E
                 \\ / \\ / \\
              @32 - F - G   @22
                   \\   \\
                    @20   @21"""
        bl3 = \
            """\
                    @13   @12
                   /   /
              @30 - A - B   @11
                 / \\ / \\ /
            @31 - C - D - E   @10
               / \\ / \\ / \\ /
          @32 - F - G - H - I
               \\ / \\ / \\ / \\
            @33 - J - K - L   @23
                \\    \\    \\
                 @20    @21    @22"""

        bl4 = \
            """\
                    @14   @13
                   /   /
              @30 - A - B   @12
                 / \\ / \\ /
            @31 - C - D - E   @11
               / \\ / \\ / \\ /
          @32 - F - G - H - I   @10
             / \\ / \\ / \\ / \\ /
        @33 - J - K - L - M - N
             \\ / \\ / \\ / \\ / \\
          @34 - O - P - Q - R   @24
                \\   \\   \\   \\
                 @20   @21   @22   @23"""

        bl5 = \
            """\
                    @15   @14
                   /   /
              @30 - A - B   @13
                 / \\ / \\ /
            @31 - C - D - E   @12
               / \\ / \\ / \\ /
          @32 - F - G - H - I   @11
             / \\ / \\ / \\ / \\ /
        @33 - J - K - L - M - N   @10
           / \\ / \\ / \\ / \\ / \\ /
      @34 - O - P - Q - R - S - T
           \\ / \\ / \\ / \\ / \\ / \\
        @35 - U - V - W - X - Y   @25
             \\   \\   \\   \\   \\
              @20   @21   @22   @23   @24"""

        if self.size == 1:
            copy = bl1
        elif self.size == 2:
            copy = bl2
        elif self.size == 3:
            copy = bl3
        elif self.size == 4:
            copy = bl4
        else:
            copy = bl5

        combined_grid = sum(self.grid, [])
        for x in range(len(combined_grid)):
            copy = copy.replace(self.constant_letters[x], str(combined_grid[x]))
        for x in range(len(self.left_diagonal)):
            copy = copy.replace('@1' + str(x), str(self.left_diagonal[x]))
        for x in range(len(self.right_diagonal)):
            copy = copy.replace('@2' + str(x), str(self.right_diagonal[x]))
        for x in range(len(self.horizontal)):
            copy = copy.replace('@3' + str(x), str(self.horizontal[x]))
        return copy

    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        return "Turn: {}, Cells: {}, Left Diagonal " \
               "LeyLines: {}, Right Diagonal LeyLines: {}, " \
               "Horizontal LeyLines: {}"\
            .format('p1' if self.p1_turn else 'p2', self.grid,
                    self.left_diagonal, self.right_diagonal, self.horizontal)

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.
        """
        lst = []
        total = len(self.left_diagonal +
                    self.right_diagonal + self.horizontal)
        p1l = self.left_diagonal.count(1)
        p2l = self.left_diagonal.count(2)
        p1r = self.right_diagonal.count(1)
        p2r = self.right_diagonal.count(2)
        p1h = self.horizontal.count(1)
        p2h = self.horizontal.count(2)
        if sum([p1l, p1r, p1h]) >= int(ceil(total / 2)) or sum(
                [p2l, p2r, p2h]) >= int(ceil(total)):
            return []

        for x in sum(self.grid, []):
            if x in self.constant_letters:
                lst.append(x)
        return lst

    def make_move(self, move: str) -> 'StoneHengeState':
        """
        Return the GameState that results from applying move to this GameState.
        """
        new_state = StoneHengeState(not self.p1_turn, self.size)
        holder = sum(self.grid, [])
        new_state.grid = []
        new_state.left_diagonal = self.left_diagonal[:]
        new_state.right_diagonal = self.right_diagonal[:]
        new_state.horizontal = self.horizontal[:]

        # Fills in grid according to updated values
        for e in range(len(holder)):
            if holder[e] == move:
                if self.p1_turn:
                    holder[e] = 1
                elif not self.p1_turn:
                    holder[e] = 2
        initial = 2
        for _ in range(self.size + 1):
            new_state.grid.append([holder.pop(0) for _ in range(initial)])
            if initial > self.size:
                initial -= 1
            else:
                initial += 1

        # Updates right_diagonal
        right_list = self.transform_to_right(new_state.grid)
        counter1 = 0
        for sublst in right_list:
            if sublst.count(1) >= int(ceil(len(sublst)/2)) and \
                    new_state.right_diagonal[counter1] not in [1, 2]:
                new_state.right_diagonal[counter1] = 1
            elif sublst.count(2) >= int(ceil(len(sublst)/2)) and \
                    new_state.right_diagonal[counter1] not in [1, 2]:
                new_state.right_diagonal[counter1] = 2
            counter1 += 1

        # Updates left_diagonal
        left_list = self.transform_to_left(new_state.grid)
        counter2 = 0
        for sublst in left_list:
            if sublst.count(1) >= int(ceil(len(sublst)/2)) and \
                    new_state.left_diagonal[counter2] not in [1, 2]:
                new_state.left_diagonal[counter2] = 1
            elif sublst.count(2) >= int(ceil(len(sublst)/2)) and \
                    new_state.left_diagonal[counter2] not in [1, 2]:
                new_state.left_diagonal[counter2] = 2
            counter2 += 1

        # Updates horizontal
        counter3 = 0
        for sublst in new_state.grid:
            if sublst.count(1) >= int(ceil(len(sublst)/2)) and \
                    new_state.horizontal[counter3] not in [1, 2]:
                new_state.horizontal[counter3] = 1
            elif sublst.count(2) >= int(ceil(len(sublst)/2)) and \
                    new_state.horizontal[counter3] not in [1, 2]:
                new_state.horizontal[counter3] = 2
            counter3 += 1

        return new_state

    def transform_to_left(self, ogrid: List[list]) -> List[list]:
        """
        Takes the grid sorted horizontally (self.grid) and returns a
        new grid sorted left diagonally. Does not mutate self.grid.
        """
        lgrid = []
        c = sum(ogrid, [])
        if self.size == 1:
            lgrid = [[c[2], c[1]], [c[0]]]
        elif self.size == 2:
            lgrid = [[c[6], c[4]], [c[5], c[3], c[1]], [c[2], c[0]]]
        elif self.size == 3:
            lgrid = [[c[11], c[8]],
                     [c[10], c[7], c[4]], [c[9], c[6], c[3], c[1]],
                     [c[5], c[2], c[0]]]
        elif self.size == 4:
            lgrid = [[c[17], c[13]], [c[16], c[12], c[8]],
                     [c[15], c[11], c[7], c[4]],
                     [c[14], c[10], c[6], c[3], c[1]], [c[9], c[5], c[2], c[0]]]
        elif self.size == 5:
            lgrid = [[c[24], c[19]], [c[23], c[18], c[13]],
                     [c[22], c[17], c[12], c[8]],
                     [c[21], c[16], c[11], c[7], c[4]],
                     [c[20], c[15], c[10], c[6], c[3], c[1]],
                     [c[14], c[9], c[5], c[2], c[0]]]
        return lgrid

    def transform_to_right(self, ogrid: List[list]) -> List[list]:
        """
        Takes the grid sorted horizontally (self.grid) and returns a
        new grid sorted right diagonally. Does not mutate self.grid.
        """
        rgrid = []
        c = sum(ogrid, [])
        if self.size == 1:
            rgrid = [[c[0], c[2]], [c[1]]]
        elif self.size == 2:
            rgrid = [[c[2], c[5]], [c[0], c[3], c[6]], [c[1], c[4]]]
        elif self.size == 3:
            rgrid = [[c[5], c[9]], [c[2], c[6], c[10]],
                     [c[0], c[3], c[7], c[11]], [c[1], c[4], c[8]]]
        elif self.size == 4:
            rgrid = [[c[9], c[14]], [c[5], c[10], c[15]],
                     [c[2], c[6], c[11], c[16]],
                     [c[0], c[3], c[7], c[12], c[17]],
                     [c[1], c[4], c[8], c[13]]]
        elif self.size == 5:
            rgrid = [[c[14], c[20]], [c[9], c[15], c[21]],
                     [c[5], c[10], c[16], c[22]],
                     [c[2], c[6], c[11], c[17], c[23]],
                     [c[0], c[3], c[7], c[12], c[18], c[24]],
                     [c[1], c[4], c[8], c[13], c[19]]]
        return rgrid

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        """
        total = len(self.left_diagonal +
                    self.right_diagonal + self.horizontal)
        if self.p1_turn:
            return self.helper_function_p1(total)
        return self.helper_function_p2(total)

    def helper_function_p1(self, total: int) -> int:
        """
        Helper function for rough_outcome
        """
        p2_wins = []
        for move in self.get_possible_moves():
            new_state = self.make_move(move)
            p1l = new_state.left_diagonal.count(1)
            p1r = new_state.right_diagonal.count(1)
            p1h = new_state.horizontal.count(1)
            if sum([p1l, p1r, p1h]) >= int(ceil(total / 2)):
                return 1

            p2_wins_mini = []
            for p2_move in new_state.get_possible_moves():
                new_state_p2 = new_state.make_move(p2_move)
                p2l = new_state_p2.left_diagonal.count(2)
                p2r = new_state_p2.right_diagonal.count(2)
                p2h = new_state_p2.horizontal.count(2)
                if sum([p2l, p2r, p2h]) >= int(ceil(total / 2)):
                    p2_wins_mini.append(True)

            if any(p2_wins_mini):
                p2_wins.append(True)

        if len(p2_wins) == len(self.get_possible_moves()):
            return -1
        return 0

    def helper_function_p2(self, total: int) -> int:
        """
        Helper function for rough_outcome
        """
        p1_wins = []
        for move in self.get_possible_moves():
            new_state = self.make_move(move)
            p2l = new_state.left_diagonal.count(2)
            p2r = new_state.right_diagonal.count(2)
            p2h = new_state.horizontal.count(2)
            if sum([p2l, p2r, p2h]) >= int(ceil(total / 2)):
                return 1

            p1_wins_mini = []
            for p1_move in new_state.get_possible_moves():
                new_state_p1 = new_state.make_move(p1_move)
                p1l = new_state_p1.left_diagonal.count(1)
                p1r = new_state_p1.right_diagonal.count(1)
                p1h = new_state_p1.horizontal.count(1)
                if sum([p1l, p1r, p1h]) >= int(ceil(total / 2)):
                    p1_wins_mini.append(True)

            if any(p1_wins_mini):
                p1_wins.append(True)

        if len(p1_wins) == len(self.get_possible_moves()):
            return -1
        return 0


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
