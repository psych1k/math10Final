
class Player(object):
    def __init__(self, health):
        self.health = health

    def lose_health(self):
        self.health -= 1
        #return self.health
    def gain_health(self):
        self.health += 1
        #return self.health
    def get_health(self):
        return self.health
    def set_health(self, h):
        self.health = h
