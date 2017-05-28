import random
from Abilities import *
from items import *
from funcs import *
import pickle


class Character(pygame.sprite.Sprite):              # The guy appearing on the map is the Character
    def __init__(self, x, y, sword, gun):
        super().__init__()
        # General properties
        self.win = False
        self.health = 100
        self.cycle = 0
        self.hit = False
        self.image = pygame.image.load('char.jpg')
        self.image = self.image.convert()
        self.originalImage = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.shift_x = 0
        self.shift_y = 0
        self.v_x = 0
        self.v_y = 0
        self.speed = 5

        # Weapons
        self.sword = sword
        self.gun = gun
        self.sword_damage = self.sword.damage
        self.sword_reach = self.sword.reach
        self.bullet_speed = self.gun.bullet_speed
        self.gun_damage = self.gun.damage

        # Abilities

        self.ability_selector = 0
        self.abilities_all = {'dash': 1, 'whirlwind': 1}
        self.abilities_s = ['dash', 'whirlwind']
        self.abilities_g = ['buckshot', 'rapid fire']
        self.todo = []
        self.arguments = []

        self.timer_sp = {'dash': 3, 'whirlwind': 2}     # Timer starting points
        self.timer = {'dash': 0, 'whirlwind': 0}
        self.cooldowns_sp = {'dash': 0}
        self.cooldowns = {'dash': 0, 'whirlwind': 0}


    def move_char(self, x, y):
        '''Use in abilities to move the character'''
        self.rect.centerx += x
        self.rect.centery += y
        current_level.shift_world(x, y)

    def if_ability(self, ability, name, arguments):
        '''Use to add ability to the a list of casting'''
        if ability == name:
            if self.cooldowns[name] == 0 and self.timer[name] == 0:
                    self.timer[name] = self.timer_sp[name]
                    self.todo.append(getattr(self.abilities, name))
                    self.arguments.append(arguments)




    def update(self):                           # TODO: Smoothen the walking mechanic and fix the speed if both buttons are pressed
        """
        Moves the character through time and makes all of his actions.
        """
        mouse_x = pygame.mouse.get_pos()[0] - self.rect.centerx
        mouse_y = pygame.mouse.get_pos()[1] - self.rect.centery
        mouse_angle_v = math.atan2(mouse_x, mouse_y)     # def the angle of orientation early.
        mouse_angle = math.atan2(mouse_y, mouse_x)       # the _v version serves for display purposes.
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.v_x = -self.speed
                if event.key == pygame.K_d:
                    self.v_x = self.speed
                if event.key == pygame.K_w:
                    self.v_y = -self.speed
                if event.key == pygame.K_s:
                    self.v_y = self.speed
                if event.key == pygame.K_q:
                    self.cycle += 1



            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.v_x = 0
                if event.key == pygame.K_d:
                    self.v_x = 0
                if event.key == pygame.K_w:
                    self.v_y = 0
                if event.key == pygame.K_s:
                    self.v_y = 0


            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == True:
                    if self.cycle % 2 == 0:
                        add_to_group(current_level, AnimationBox(current_level, 2, 'Stock/', self.rect.centerx, self.rect.centery,
                                                  self.sword_reach*4, self.sword_reach*4, mouse_angle_v))
                        for enemy in current_level.enemies:
                            x = enemy.rect.centerx - self.rect.centerx
                            y = enemy.rect.centery - self.rect.centery
                            enemy_distance = math.sqrt(x**2 + y**2)
                            print(enemy_distance)
                            if enemy_distance <= self.sword_reach:
                                enemy_angle = math.atan2(y, x)
                                print('Distance, YES')
                                mouse_angle = cycle_angle(mouse_angle)
                                enemy_angle = cycle_angle(enemy_angle)
                                print(enemy_angle, mouse_angle_v)
                                if mouse_angle - math.pi/2 < enemy_angle < mouse_angle + math.pi/2:
                                    enemy.health -= self.sword_damage
                                    print('ANGLE, YES')
                                    print(enemy.health)
                    if self.cycle % 2 == 1:                     # If gun is equipped, a projectile instance is created using
                        bullet = Projectile(self.rect.centerx,      # from the character class and mouse class.
                                            self.rect.centery, 20, 20,
                                            self.bullet_speed * math.cos(mouse_angle),
                                            self.bullet_speed * math.sin(mouse_angle),
                                            self.gun_damage)
                        add_to_group(current_level, bullet, current_level.player_projectiles)

                if event.dict['button'] == 4:
                    self.ability_selector -= 1
                elif event.dict['button'] == 5:
                    self.ability_selector += 1

                if pygame.mouse.get_pressed()[2] == True:       # Here we have the ability launching system.
                    if self.cycle % 2 == 0:
                        ability = self.abilities_s[self.ability_selector % len(self.abilities_s)]
                        self.if_ability(ability, 'dash', mouse_angle)
                        self.if_ability(ability, 'whirlwind', None)
                    if self.cycle % 1 == 0:
                        ability = self.abilities_g[self.ability_selector % len(self.abilities_s)]






                    if self.cycle % 2 == 1:
                        print(self.abilities_g[self.ability_selector % len(self.abilities_g)])



        todo = self.todo.copy()
        arguments = self.arguments.copy()
        for i in range(len(todo)):                  # Call the function with the arguments
            if todo[i](arguments[i]) == 'Done':     # The timer is checked in the Abilities.py
                print(todo[i])
                self.todo.pop(i)
                self.arguments.pop(i)



        for value in self.timer:                    # Timer decreases, ability is stopped casting when
            if self.timer[value] > 0:               # Timer goes to 0.
                self.timer[value] -= 1
                print(self.timer)



        self.image = self.originalImage
        self.image = rot_center(self.image, mouse_angle_v * 180/math.pi)


        self.rect.x += self.v_x
        self.rect.y += self.v_y
        self.shift_x += self.rect.x
        self.shift_y += self.rect.y


