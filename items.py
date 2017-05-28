import pygame

class Sword:
    def __init__(self, damage, reach, attack_speed, mass, special_list = []):           # Create class for the Swords
        self.damage = damage
        self.reach = reach
        self.attack_speed = attack_speed
        self.mass = mass
        self.special_list = special_list

class Gun():
    def __init__(self, damage, bullets_shot, bullet_speed, attack_speed, mass, special_list = []):        # Create class for the Guns
        self.damage= damage
        self.bullets_shot = bullets_shot
        self.bullet_speed = bullet_speed
        self.attack_speed = attack_speed
        self.mass = mass
        self.special_list = special_list

class ArmorPiece():
    def __init__(self, health, armor):
        self.health = health
        self.armor = armor

