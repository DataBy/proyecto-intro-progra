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
drone_y = BACKGROUND_HEIGHT - HEIGHT // 2 - drone_height // 2  # Centrado en la parte baja

# --- Loop principal ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- Movimiento del drone con boost ---
    keys = pygame.key.get_pressed()
    is_moving = False

    # Detectar si está presionado shift izquierdo
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


    # --- Lista de elementos físicos (imagen, posición, máscara) ---
    elementos_fisicos = []

    # --- Cargar element01.png ---
    img_01 = pygame.image.load("assets/background01/element01.png").convert_alpha()
    pos_01 = (-100, 2200)  # (x, y) en coordenadas del fondo — puedes ajustarlo
    mask_01 = pygame.mask.from_surface(img_01)
    elementos_fisicos.append({"img": img_01, "pos": pos_01, "mask": mask_01})

    # --- Cargar element02.png ---
    img_02 = pygame.image.load("assets/background01/element02.png").convert_alpha()
    pos_02 = (-100, 1810)   # (x, y) en coordenadas del fondo
    mask_02 = pygame.mask.from_surface(img_02)
    elementos_fisicos.append({"img": img_02, "pos": pos_02, "mask": mask_02})

    # --- Cargar element03.png ---
    img_03 = pygame.image.load("assets/background01/element03.png").convert_alpha()
    pos_03 = (360, 1740)  # (x, y) en coordenadas del fondo
    mask_03 = pygame.mask.from_surface(img_03)
    elementos_fisicos.append({"img": img_03, "pos": pos_03, "mask": mask_03})

    # --- Cargar element04.png ---
    img_04 = pygame.image.load("assets/background01/element04.png").convert_alpha()
    pos_04 = (-90, 1480)  # (x, y) en coordenadas del fondo
    mask_04 = pygame.mask.from_surface(img_04)
    elementos_fisicos.append({"img": img_04, "pos": pos_04, "mask": mask_04})

    # --- Cargar element06.png ---
    img_06 = pygame.image.load("assets/background01/element06.png").convert_alpha()
    pos_06 = (-100, 900)  # (x, y) en coordenadas del fondo
    mask_06 = pygame.mask.from_surface(img_06)
    elementos_fisicos.append({"img": img_06, "pos": pos_06, "mask": mask_06})

    # --- Cargar element05.png ---
    img_05 = pygame.image.load("assets/background01/element05.png").convert_alpha()
    pos_05 = (580, 1150)  # (x, y) en coordenadas del fondo
    mask_05 = pygame.mask.from_surface(img_05)
    elementos_fisicos.append({"img": img_05, "pos": pos_05, "mask": mask_05})

    # --- Cargar element07.png ---
    img_07 = pygame.image.load("assets/background01/element07.png").convert_alpha()
    pos_07 = (350, 400 )  # (x, y) en coordenadas del fondo
    mask_07 = pygame.mask.from_surface(img_07)
    elementos_fisicos.append({"img": img_07, "pos": pos_07, "mask": mask_07})

    # --- Cargar element08.png ---
    img_08 = pygame.image.load("assets/background01/element08.png").convert_alpha()
    pos_08 = (-250, 290 )  # (x, y) en coordenadas del fondo
    mask_08 = pygame.mask.from_surface(img_08)
    elementos_fisicos.append({"img": img_08, "pos": pos_08, "mask": mask_08})

    # --- Cargar element09.png ---
    img_09 = pygame.image.load("assets/background01/element09.png").convert_alpha()
    pos_09 = (-20, 10 )  # (x, y) en coordenadas del fondo
    mask_09 = pygame.mask.from_surface(img_09)
    elementos_fisicos.append({"img": img_09, "pos": pos_09, "mask": mask_09})

    

    # --- Crear máscara del drone ---
    drone_surface = drone_sprites[drone_index]
    drone_mask = pygame.mask.from_surface(drone_surface)

    # --- Revisar colisión con cada elemento físico ---
    for elem in elementos_fisicos:
        elem_x, elem_y = elem["pos"]
        offset_x = elem_x - drone_x
        offset_y = elem_y - drone_y

        if drone_mask.overlap(elem["mask"], (offset_x, offset_y)):
            retroceso = int(DRONE_SPEED * 2.5)
            if keys[pygame.K_UP]:
                drone_y += retroceso
            if keys[pygame.K_DOWN]:
                drone_y -= retroceso
            if keys[pygame.K_LEFT]:
                drone_x += retroceso
            if keys[pygame.K_RIGHT]:
                drone_x -= retroceso
    

    # --- Dibujar todos los objetos físicos con scroll ---
    for elem in elementos_fisicos:
        elem_x, elem_y = elem["pos"]
        screen.blit(elem["img"], (elem_x, elem_y - scroll_y))







    pygame.display.flip()
    clock.tick(FPS)
