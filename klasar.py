class Game:
    current = 0
    turn = 1

    def __init__(self):
        self.players = []
        self.category = ''


class Player:
    def __init__(self):
        self.name = ''
        self.id = 0
        self.score = 0
