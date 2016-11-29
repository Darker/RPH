#from __future__ import print_function
from board import Board
# Je to ochcavka abych nemusel pri uploadu prejmenovavat soubory,
# staci zmenit z jakeho souboru importuju
from player_greedy_weighted import MyPlayer as SomePlayer

class MyPlayer(SomePlayer):
    '''Tento hrac nacita jinaho hrace (tridu) a za toho hraje.'''
    # Toto byl neuspesny pokus zabranit odevzdavacimu systemu aby tvrdil,
    # ze tato trida neexistuje. Nepomohlo to.
    def NOOP(self):
        return None
