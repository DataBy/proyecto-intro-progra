import pygame
import random
import math

# --- Configuraciones iniciales ---
INDIO_START_DELAY = 5  # segundos
INDIO_ATTACK_INTERVAL = 1.0  # segundos entre ataques
INDIO_SPEED = 3.5
INDIO_COUNT = 5
INDIO_MIN_DIST = 180     # distancia mínima al dron
INDIO_REPEL_DIST = 80    # distancia mínima entre indios

INDIO_CORRER_PATH = "assets/indio/indio_corre/"
INDIO_LANZA_PATH = "assets/indio/indio_flecha/"
FLECHA_PATH = "assets/indio/flecha.png"

# --- Clase Flecha ---
class Flecha(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.original_image = pygame.image.load(FLECHA_PATH).convert_alpha()

        # 75% de probabilidades de fallar
        if random.random() > 0.25:
            angle += random.uniform(-35, 35)

        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=(x, y))

        speed = 12
        rad = math.radians(angle)
        self.vel_x = math.cos(rad) * speed
        self.vel_y = -math.sin(rad) * speed

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()

    def collides_with(self, target_rect):
        return self.rect.colliderect(target_rect)

# --- Clase Indio ---
class Indio(pygame.sprite.Sprite):
    def __init__(self, pos, drone_reference, colisiones):
        super().__init__()
        self.drone = drone_reference
        self.colisiones = colisiones

        self.running_frames = [pygame.image.load(f"{INDIO_CORRER_PATH}{i}.png").convert_alpha() for i in range(1, 9)]
        self.attack_frames = [pygame.image.load(f"{INDIO_LANZA_PATH}{i}.png").convert_alpha() for i in range(1, 5)]

        self.image = self.running_frames[0]
        self.rect = self.image.get_rect(topleft=pos)

        self.animation_timer = 0
        self.animation_index = 0
        self.attack_timer = 0
        self.state = "running"

        self.flechas = pygame.sprite.Group()
        self.free_roaming_time = 2  # segundos sin colisiones al inicio
        self.total_time = 0

    def update(self, dt, otros_indios):
        self.dt = dt
        self.total_time += dt
        self.flechas.update()

        if self.state == "running":
            self.move_towards_drone(otros_indios)
            self.animate_running()
        elif self.state == "attacking":
            self.animate_attack()

    def move_towards_drone(self, otros_indios):
        # Repulsión entre indios
        for otro in otros_indios:
            if otro is not self:
                dx = self.rect.centerx - otro.rect.centerx
                dy = self.rect.centery - otro.rect.centery
                distance = math.hypot(dx, dy)
                if distance < INDIO_REPEL_DIST and distance > 0:
                    repel_strength = (INDIO_REPEL_DIST - distance) / INDIO_REPEL_DIST
                    self.rect.x += int((dx / distance) * repel_strength * 2)
                    self.rect.y += int((dy / distance) * repel_strength * 2)

        # Movimiento hacia el dron
        dx = self.drone.rect.centerx - self.rect.centerx
        dy = self.drone.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance > INDIO_MIN_DIST:
            angle = math.atan2(dy, dx)
            old_x, old_y = self.rect.x, self.rect.y
            self.rect.x += int(math.cos(angle) * INDIO_SPEED)
            self.rect.y += int(math.sin(angle) * INDIO_SPEED)

            # Colisiones con obstáculos después del roaming
            if self.total_time > self.free_roaming_time:
                for obj in self.colisiones:
                    offset_x = obj["pos"][0] - self.rect.x
                    offset_y = obj["pos"][1] - self.rect.y
                    indio_mask = pygame.mask.from_surface(self.image)
                    if indio_mask.overlap(obj["mask"], (offset_x, offset_y)):
                        self.rect.x, self.rect.y = old_x, old_y
                        break

        # Control de ataque
        self.attack_timer += self.dt
        if self.attack_timer >= INDIO_ATTACK_INTERVAL:
            self.attack_timer = 0
            self.state = "attacking"
            self.animation_index = 0

    def animate_running(self):
        self.animation_timer += 1
        if self.animation_timer >= 4:
            self.animation_timer = 0
            self.animation_index = (self.animation_index + 1) % len(self.running_frames)
            self.image = self.running_frames[self.animation_index]

    def animate_attack(self):
        if self.animation_index < len(self.attack_frames):
            self.image = self.attack_frames[self.animation_index]
            self.animation_index += 1
        else:
            self.lanzar_flecha()
            self.state = "running"
            self.animation_index = 0

    def lanzar_flecha(self):
        dx = self.drone.rect.centerx - self.rect.centerx
        dy = self.drone.rect.centery - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))
        flecha = Flecha(self.rect.centerx, self.rect.centery, angle)
        self.flechas.add(flecha)

    def draw(self, screen, scroll_y):
        screen.blit(self.image, (self.rect.x, self.rect.y - scroll_y))
        for flecha in self.flechas:
            screen.blit(flecha.image, (flecha.rect.x, flecha.rect.y - scroll_y))

    def check_flecha_collision(self, drone_rect):
        for flecha in self.flechas:
            if flecha.collides_with(drone_rect):
                flecha.kill()
                return True
        return False
