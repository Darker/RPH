
#Testovaci kod
if __name__ == "__main__":
    board = [
     #   0 1 2 3 4 5 6 7
        [0,0,0,0,0,0,0,0],# 0
        [0,0,0,0,0,0,0,0],# 1
        [0,0,0,0,0,0,0,0],# 2
        [0,0,0,1,2,0,0,0],# 3
        [0,0,0,2,1,0,0,0],# 4
        [0,0,0,0,0,0,0,0],# 5
        [0,0,0,0,0,0,0,0],# 6
        [0,0,0,0,0,0,0,0] # 7
    ]
    board = Board(board)
    player = MyPlayer(1, 2, 0)
    from predictive_player import MyPlayer as OtherPlayer
    console_player = OtherPlayer(2, 1, 0)
    console_player.enemy_ = player
    player_enemy = console_player
    
    board.printMe(1, 2, 0)
    while True:
        move = player.move(board)
        moves = 0;
        #if move is not None:
        #    print("[" + ", ".join( str(x) for x in move) + "]")
        #else:
        #    print("No valid move...")
        if move is not None:
            board.place(list(move), player)
            print("Computer (simple) played:")
            board.printMe(1, 2, 0)
            moves+=1
        if  console_player.can_play(board):
            #move = console_player.move_via_console(board) 
            move = list(console_player.move(board))
            board.place(move, console_player)
            print("Advanced opponent played:")
            board.printMe(1, 2, 0)
            moves+=1
        if moves==0:
            break
    result = board.balance(player)
    if result>0:
        print("Base player wins!")
    elif result==0:
        print("Nobody wins!")
    else:
        print("Guest player wins!")
    #print '[%s]' % ', '.join(map(str, p))