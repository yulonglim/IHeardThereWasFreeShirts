from User import User

class Session:
    # Constructor
    def __init__(self, chatID):
        # ChatID that this session exists in
        self.chatID = chatID

        # List of Users in the session.
        self.userList = {}

    def addUser(self, user):
        if user.id not in self.userList:
            newUser = User(self.chatID, user.username, user.id)    
            self.userList[user.id] = newUser
            return True
        else:
            return False
        

    def removeUser(self, userID):
        del self.userList[userID]


    # MUTATORS
    # def setRequestedIndex(self, index):
    #     self.requestedIndex = index




    def startAssignment(self):
        # randomise the start assignment thingy, assign each user a random user
        # for loop through the dictionary and use the inbuilt add user function
        return 0

    def messageUser(self, userID):
        # call this function everytime we assign a user. A user is ready to be messaged when he/she has the assigned user field.
        return 0

    


    

    