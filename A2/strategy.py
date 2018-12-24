"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any
import copy


# TODO: Adjust the type annotation as needed.
def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


# TODO: Implement a recursive version of the minimax strategy.
def recursive_minimax(game: Any) -> Any:
    """
    Recursively return the most optimal move for game
    """
    lst = []
    moves = game.current_state.get_possible_moves()
    for move in game.current_state.get_possible_moves():
        new_game = copy.deepcopy(game)
        new_state = new_game.current_state.make_move(move)
        new_game.current_state = new_state
        lst.append(helper_recursion(new_game) * -1)
    return moves[lst.index(max(lst))]


def helper_recursion(game) -> list:
    """
    Helper Function for recursive_minimax.
    """
    if game.is_over(game.current_state) \
            and game.is_winner(game.current_state.get_current_player_name()):
        return 1
    elif game.is_over(game.current_state) and not \
            game.is_winner(game.current_state.get_current_player_name()):
        return -1
    elif game.is_over(game.current_state) \
            and not game.is_winner('p1') and not game.is_winner('p2'):
        return 0
    lst = []
    for move in game.current_state.get_possible_moves():
        new_game = copy.deepcopy(game)
        new_state = new_game.current_state.make_move(move)
        new_game.current_state = new_state
        lst.append(new_game)
    return max([(helper_recursion(new) * -1) for new in lst])

# Class Stack and Tree Taken from lecture


class Stack:
    """
    Last-in, first-out (LIFO) stack.
    This class was taken from lecture.
    """

    def __init__(self) -> None:
        """
        Create a new, empty Stack self.
        """
        self._contains = []

    def add(self, obj: object) -> None:
        """
        Add object obj to top of Stack self.
        """
        self._contains.append(obj)

    def remove(self) -> object:
        """
        Remove and return top element of Stack self.
        Assume Stack self is not emp.
        """
        return self._contains.pop()

    def is_empty(self) -> bool:
        """
        Return whether Stack self is empty.
        """
        return len(self._contains) == 0


class Tree:
    """
    A bare-bones Tree ADT that identifies the root with the entire tree.
    value: value of root node
    children: child nodes
    This class was taken from lecture.
    """
    def __init__(self, value=None, children=None, score=None):
        """
        Create Tree self with content value and 0 or more children
        """
        self.value = value
        self.score = score
        self.children = children[:] if children is not None else []


def iterative_minimax(game: Any) -> Any:
    """
    Iteratively return the most optimal move for game
    """
    stk = Stack()
    init_game = copy.deepcopy(game)
    init_game_tree = Tree(init_game)
    stk.add(init_game_tree)
    while not stk.is_empty():
        tree = stk.remove()
        if tree.value.is_over(tree.value.current_state):
            if tree.value.is_winner\
                        (tree.value.current_state.get_current_player_name()):
                tree.score = 1
            elif not tree.value.is_winner\
                        (tree.value.current_state.get_current_player_name()):
                tree.score = -1
            elif not tree.value.is_winner('p1') \
                    and not tree.value.is_winner('p2'):
                tree.score = 0

        elif tree.children == []:
            for move in tree.value.current_state.get_possible_moves():
                new_game = copy.deepcopy(tree.value)
                new_game.current_state = new_game.current_state.make_move(move)
                new_child = Tree(new_game)
                tree.children.append(new_child)
            stk.add(tree)
            for tree_child in tree.children:
                stk.add(tree_child)

        elif tree.children != []:
            lst = []
            for child in tree.children:
                lst.append(child.score * -1)
            tree.score = max(lst)

    for child in init_game_tree.children:
        if child.score * -1 == init_game_tree.score:
            return (init_game_tree.value.current_state.
                    get_possible_moves()[init_game_tree.children.index(child)])
    return None


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
