import pygame
from pygame import Surface
import pygame.sprite
import pygame.transform

class Monster(pygame.sprite.Sprite):
    def __init__(self,screen:Surface, img,x:int, y:int, move:int=25, speed:int=1):
        pygame.sprite.Sprite.__init__(self)
            
        self.screen = screen        
        # img = pygame.image.load(f'{filename}').convert_alpha()
        self.image = pygame.transform.scale(img,(40,40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = speed
        self.move = move
        self.delay_counter = 0

    def update(self):
        self.rect.x += self.direction
        self.delay_counter += 1
        if abs(self.delay_counter) > self.move:
            self.direction *= -1
            self.delay_counter *= -1