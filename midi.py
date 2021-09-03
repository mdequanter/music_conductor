import pygame.midi
import time

pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)
player.note_on(60, 127)
time.sleep(1)
player.note_off(60, 127)
player.note_on(62, 127)
time.sleep(1)
player.note_off(62, 127)

del player
pygame.midi.quit()