import player_abstract
import sys
if sys.version_info < (3, 0):
    def console_input(prompt):
        return raw_input(prompt)
else:
    def console_input(prompt):
        return input(prompt)
class MyPlayer(player_abstract.MyPlayer):
    # prompts player to make a move via standard input
    # todo: remove this after debug
    def find_position(self, board):
        board = self.wrap_board_if_needed(board)
        zeman = "kunda"
        fails = 3
        while zeman=="kunda":
            i,j = console_input("Enter two values:  ").split()
            i = int(i)
            j = int(j)
            if board.is_valid_move([i, j], self):
                return [i, j]
            else:
                fails-=1
                if fails>0:
                    print("Invalid move! Enter valid values - "+str(fails)+" attempts remaining.")
                else:
                    raise ValueError("Too many invalid move attempts!")  