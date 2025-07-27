import pygame
import sys
import random
from npc_indio import Indio

# --- Configuración ---
WIDTH, HEIGHT = 1280, 720
FPS = 60
DRONE_SPEED = 5
ZOOM_FACTOR = 1.1

# --- Inicialización ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escenario 01")
clock = pygame.time.Clock()

# --- Cargar fondo largo ---
background = pygame.image.load("assets/background01/background_clean.png").convert()
background = pygame.transform.scale(background, (WIDTH, 2880))
BACKGROUND_HEIGHT = background.get_height()

# --- Cargar sprites del drone ---
sprite_0 = pygame.image.load("assets/drone_3cajas/sprite_0.png").convert_alpha()
sprite_1 = pygame.image.load("assets/drone_3cajas/sprite_1.png").convert_alpha()
drone_sprites = [sprite_0, sprite_1]

# --- Variables del drone ---
drone_index = 0
drone_timer = 0
drone_width = sprite_0.get_width()
drone_height = sprite_0.get_height()
drone_x = WIDTH // 2 - drone_width // 2
drone_y = BACKGROUND_HEIGHT - HEIGHT // 2 - drone_height // 2
drone_rect = pygame.Rect(drone_x, drone_y, drone_width, drone_height)

# --- Referencia viva para NPC y flechas ---
class DronSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = None
        self.rect = None
        self.mask = None

dron_ref_global = DronSprite()

# --- Inicializar grupos ---
indios = pygame.sprite.Group()
flechas = pygame.sprite.Group()
grupo_colisiones = pygame.sprite.Group()

indios_creados = False
INDIO_START_DELAY = 5  # segundos

INDIO_POSICIONES = [
    (random.randint(100, 1000), 2600),
    (random.randint(100, 1000), 1600),
    (random.randint(100, 1000), 1400),
    (random.randint(100, 1000), 600),
    (random.randint(100, 1000), 200),
]

# --- Elementos físicos del fondo ---
elementos_fisicos = []
elementos_info = [
    ("element01.png", (-100, 2200)),
    ("element02.png", (-100, 1810)),
    ("element03.png", (360, 1740)),
    ("element04.png", (-90, 1480)),
    ("element06.png", (-100, 900)),
    ("element05.png", (580, 1150)),
    ("element07.png", (350, 400)),
    ("element08.png", (-250, 290)),
    ("element09.png", (-20, 10)),
]

for filename, pos in elementos_info:
    img = pygame.image.load(f"assets/background01/{filename}").convert_alpha()
    mask = pygame.mask.from_surface(img)

    # Guardar para colisiones con el dron
    elementos_fisicos.append({"img": img, "pos": pos, "mask": mask})

    # Agregar colisionables para NPCs
    sprite = pygame.sprite.Sprite()
    sprite.image = img
    sprite.rect = img.get_rect(topleft=pos)
    grupo_colisiones.add(sprite)

# --- Loop principal ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255))

    # --- Movimiento del dron ---
    keys = pygame.key.get_pressed()
    is_moving = False
    speed_multiplier = 3 if keys[pygame.K_LSHIFT] else 1
    actual_speed = DRONE_SPEED * speed_multiplier

    if keys[pygame.K_UP]:
        drone_y -= actual_speed
        is_moving = True
    if keys[pygame.K_DOWN]:
        drone_y += actual_speed
        is_moving = True
    if keys[pygame.K_LEFT]:
        drone_x -= actual_speed
        is_moving = True
    if keys[pygame.K_RIGHT]:
        drone_x += actual_speed
        is_moving = True

    drone_y = max(0, min(BACKGROUND_HEIGHT - drone_height, drone_y))
    margin_x = int(drone_width * (ZOOM_FACTOR - 1) / 2)
    drone_x = max(-margin_x, min(WIDTH - drone_width + margin_x, drone_x))

    drone_rect.x = drone_x
    drone_rect.y = drone_y

    # --- Scroll de cámara ---
    scroll_y = drone_y + drone_height // 2 - HEIGHT // 2
    scroll_y = max(0, min(scroll_y, BACKGROUND_HEIGHT - HEIGHT))

    # --- Animación del dron ---
    drone_timer += 1
    if drone_timer >= 10:
        drone_index = (drone_index + 1) % 2
        drone_timer = 0

    current_sprite = drone_sprites[drone_index]

    # --- Actualizar referencia viva del dron ---
    dron_ref_global.rect = drone_rect.copy()
    dron_ref_global.image = current_sprite
    dron_ref_global.mask = pygame.mask.from_surface(current_sprite)

    screen.blit(background, (0, -scroll_y))

    # --- Dibujar dron ---
    if is_moving:
        zoomed_sprite = pygame.transform.scale(
            current_sprite,
            (int(current_sprite.get_width() * ZOOM_FACTOR), int(current_sprite.get_height() * ZOOM_FACTOR))
        )
        rect = zoomed_sprite.get_rect(center=(drone_x + drone_width // 2, drone_y - scroll_y + drone_height // 2))
        screen.blit(zoomed_sprite, rect.topleft)
    else:
        screen.blit(current_sprite, (drone_x, drone_y - scroll_y))

    # --- Colisiones físicas del dron ---
    drone_mask = pygame.mask.from_surface(current_sprite)
    for elem in elementos_fisicos:
        elem_x, elem_y = elem["pos"]
        offset_x = elem_x - drone_x
        offset_y = elem_y - drone_y
        if drone_mask.overlap(elem["mask"], (offset_x, offset_y)):
            retroceso = int(DRONE_SPEED * 3.5)
            if keys[pygame.K_UP]: drone_y += retroceso
            if keys[pygame.K_DOWN]: drone_y -= retroceso
            if keys[pygame.K_LEFT]: drone_x += retroceso
            if keys[pygame.K_RIGHT]: drone_x -= retroceso

    # --- Dibujar elementos físicos ---
    for elem in elementos_fisicos:
        elem_x, elem_y = elem["pos"]
        screen.blit(elem["img"], (elem_x, elem_y - scroll_y))

    # --- Crear indios después del delay ---
    if not indios_creados and pygame.time.get_ticks() >= INDIO_START_DELAY * 1000:
        for pos in INDIO_POSICIONES:
            indio = Indio(pos[0], pos[1], dron_ref_global, flechas, grupo_colisiones)
            indios.add(indio)
        indios_creados = True

    # --- Actualizar y dibujar indios ---
    indios.update(dron_ref_global)
    for indio in indios:
        screen.blit(indio.image, (indio.rect.x, indio.rect.y - scroll_y))

    # --- Actualizar y dibujar flechas ---
    flechas.update(dron_ref_global)
    for flecha in flechas:
        screen.blit(flecha.image, (flecha.rect.x, flecha.rect.y - scroll_y))

    pygame.display.flip()
    clock.tick(FPS)
