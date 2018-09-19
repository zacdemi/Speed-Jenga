import pygame
import time

class Sounds():
    """ contains all sounds of the game """
 
    def __init__(self):
        pygame.mixer.init()

    def play(self,soundfile):
        sound = pygame.mixer.Sound(soundfile)
        sound.play()
        time.sleep(sound.get_length())

    def start_turn(self):
        soundfile = 'sounds/263125_pan14_sine-fifths-up-beep.ogg'
        self.play(soundfile)

    def end_turn(self):
        soundfile = 'sounds/263124_pan14_sine-octaves-up-beep.ogg'
        self.play(soundfile)

    def pause_turn(self):
        soundfile = 'sounds/263655__pan14__upward-beep-chromatic-fifths.ogg' 
        self.play(soundfile)

    def end_of_round(self):
        soundfile = 'sounds/407237__pointparkcinema__computer-chirp-2.ogg'
        self.play(soundfile)

    def out_of_game(self):
        soundfile = 'sounds/263123__pan14__sine-tri-tone-down-negative-beep-amb-verb.ogg' 
        self.play(soundfile)

    def game_over(self):
        soundfile = '' 
        self.play(soundfile)

