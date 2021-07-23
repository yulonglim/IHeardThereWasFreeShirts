from Session import Session

sessions = {};

def addSession(chatID):
    sessions[chatID] = Session(chatID);

def getSession(chatID):
    return sessions[chatID]

def sessionExists(chatID):
    return (chatID in sessions.keys())