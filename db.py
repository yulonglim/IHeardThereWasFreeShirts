from Session import Session

# uh this is just a dictionary of sessions, in which has a dictionary of users
sessions = {};

def addSession(chatID):
    sessions[chatID] = Session(chatID);

def getSession(chatID):
    return sessions[chatID]

def getSessions():
    return sessions

def sessionExists(chatID):
    return (chatID in sessions.keys())

def deleteSession(chatID):
    if sessionExists(chatID):
        del sessions[chatID]
        return True
    else:
        return False