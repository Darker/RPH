class MyVector:
	"""Vector class"""
	coordinates = None
	def __init__(self, coordinates):
		if not isinstance(coordinates, list):
			raise TypeError("Coordinates of vector must be single dimensional array.")
		self.coordinates = coordinates
	def get_vector(self):
		return self.coordinates
	def dimensions(self):
		return len(self.coordinates)
	def __mul__(self,other):
		if other.dimensions() != self.dimensions():
			raise ValueError("Number of dimensions of multiplied vectors must be equal.")
		#tmp = 0
		#for index in range(self.dimensions()):
		#	tmp += self.coordinates[index] * other.coordinates[index]
		#return tmp
		return sum(a * b for a, b in zip(self.coordinates, other.coordinates))
		
# Just a testing section recommended in the assignment
if __name__ == "__main__":
	vec1 = MyVector([1,2,5,5,5]) # vektory mohou byt i jine dimenze nez 3!
	vec2 = MyVector([1,2,5,5,5]) 
	print(vec1.get_vector()) # Test getting the list of items
	dot_product = vec1*vec2  # Multiplication test
	print(dot_product)