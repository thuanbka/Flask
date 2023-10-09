class User():

    def __init__(self, username, password, role=None):
        self.username = username
        self.password = password
        self.role = role

    def getPassword(self):
        return self.password
    
    def setPassword(seld, password):
        seld.password = password
    
    def getUsername(self):
        return self.username
    
    def setUsername(self, username):
        self.username = username

    def getRole(self):
        return self.role

    def setRole(self, role):
        self.role = role