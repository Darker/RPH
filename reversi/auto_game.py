#srsly...
from glob import glob as glob
from headless_reversi_creator import HeadlessReversiCreator as Gamer
import re
import time
import getopt
import sys


def find_valid_players(directory, blacklist):
    py_files = glob(directory+"/*.py")
    package_regex = re.compile("^([a-zA-Z0-9_\-\./\\\\: ]+[\\\\/])?([^/\\\\]+)\.py$")
    players = []
    for python_file in py_files:
        player = None
        matches = package_regex.match(python_file)
        if matches is None:
            continue
        module_name = matches.group(2)
        # if blacklist contains name skip it
        try:
            index = blacklist.index(module_name)
            print("Skip: ",module_name)
            continue
        except ValueError:
            # this is actually ok
            noop = 0
        try:
            player_module = __import__(module_name)
            player = player_module.MyPlayer
        except ImportError: 
            print('Error: Cannot import from: ', module_name)
        except AttributeError:
            print('Error: No player class in: ', module_name)
        except IndentationError:
            print('Error: Broken indentation in: ', module_name)
        if player is not None:
            player.module_name = module_name
            players.append(player)
            print("Loaded: ",player.module_name)
    return players

def print_results(players):
    for PlayerClass in players:
        if hasattr(PlayerClass, 'score'):
            print(PlayerClass.module_name, " => ", PlayerClass.score)

if __name__ == "__main__":
    (choices,args) = getopt.getopt(sys.argv[1:],"")
    
    players = find_valid_players(".", args)
    print("Testing ", len(players),"player classes.")
    color1 = 0
    color2 = 1
    try:
        while True:
            for MyPlayer1 in players:
                for MyPlayer2 in players:
                    print("Starting a game",MyPlayer1.module_name,"VS",MyPlayer2.module_name)
                    # skip same players, there's no reason to compare them
                    if MyPlayer1 is MyPlayer2:
                        print("  - game skipped, players are the same")
                        continue
                    player1 = MyPlayer1(color1, color2)
                    player2 = MyPlayer2(color2, color1)
                    if not hasattr(MyPlayer1, 'score'):
                        MyPlayer1.score = 0
                    if not hasattr(MyPlayer2, 'score'):
                        MyPlayer2.score = 0
                    
                    game = Gamer(player1, color1, player2, color2)
                    game.silent = True
                    winner = None
                    try:
                        winner = game.play_game()
                    except:
                        print("Error killed the game!")
                        print("Taking a break. Press Ctrl+C to terminate.")
                        time.sleep(2)
                    print("Game ends after ",game.moves,"moves.")
                    if winner==player1:
                        MyPlayer1.score += 1
                        print(MyPlayer1.module_name," won!")
                    elif winner==player2:
                        MyPlayer2.score += 1
                        print(MyPlayer2.module_name," won!")
                    else:
                        print("Everybody loses!")   
                print("---- MID RESULTS ----")
                print_results(players)
                print("\n")
    except:
        print("Error killed the loop!")
    print("---- RESULTS ----")
    print_results(players)
    print("\n")

