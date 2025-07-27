import pygame
import random
import math

class Flecha(pygame.sprite.Sprite):
    def __init__(self, x, y, target_pos, accuracy=0.1):
        super().__init__()
        original_image = pygame.image.load("assets/indio/flecha.png").convert_alpha()
        self.rect = original_image.get_rect(center=(x, y))

        if random.random() > accuracy:
            target_pos = (
                target_pos[0] + random.randint(-200, 200),
                target_pos[1] + random.randint(-200, 200)
            )

        dx = target_pos[0] - x
        dy = target_pos[1] - y
        angle = math.degrees(math.atan2(-dy, dx))
        distance = math.hypot(dx, dy) or 1

        self.vel_x = (dx / distance) * 10
        self.vel_y = (dy / distance) * 10
        self.image = pygame.transform.rotate(original_image, angle)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, drone_ref):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if pygame.sprite.collide_mask(self, drone_ref):
            self.kill()

        if not pygame.Rect(0, 0, 1280, 2880).colliderect(self.rect):
            self.kill()


class Indio(pygame.sprite.Sprite):
    def __init__(self, x, y, drone_ref, all_arrows_group, collidable_surfaces):
        super().__init__()
        self.load_assets()

        self.rect = self.image.get_rect(
            center=(x + random.randint(-300, 300),
                    y + random.randint(-150, 150))
        )

        self.speed = random.uniform(1.5, 2.5)
        self.drone_ref = drone_ref
        self.arrow_group = all_arrows_group
        self.collidable_surfaces = collidable_surfaces

        self.min_distance = random.randint(150, 250)
        self.arrow_timer = random.randint(0, 60)
        self.spawn_time = pygame.time.get_ticks()

        self.frame_index = 0
        self.animation_timer = 0

    def load_assets(self):
        self.frames = [
            pygame.image.load(f"assets/indio/indio_flecha/{i}.png").convert_alpha()
            for i in range(1, 5)
        ]
        self.image = self.frames[0]

    def update(self, drone_ref=None):
        if drone_ref:
            self.drone_ref = drone_ref

        self.handle_animation()
        self.handle_movement()
        self.handle_attacking()
        self.handle_collisions()

    def handle_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.animation_timer = 0

    def handle_movement(self):
        dx = self.drone_ref.rect.centerx - self.rect.centerx
        dy = self.drone_ref.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance == 0:
            return  # Evita división por 0

        # Zona muerta ampliada para evitar vibraciones
        if distance > self.min_distance + 20:
            norm_dx = dx / distance
            norm_dy = dy / distance
            self.rect.x += norm_dx * self.speed
            self.rect.y += norm_dy * self.speed

        elif distance < self.min_distance - 20:
            norm_dx = dx / distance
            norm_dy = dy / distance
            self.rect.x -= norm_dx * self.speed
            self.rect.y -= norm_dy * self.speed

    def handle_attacking(self):
        self.arrow_timer += 1
        distance_to_drone = math.hypot(
            self.drone_ref.rect.centerx - self.rect.centerx,
            self.drone_ref.rect.centery - self.rect.centery
        )

        if self.arrow_timer >= 60 and distance_to_drone < 500:
            self.shoot_arrow()
            self.arrow_timer = 0

    def shoot_arrow(self):
        flecha = Flecha(
            self.rect.centerx,
            self.rect.centery,
            self.drone_ref.rect.center,
            accuracy=0.1
        )
        self.arrow_group.add(flecha)

    def handle_collisions(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_time < 1000:
            return  # 1 segundo de libertad al nacer

        for surface in self.collidable_surfaces:
            if self.rect.colliderect(surface.rect):
                # Rebote: retroceso realista
                dx = self.drone_ref.rect.centerx - self.rect.centerx
                dy = self.drone_ref.rect.centery - self.rect.centery
                distance = math.hypot(dx, dy) or 1

                self.rect.x -= (dx / distance) * self.speed * 2
                self.rect.y -= (dy / distance) * self.speed * 2

                # Límite dentro de pantalla
                self.rect.clamp_ip(pygame.Rect(0, 0, 1280, 2880))
