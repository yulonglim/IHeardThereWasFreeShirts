class Session:
    # Constructor
    def __init__(self, chatID):
        # ChatID that this session exists in
        self.chatID = chatID

        # List of Users in the session.
        self.userList = []
    
    # MUTATORS
    # def setRequestedIndex(self, index):
    #     self.requestedIndex = index