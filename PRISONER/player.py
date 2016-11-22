from numbers import Number
class MyPlayer:
	"""I seriously wonder why we're supposed to prepend class' names with 'my'"""
	iterations = -1
	payoff = None
	#const
	COOPERATE = 0
	DEFECT = 1
	STRATEGY = ["COOPERATE", "DEFECT"]
	ME = 0
	ENEMY = 1
	CHARACTER = ["ME", "ENEMY"]
	default_matrix = [ 
		#  C     D
		[(4,4),(1,6)] ,# C
		[(6,1),(2,2)]  # D
	]
	z_prednasky = [ 
		#  C     D
		[(3,3),(1,4)] ,# C
		[(4,1),(2,2)] # D
	]
	def __init__(self, payoff, iterations=-1):
		if not isinstance(payoff, list) or len(payoff)!=2 or len(payoff[0])!=2 or len(payoff[1])!=2:
			raise TypeError("Payof mattrix must be nested list!")
		if isinstance(iterations, Number):
			self.iterations = iterations
		self.payoff = payoff
		self.history = []
		
		# determine best strategy
		#in this array, count will be presented for every case where strategy is favored
		#best_strats = [0, 0];
		#for 
		
		# let's start with naive impl
		# this says that if value of situation where I C, he D, is higher than if I D he D, then I C and vice versa
		#  
		#if_d = self.payoff[self.COOPERATE][self.DEFECT]<self.payoff[self.DEFECT][self.DEFECT] ? self.COOPERATE : self.DEFECT
		#if_c = self.payoff[self.COOPERATE][self.COOPERATE]<self.payoff[self.DEFECT][self.COOPERATE] ? self.COOPERATE : self.DEFECT
		
	def move(self):
		# not sure yet
		# ok fakit just defect every time
		return False
	# Move must be boolean or else!
	def record_opponents_move(self, move):
		self.history.append(move)

# Just a testing section
if __name__ == "__main__":
    print(MyPlayer.CHARACTER[0])
    player = MyPlayer(MyPlayer.default_matrix)
    player.move()