import time
import pygame

#pygame.init()
pygame.mixer.init()

sound = pygame.mixer.Sound('263124_pan14_sine-octaves-up-beep.ogg')
sound.play()
time.sleep(sound.get_length())
