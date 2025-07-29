import pygame
import random
import math

class proyectil_ave(pygame.sprite.Sprite):
    def __init__(self, x, y, target_pos):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/bola/sprite_0.png").convert_alpha(), (10, 10)
            )

        self.rect = self.image.get_rect(center=(x, y))

        dx = target_pos[0] - x
        dy = target_pos[1] - y
        angle = math.atan2(dy, dx)
        speed = 7

        self.vel_x = math.cos(angle) * speed
        self.vel_y = math.sin(angle) * speed
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, drone_ref):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if pygame.sprite.collide_mask(self, drone_ref):
            self.kill()

        if not pygame.Rect(0, 0, 1280, 2880).colliderect(self.rect):
            self.kill()

        if pygame.sprite.collide_mask(self, drone_ref):
            self.kill()
            if hasattr(drone_ref, "vida_manager"):
                drone_ref.vida_manager.perder_vida()


class Animacion_disparo_ave(pygame.sprite.Sprite):
    def __init__(self, x, y, target_pos, all_projectiles):
        super().__init__()
        self.frames = [
            pygame.transform.scale(pygame.image.load(f"assets/bola/sprite_{i}.png").convert_alpha(), (32, 32))
            for i in range(5)
            ]

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.frame_index = 0
        self.frame_timer = 0
        self.target_pos = target_pos
        self.all_projectiles = all_projectiles

    def update(self):
        self.frame_timer += 1
        if self.frame_timer >= 5:
            self.frame_index += 1
            if self.frame_index < len(self.frames):
                self.image = self.frames[self.frame_index]
                self.frame_timer = 0
            else:
                proyectil = proyectil_ave(self.rect.centerx, self.rect.centery, self.target_pos)
                self.all_projectiles.add(proyectil)
                self.kill()


class Ave(pygame.sprite.Sprite):
    def __init__(self, area_rect, drone_ref, animation_group, all_projectiles, collidable_surfaces):
        super().__init__()
        self.frames = [
            pygame.transform.scale(pygame.image.load(f"assets/ave/sprite_{i}.png").convert_alpha(), (45, 45))
            for i in range(2)
            ]


        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=area_rect.center)



        self.area_rect = area_rect
        self.drone_ref = drone_ref
        self.projectiles = all_projectiles
        self.collidable_surfaces = collidable_surfaces
        self.animaciones_group = animation_group


        self.target_pos = self.random_point_in_area()
        self.speed = 2
        self.shoot_cooldown = 0
        self.animation_timer = 0
        self.frame_index = 0

    def random_point_in_area(self):
        return (
            random.randint(self.area_rect.left, self.area_rect.right),
            random.randint(self.area_rect.top, self.area_rect.bottom)
        )

    def update(self, drone_ref=None):
        if drone_ref:
            self.drone_ref = drone_ref

        self.animate()
        self.move()
        self.atacar_en_cercania()

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.animation_timer = 0

    def move(self):
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance < 5:
            self.target_pos = self.random_point_in_area()
        else:
            self.rect.x += int((dx / distance) * self.speed)
            self.rect.y += int((dy / distance) * self.speed)
    
    def draw(self, surface, scroll_y=0):
        surface.blit(self.image, (self.rect.x, self.rect.y - scroll_y))


    def atacar_en_cercania(self):
        self.shoot_cooldown += 1
        drone_dx = self.drone_ref.rect.centerx - self.rect.centerx
        drone_dy = self.drone_ref.rect.centery - self.rect.centery
        distance = math.hypot(drone_dx, drone_dy)

        if self.shoot_cooldown > 60 and distance < 400:
            if not any(
                isinstance(obj, Animacion_disparo_ave) and obj.rect.center == self.rect.center
                for obj in self.animaciones_group
                    ):
                        animacion = Animacion_disparo_ave(
                            self.rect.centerx, self.rect.centery,
                            self.drone_ref.rect.center,
                            self.projectiles
                    )
                        self.animaciones_group.add(animacion)


