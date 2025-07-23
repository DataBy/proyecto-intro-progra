import pygame
import sys

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
background = pygame.image.load("assets/background01/background.png").convert()
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
drone_y = BACKGROUND_HEIGHT - HEIGHT // 2 - drone_height // 2  # Centrado en la parte baja

# --- Loop principal ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- Movimiento del drone ---
    keys = pygame.key.get_pressed()
    is_moving = False
    if keys[pygame.K_UP]:
        drone_y -= DRONE_SPEED
        is_moving = True
    if keys[pygame.K_DOWN]:
        drone_y += DRONE_SPEED
        is_moving = True
    if keys[pygame.K_LEFT]:
        drone_x -= DRONE_SPEED
        is_moving = True
    if keys[pygame.K_RIGHT]:
        drone_x += DRONE_SPEED
        is_moving = True

    # --- Límite del drone dentro del fondo ---
    drone_y = max(0, min(BACKGROUND_HEIGHT - drone_height, drone_y))
    # Asumimos zoom puede crecer hasta un 10%, por eso usamos un margen
    margin_x = int(drone_width * (ZOOM_FACTOR - 1) / 2)
    margin_y = int(drone_height * (ZOOM_FACTOR - 1) / 2)

    drone_x = max(-margin_x, min(WIDTH - drone_width + margin_x, drone_x))

    # --- Scroll: que el fondo siga al drone ---
    scroll_y = drone_y + drone_height // 2 - HEIGHT // 2
    scroll_y = max(0, min(scroll_y, BACKGROUND_HEIGHT - HEIGHT))

    # --- Animación del sprite ---
    drone_timer += 1
    if drone_timer >= 10:
        drone_index = (drone_index + 1) % 2
        drone_timer = 0

    # --- Dibujar fondo ---
    screen.blit(background, (0, -scroll_y))

    # --- Dibujar drone con hover/zoom si se mueve ---
    current_sprite = drone_sprites[drone_index]
    if is_moving:
        zoomed_sprite = pygame.transform.scale(
            current_sprite,
            (int(current_sprite.get_width() * ZOOM_FACTOR), int(current_sprite.get_height() * ZOOM_FACTOR))
        )
        rect = zoomed_sprite.get_rect(center=(drone_x + drone_width // 2, drone_y - scroll_y + drone_height // 2))
        screen.blit(zoomed_sprite, rect.topleft)
    else:
        screen.blit(current_sprite, (drone_x, drone_y - scroll_y))

    pygame.display.flip()
    clock.tick(FPS)
