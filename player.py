#Player class by Stephan Green
#Creates a player object that holds the current health of the player.
#Methods modify this health variable.
#8/12/2021
class Player(object):
    def __init__(self, health):
        self.health = health

    def lose_health(self):
        self.health -= 1
    def gain_health(self):
        self.health += 1
    def get_health(self):
        return self.health
    def set_health(self, h):
        self.health = h
