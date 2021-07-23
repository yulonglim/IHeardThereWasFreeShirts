class Session:
    # Constructor
    def __init__(self, chatID):
        # ChatID that this session exists in
        self.chatID = chatID

        # List of Users in the session.
        self.userList = []

    #TODO append user instead of their userID
    def addUser(self, userID):
        self.userList.append(userID)
    
    # MUTATORS
    # def setRequestedIndex(self, index):
    #     self.requestedIndex = index