class User():
    def __init__(self, file):
        self.equipped = pickle.load(open("save.p", "rb"))


    def create_char(self):
        char = Character(400, 400, self.equipped[0], self.equipped[1])
        return char



class DamageBox(pygame.sprite.Sprite):
    def __init__(self, damage, x, y, size_x, size_y, timer, type = 'box'):
        super().__init__()
        self.damage = damage
        self.size = (size_x, size_y)
        self.type = type
        self.timer = timer
        if type == 'box':
            self.image = pygame.Surface((size_x, size_y))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
    def update(self):
        if self.timer == 0:
            allies = current_level.allies
            collision = pygame.sprite.spritecollide(self, allies, False)
            for ally in collision:
                ally.health -= self.damage
                print(ally.health)

            self.kill()
        self.timer -=1
        alpha = 255 - self.timer
        self.image.set_alpha(alpha)
        print(self.timer)



        self.timer -= 1


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, v_x, v_y, damage, frames = 0):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.image_count = 0
        self.v_x = v_x

        self.v_y = v_y
        self.distance_travelled = 0
        self.frames = frames
        self.damage = damage

    def update(self):
        self.rect.x += self.v_x
        self.rect.y += self.v_y
        self.distance_travelled += math.sqrt(self.v_x ** 2 + self.v_y ** 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.win = False
        self.health = 100
        self.hit = False
        self.image = pygame.image.load('char.jpg')
        self.image = self.image.convert()
        self.originalImage = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.v_x = 0
        self.v_y = 0
        self.speed = 3

    def update(self):
        projectiles = current_level.player_projectiles
        projectile_collision = pygame.sprite.spritecollide(self, projectiles, True)
        enemies = current_level.enemies
        enemy_collision = pygame.sprite.spritecollide(self, enemies, False)


        if len(projectile_collision) > 0:
            for projectile in projectile_collision:
                self.health -= projectile.damage
                print(self.health)
        if self.health <= 0:
            remove_from_group(current_level, self, current_level.enemies)

        self.move_crawler(current_level.local_character)

    def move_crawler(self, player):
        angle = cycle_angle(angle_between(self, player))
        self.v_x = self.speed * math.cos(angle)
        self.v_y = self.speed * math.sin(angle)
        self.rect.x += self.v_x
        self.rect.y += self.v_y
        self.image = self.originalImage
        self.image = rot_center(self.image, 90 - angle * 180/math.pi)





class Level(object):
    def __init__(self, local_character, other_characters = []):
        # Create all of the groups that are concerned on the level
        self.object_list = pygame.sprite.Group()    # stores everything in the level
        self.hit_markers = pygame.sprite.Group()    # stores red hit markers signifying where abilities will land
        self.enemies = pygame.sprite.Group()    # stores all enemies
        self.allies = pygame.sprite.Group()     # stores other players
        self.player_projectiles = pygame.sprite.Group()     # stores player projectiles
        self.enemy_projectiles = pygame.sprite.Group()
        self.local_character = local_character      # stores the character of the client
        self.other_characters = []
        for character in self.other_characters:
            self.allies.add(character)
        self.allies.add(local_character)
        self.object_list.add(self.local_character)
        self.world_shift_x = 0
        self.world_shift_y = 0


    def update(self):
        self.object_list.update()
        self.shift_world(self.local_character.v_x, self.local_character.v_y)
        for event in pygame.event.get():
            print(event)

    def draw(self, window):
        window.fill((0,0,0))
        self.object_list.draw(window)

    def shift_world(self, shift_x, shift_y):        # function used to shift all objects around the character.
        self.world_shift_x += shift_x
        self.world_shift_y += shift_y
        for each_object in self.object_list:
            each_object.rect.x -= shift_x
            each_object.rect.y -= shift_y
        self.local_character.rect.x = window_width/2
        self.local_character.rect.y = window_height/2


class Level_01(Level):
    def __init__(self, local_character, other_characters = []):
        super().__init__(local_character)
        for i in range(1):
            enemy = Enemy(random.randint(100, 600), random.randint(100, 600))
            d_box = DamageBox(20, 300, 300, 300, 300, 300)
            self.add_to_group(d_box)
            self.add_to_group(enemy, self.enemies)

    def add_to_group(self, item, group=None):
        self.object_list.add(item)
        if group is not None:
            group.add(item)




if __name__ == "__main__":
    pygame.init()

    window_size = window_width, window_height = 1366, 768
    window = pygame.display.set_mode(window_size)

    pygame.display.set_caption('HACKSLASH')

    clock = pygame.time.Clock()
    frames_per_second = 60

    local_User = User("save.p")
    local_character = local_User.create_char()
    current_level = Level_01(local_character)
    local_character.level = current_level
    local_character.abilities = PlayerAbilities(local_character)

    gameActive = True

    while gameActive:

        # Update functions
        event = None
        current_level.update()
        # Logic testing

        # Draw everything
        current_level.draw(window)

        clock.tick(frames_per_second)
        pygame.display.update()
