class User:
    def __init__(self, name):
        self.name = name
        self.score = 0
    
    def update_score(self, points):
        self.score += points
    