from time import time, sleep
from .timer import Timer
from .config import PAUSE_BLOCKS, BONUS_SECONDS

class Player():

    def __init__(self, player_id, name, seconds):
        self.player_id = player_id 
        self.name = name
        self.timer = Timer(seconds)
        self.pause_blocks = PAUSE_BLOCKS
        self.out_of_game = False
        self.knock_over_tower = False
 
        self.last_time = seconds
        self.turn_index = 0
        self.fastest_move_count = 0

    def start_turn(self):
        """ start player timer, save last time """
        self.last_time = self.timer.get_seconds()
        self.timer.start()

    def pause_turn(self):
        """ pause player timer, subtract pause block """
        self.timer.pause()
        self.pause_blocks -= 1

    def current_time(self):
        """ return player's current time """
        return self.timer.get_seconds()
        
    def end_turn(self):
        """ pause player timer, add bonus seconds """
        self.timer.pause()
        if not self.out_of_time():
            self.timer.add_seconds(BONUS_SECONDS)

        self.turn_index += 1

    def status(self): #GUI
        """ return the status of the player as a string"""
        if self.out_of_game or self.out_of_time():
            return "{name} is out of the game".format(name=self.name)
        elif self.timer.active:
            return  "{name} : {time}".format(name=self.name,time=self.timer.get_seconds())
        elif not self.timer.active:
            return "{name}'s clock is paused: {time}".format(name=self.name,time=self.timer.get_seconds())

    def out_of_time(self):
        """ return True if players is out of time """
        return self.timer.get_seconds() <= 0

    def out_of_pause_blocks(self):
        """ return True if player is out of pause blocks """
        return self.pause_blocks < 1 

    def turn_time(self):
        """ return last turn time except when no turns have been taken """
        if self.turn_index == 0 or self.out_of_game:
            return None
        else:
            return round(self.last_time - self.timer.get_seconds() + BONUS_SECONDS,2)
