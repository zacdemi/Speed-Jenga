import pygame
import time

class Sounds():
    """ contains all sounds of the game """
 
    def __init__(self):
        pygame.mixer.init()

    def stop_all(self):
        pygame.mixer.stop()

    def start_turn(self):
        soundfile = 'sounds/263125_pan14_sine-fifths-up-beep.ogg'
        pygame.mixer.Sound(soundfile).play()

    def end_turn(self):
        soundfile = 'sounds/263124_pan14_sine-octaves-up-beep.ogg'
        pygame.mixer.Sound(soundfile).play()

    def pause_turn(self):
        soundfile = 'sounds/263655__pan14__upward-beep-chromatic-fifths.ogg' 
        pygame.mixer.Sound(soundfile).play()

    def end_of_round(self):
        soundfile = 'sounds/407237__pointparkcinema__computer-chirp-2.ogg'
        pygame.mixer.Sound(soundfile).play()

    def out_of_game(self):
        soundfile = 'sounds/263123__pan14__sine-tri-tone-down-negative-beep-amb-verb.ogg' 
        pygame.mixer.Sound(soundfile).play()

    def warning(self):
        soundfile = 'sounds/10_second_countdown.ogg'
        pygame.mixer.Sound(soundfile).play()
