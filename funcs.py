import pygame
import math


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def cycle_angle(angle):
    """ Functino used to convert a negative angle to a positive one"""
    if angle < 0:
        angle += math.pi * 2
    return angle


def remove_from_group(level, item, group=None):                    # Might be obsolete if kill is used
    """ Function use to remove sprites from the current_level groups"""
    level.object_list.remove(item)
    if group is not None:
        group.remove(item)


def add_to_group(level, item, group=None):
    """ Function use to add sprites from the current_level groups"""
    level.object_list.add(item)
    if group is not None:
        group.add(item)

def distance(object_1 , object_2):
    """ Find distance between two sprites"""
    x = object_2.rect.centerx - object_1.rect.centerx
    y = object_2.rect.centery - object_1.rect.centery
    return math.sqrt(y**2 + x**2)

def angle_between(object_1, object_2):
    y = object_2.rect.centery - object_1.rect.centery
    x = object_2.rect.centerx - object_1.rect.centerx
    return math.atan2(y, x)

def resize():
    for event in pygame.event.get():
        if event == pygame.VIDEORESIZE:
            print('yes')