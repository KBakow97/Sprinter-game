from ctypes.wintypes import PULARGE_INTEGER
import pygame
from random import randint
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(
            'graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load(
            'graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load(
            'graphics/player/jump.png').convert_alpha()
        self.player_crouch1 = pygame.image.load(
            'graphics/player/player_crouch1.png').convert_alpha()
        self.player_crouch2 = pygame.image.load(
            'graphics/player/player_crouch2.png').convert_alpha()
        self.player_crouch = [self.player_crouch1, self.player_crouch2]
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/audio_jump.mp3')
        self.jump_sound.set_volume(0.3)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        keys = pygame.key.get_pressed()
        if self.rect.bottom < 300:
            self.image = self.player_jump
        elif keys[pygame.K_DOWN] == False:
            self.rect = self.image.get_rect(midbottom=(80, 300))
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_crouch):
                self.player_index = 0
            self.image = self.player_crouch[int(self.player_index)]
            self.rect = self.image.get_rect(midbottom=(75, 300))

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly__1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly__2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly__1, fly__2]
            y_pos = 223
        else:
            snail_1 = pygame.image.load(
                'graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load(
                'graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(
            midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):

        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


class BG(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        main_image = pygame.image.load('graphics/Sky1.jpg').convert()
        self.image = pygame.Surface((WINDOW_WIDTH * 2, WINDOW_HEIGHT))
        self.image.blit(main_image, (0, 0))
        self.image.blit(main_image, (WINDOW_WIDTH, 0))
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 300 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)


class Ground(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/ground.png').convert_alpha()
        self.rect = self.image.get_rect(bottomleft=(0, 465))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 360 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)
