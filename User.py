class User:

	def __init__(self, session, userId):
		self.session = session
		self.userId = userId
		self.address = ""
		self.hunger = 0
		self.diet = ""
		self.assigned = None
		self.order = 0



	def setAddress(self, address):
		self.address = address
	
	def setHunger(self, hunger):
		self.hunger = hunger

	def setOrder(self, order):
		self.order = order

	def diet(self, diet):
		self.diet = diet

	def getUsersDiet(self, user):
		return user.diet

	def setAssigned(self, assigned):
		self.assigned = assigned