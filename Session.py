import random

import requests

from User import User

class Session:
    # Constructor
    def __init__(self, chatID):
        # ChatID that this session exists in
        self.chatID = chatID
        self.status = False

        # List of Users in the session.
        self.userList = {}

        # Price range for the group
        self.priceRange = ""

    def addUser(self, user):
        if user.id not in self.userList:
            newUser = User(self.chatID, user.username, user.id)
            self.userList[user.id] = newUser
            self.messageUser(user.id, 'You have opted in')
            return True
        else:
            return False

    def removeUser(self, user):
        if user.id in self.userList:
            del self.userList[user.id]
            self.messageUser(user.id, 'You have opted out')
            return True
        else:
            return False

    def getUserList(self):
        print(list(self.userList.keys()))
        return list(self.userList.keys())

    def startSession(self):
        if self.status:
            return False
        else:
            self.status = True
            self.startAssignment()
            return True

    def startAssignment(self):
        # randomise the start assignment thingy, assign each user a random user
        # for loop through the dictionary and use the inbuilt add user function
        keys = list(self.userList.keys())
        random.shuffle(keys)
        for index, key in enumerate(keys):
            if index + 1 == len(keys):
                self.userList[key].setAssigned(self.userList[keys[0]])
            else:
                self.userList[key].setAssigned(self.userList[keys[index + 1]])
        for i in self.userList.values():
            self.messageUser(i.userId, "What is your address? Please type '/details' followed by your current address and any extra note you would like to add for the sender!")



    def messageUser(self, userID , message):
        # call this function everytime we assign a user. A user is ready to be messaged when he/she has the assigned user field.
        send_text = 'https://api.telegram.org/bot1855391169:AAGuzaD2E6AA_mDPXRIuhT5IPv9JZ3ERlFU/sendMessage?chat_id=' + str(userID) + '&parse_mode=Markdown&text=' + message

        response = requests.get(send_text)

        return response.json()


    


    

    