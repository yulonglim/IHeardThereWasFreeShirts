class User:

	def __init__(self, session, username, userId):
		self.session = session
		self.username = username
		self.userId = userId
		self.address = ""
		self.hunger = 0
		self.assigned = None
		self.order = 0

	def setAddress(self, address):
		self.address = address
	
	def setHunger(self, hunger):
		self.hunger = hunger

	def setOrder(self, order):
		self.order = order

	def getUsersDiet(self, user):
		return user.diet

	def setAssigned(self, assigned):
		self.assigned = assigned