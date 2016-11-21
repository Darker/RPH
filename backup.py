    def find_opponent_stones(self, direction, start, player):
        #print("   Finding enemy stones at "+self.strpos(start)+" in direction "+self.strpos(direction))
        # starting directly at 'next' field.
        # btw it made this algorithm WAY faster when I put 
        # the addition in the list ctor instead of incrememting it later
        #pos = [start[0]+direction[0], start[1]+direction[1]]
        row = start[0]+direction[0]
        col = start[1]+direction[1]
        #if not (pos[0]>=0 and pos[1]>=0 and pos[0]<self.rows and pos[1]<self.cols):
        #    return []
        first_iteration = True
        # several variables are defined inside the loop so they're only defined
        # when needed
        # these:
        #   fields = []
        ended_properly = False
        #while self.isValidPos(pos):
        # While condition replaced with inline
        # because just as any other interpreted language
        # python sucks at inlining
        while pos[0]>=0 and pos[1]>=0 and pos[0]<self.rows and pos[1]<self.cols:
            #current_color = self[pos];
            current_color = self.board[pos[0]][pos[1]]
            if first_iteration:
                #opponent_color = player.opponent_color
                if current_color != player.opponent_color:
                    #print("     First stone not enemies' at "+self.strpos(pos))
                    break
                fields = []
                
            else:
                if current_color == player.color:
                    ended_properly = True
                    break;
                elif current_color == player.neutral_color:
                    #ending if free space was reached
                    break;
            first_iteration = False
            fields.append([pos[0], pos[1]])
            #print("Adding "+self.strpos(pos)+" to list of claimed points.")
            pos[0]+=direction[0]
            pos[1]+=direction[1]