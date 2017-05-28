from funcs import *
import math
import pygame

class AnimationBox(pygame.sprite.Sprite):               # Class to contain the animations used
    def __init__(self, current_level, frames, folder, x, y, width, height, angle=30):
        super().__init__()
        self.angle = angle * 180 / math.pi
        self.frames = frames
        self.folder = folder
        self.current_frame = 0
        self.width = width
        self.height = height
        self.image = pygame.image.load(self.folder + str(self.current_frame)+'.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.centerx = x
        self.rect.centery = y
        self.image = rot_center(self.image, self.angle)
        self.level = current_level

    def update(self):                                           # TODO: Make more efficient image changing system.
        """Function to change the frame of the animation"""
        self.current_frame += 1
        self.image = pygame.image.load(self.folder + str(self.current_frame)+'.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = self.image.convert()

        print(self.x)
        print(self.level.world_shift_x)

        if self.current_frame >= self.frames:
            self.kill()
            print(self, 'KILLED')




class PlayerAbilities:
    """ Class that takes in a character and launches all of the abilities for that character.
     A way to store all of the ability functions the game has."""

    def __init__(self, character):
        self.char = character
        self.current_level = character.level


    def dash(self, mouse_angle, frame = 0):
        level = self.char.abilities_all['dash']
        if level > 0:
            dash_speed = 80
            if self.char.timer['dash'] > 0:
                self.char.move_char(dash_speed * math.cos(mouse_angle),
                                    dash_speed * math.sin(mouse_angle))
                anim_box = AnimationBox(self.current_level, 2,  'Squares/', self.char.rect.centerx, self.char.rect.centery,
                                                  self.char.sword_reach*1, self.char.sword_reach*1)
                anim_box.level = self.current_level
                add_to_group(self.current_level, anim_box)
                for enemy in self.current_level.enemies:
                    d = distance(self.char, enemy)
                    if d < self.char.sword_reach/2:
                        enemy.health -= self.char.sword_damage * 100
        if self.char.timer['dash'] == 0:
            return 'Done'

    def whirlwind(self, null):
        level = self.char.abilities_all['whirlwind']
        if level > 0:
            if self.char.timer['whirlwind'] > 0:
                anim_box = AnimationBox(self.current_level, 2,  'Squares/', self.char.rect.centerx, self.char.rect.centery,
                                                  self.char.sword_reach*1, self.char.sword_reach*1)
                anim_box.level = self.current_level
                add_to_group(self.current_level, anim_box)
                for enemy in self.current_level.enemies:
                    print('distance', distance(self.char, enemy))
                    if distance(self.char, enemy) < self.char.sword_reach * 1.1:
                        enemy.health -= self.char.sword_damage * 100
                        print(enemy.health)
        if self.char.timer['whirlwind'] == 0:
            return 'Done'


