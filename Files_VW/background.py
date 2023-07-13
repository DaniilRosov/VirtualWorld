import pygame
import image
from settings import *
# from main import *

class Background:
    def __init__(self,background_image):
        self.image = image.load(f"Assets/{background_image}", size=(SCREEN_WIDTH, SCREEN_HEIGHT),
                                convert="default")


    def draw(self, surface):
        image.draw(surface, self.image, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), pos_mode="center")
