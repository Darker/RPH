from player_abstract import MyPlayer as AbstractPlayer
# for analysing how much time remaining does the player have to think
import time
# for infinity. Infinity is cool
import math

class MyPlayer(AbstractPlayer):
    '''This is player that tries to predict what the score will be next turn or more turns after that
       and picks option that yields best score when all enemy moves are just as likely
       
       This is typically called state space breadth first search.
    '''
    def find_position(self, board):
        (results, moves, boards) = self.best_future_score(board,950)
        #(results, moves, boards) = profile.runctx('self.best_future_score(board)', globals(), locals())
        if len(moves)==0:
            return None
        else:
            max_score = max(results)
            #print(results)
            index = results.index(max_score)
            return moves[index]
    @property
    def enemy(self):
        return MyPlayer(self.color, self.opponent_color, self.neutral_color)
    # sums up score posibilities in next turn
    # if no more turns are possible, returns nan
    #@profile
    def future_score(self, board, player, start_time=-1, timeout=800):
        #global playerskip
        #global calls
        #calls += 1
        # the `scores` is used for caching the turned stones to speed
        # up the algorighm
        available_moves, scores = board.get_positions_and_scores(player, False)
        # this is slightly more optimal than checking player.can_play
        if len(available_moves)==0:
            player = self if player!=self else self.enemy
            available_moves, scores = board.get_positions_and_scores(player, False)
            #playerskip+=1
            #print("PLAYERSKIP! "+str(playerskip)+" / "+str(calls))
        # array of end results in the form of 1, -1 or zero based on 
        # whether this (self) player wins or loses for every game variant
        results = []
        # array of boards of future options
        boards = []
        
        # game ovar
        # calculate result and return it as only result
        # rest arrays shall be empty
        if len(available_moves)==0:
            balance = board.balance(self)
            # This makes the algorithm avoid branches that contain defeat
            # but it does not risk so much for victory
            results.append(balance*50 if balance>0 else balance*1000)
            boards.append(board)
        else:
            move_index = 0
            #board_place = board.place
            for move in available_moves:
                if not haz_tim(start_time, timeout):
                   break
                tmp_board = board.clone()
                tmp_board.place(move, player, scores[move_index])
                #results.append(tmp_board.balance_from_cache(self))
                score = tmp_board.score_from_cache(self)
                results.append(score[0]-score[1])
                boards.append(tmp_board)
                
                move_index+=1
        return (results, available_moves, boards)
    # My attempt on breadth first search. Curiously, I've actually never done this
    # tries to generate as many levels of depth as possible
    # and sums their win/loss rating
    # enemy moves are considered all equally likely, which means
    # the final rating is not weighted
    def best_future_score(self, board, timeout = 900):
        # current level of depth
        level = 0
        # no of level that was finished completely
        succesful_level = 0
        
        enemy = self.enemy
        board.set_players(self, enemy)

        # we know that, lest this method wouldn't get called
        board.currentTurn = 0
        # used to stop before timeout
        start_time = time.clock()*1000
        # measures time required to calculate each level of depth
        level_time = start_time
        last_level_duration = 0
        base_results, base_moves, base_boards = self.future_score(board, self)
        # temporary results that are added directly into `base_results` once
        # full level of breadth is finished
        tmp_results = []
        for i in base_results:
            tmp_results.append(0)
        # this will be filled with predictions, which will then spawn more predictions ad infinitum
        # prediction format: [list of results, list of moves, list of boards, player who played, level index, origin]
        #                 0             1           2            3     4   5
        options_trees = [[base_results, base_moves, base_boards, self, 0, -1]]

        while len(options_trees)>0 and haz_tim(start_time, timeout):
            prev_prediction = options_trees[0]
            # If new prediction's level is higher than current, put
            # tmp results in base results
            if prev_prediction[4]>level:
                if level>0:
                    for i in range(0, len(base_results)):
                        result = tmp_results[i]
                        tmp_results[i] = 0
                        # Still not sure if I should add or overwrite
                        base_results[i] += result/(level*2)
                succesful_level = level
                print("Predicting LVL "+str(level)+" stats:\n    ", end="")
                self.print_prediction(base_results, base_moves)
                level = prev_prediction[4]
                # calculation of time
                #time_now = time.clock()*1000 
                #last_level_duration = time_now - level_time
                #level_time = time_now
                # if this level took more time to finish than the remaining time, 
                # it's pointless to continue
                #if last_level_duration>time_now-start_time:
                #    break
            #print("Predicting LVL "+str(level)+" time remaining "+str(time_remains(start_time, timeout))+" ms")
            board_index = 0
            # for every possible board
            for cur_board in prev_prediction[2]:
                # this if actually checks if prev_prediction is
                # end game prediction or not
                # in the former case, there will be no valid moves
                if len(prev_prediction[1]) != 0:
                    cur_playa = cur_board.cur_playa()#self if prev_prediction[3]!=self else enemy
                    prediction = list(self.future_score(cur_board, cur_playa))
                    # remembers who played
                    prediction.append(cur_playa)
                    # Level increases by one
                    prediction.append(prev_prediction[4]+1)
                    # origin inherited unless this is the first level
                    prediction.append(board_index if prev_prediction[4]==0 else prev_prediction[5])
                    options_trees.append(prediction)
                    #print("    PREDICTION ", end="");
                    #print(prediction[0])
                #else:
                    #print("    END GAME PREDICTION!", end="")
                    #print(prev_prediction[0])
                # add current prediction's stats to base stats
                if prev_prediction[4]!=0:
                    tmp_results[prev_prediction[5]] += prev_prediction[0][board_index]
                board_index += 1
            # remove processed prediction from queue
            options_trees.pop(0)
        #print("Predict end last LVL "+str(succesful_level))
        return (base_results, base_moves, base_boards)
    def print_prediction(self, predictions, base_moves):
        index = 0
        length = len(predictions)
        while index<length:
            print("    ",base_moves[index]," = ",predictions[index])
            index+=1
        
        
def haz_tim(start_time, timeout):
    if start_time<0 or timeout<0:
        return True
    return (time.clock()*1000-start_time)<timeout
def time_remains(start_time, timeout):
    if start_time<0 or timeout<0:
        return math.inf
    return timeout-(time.clock()*1000-start_time)
