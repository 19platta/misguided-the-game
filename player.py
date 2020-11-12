import pygame

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
        self.surf = pygame.image.load('Media/characters/turtle/turtle right 1.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.images = [[pygame.image.load('Media/characters/turtle/turtle right 1.png').convert(),
                        pygame.image.load('Media/characters/turtle/turtle right 3.png').convert()],
                       [pygame.image.load('Media/characters/turtle/turtle right 2.png').convert(),
                        pygame.image.load('Media/characters/turtle/turtle right 4.png').convert()]]
        self.index = 0

    def update(self, screen):
        screen.blit(self.surf, self.rect)

    def move(self, pressed_keys, h, w):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[0][self.index]
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1, 0)
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[1][self.index]

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > w:
            self.rect.right = w
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= h:
            self.rect.bottom = h