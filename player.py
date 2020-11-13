import pygame
import animator

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL,
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.animator = animator.Animator(pathname='Media/characters/turtle2')
        self.surf = self.animator.get_next('right')
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()


    def update(self, screen):
        screen.blit(self.surf, self.rect)

    def move(self, pressed_keys, h, w):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.surf = self.animator.get_next('left',0.5)
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.surf = self.animator.get_next('right',0.5)
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > w:
            self.rect.right = w
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= h:
            self.rect.bottom = h