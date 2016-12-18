class Game:
    current = 0     # Halda utan um hver á að gera að  hverju sinni
    turn = 1        # Heldur utan um fjölda umferða sem eru búnar, hvenær á að enda leikinn

    def __init__(self):
        self.players = []
        self.category = ''
        self.categories = ''


class Player:
    def __init__(self):
        self.name = ''
        self.id = 0
        self.score = 0
