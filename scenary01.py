import pygame
import sys
import random
from npc_indio import Indio
from npc_tucan import Ave
from sistema_vidas import VidaManager, VidaFlotante
from game_over_screen import mostrar_pantalla_gameover
from lluvia import TormentaTropical
from disparo import HuevoDisparo, manejar_colisiones_huevo
from meta import MetaFinal
from pantalla_gano import mostrar_pantalla_gano
from arbol import arbol_cayendo


def jugar_escenario(screen):
    WIDTH, HEIGHT = 1280, 720
    FPS = 60
    DRONE_SPEED = 5
    ZOOM_FACTOR = 1.1

    # --- Meta ---
    meta = MetaFinal(600, 100)  # Puedes cambiar manualmente X y Y


    clock = pygame.time.Clock()

    vida_manager = VidaManager()
    vidas_flotantes = pygame.sprite.Group(
        VidaFlotante(200, 2500),
        VidaFlotante(400, 1500),
        VidaFlotante(700, 600)
    )

    background = pygame.image.load("assets/background01/background_clean.png").convert()
    background = pygame.transform.scale(background, (WIDTH, 2880))
    BACKGROUND_HEIGHT = background.get_height()

    sprite_0 = pygame.image.load("assets/drone_3cajas/sprite_0.png").convert_alpha()
    sprite_1 = pygame.image.load("assets/drone_3cajas/sprite_1.png").convert_alpha()
    drone_sprites = [sprite_0, sprite_1]

    drone_index = 0
    drone_timer = 0
    drone_width = sprite_0.get_width()
    drone_height = sprite_0.get_height()
    drone_x = WIDTH // 2 - drone_width // 2
    drone_y = BACKGROUND_HEIGHT - HEIGHT // 2 - drone_height // 2
    drone_rect = pygame.Rect(drone_x, drone_y, drone_width, drone_height)

    class DronSprite(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = None
            self.rect = None
            self.mask = None

    dron_ref_global = DronSprite()

    indios = pygame.sprite.Group()
    flechas = pygame.sprite.Group()
    aves = pygame.sprite.Group()
    grupo_animaciones_ave = pygame.sprite.Group()
    proyectiles_ave = pygame.sprite.Group()
    grupo_colisiones = pygame.sprite.Group()

    indios_creados = False
    aves_creadas = False
    INDIO_START_DELAY = 5
    AVE_START_DELAY = 5

    INDIO_POSICIONES = [
        (random.randint(100, 1000), 2600),
        (random.randint(100, 1000), 1600),
        (random.randint(100, 1000), 1400),
        (random.randint(100, 1000), 600),
        (random.randint(100, 1000), 200),
    ]

    AVE_POSICIONES = [
        pygame.Rect(random.randint(100, 1000), 2200, 120, 100),
        pygame.Rect(random.randint(100, 1000), 1800, 120, 100),
        pygame.Rect(random.randint(100, 1000), 1000, 120, 100),
    ]

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
    
    grupo_arboles = pygame.sprite.Group()
    ARBOLES_POS = [
        (220, 295)
    ]
    
    for pos in ARBOLES_POS:
        arbol = arbol_cayendo(pos[0], pos[1], dron_ref_global)
        grupo_arboles.add(arbol)


    for filename, pos in elementos_info:
        img = pygame.image.load(f"assets/background01/{filename}").convert_alpha()
        mask = pygame.mask.from_surface(img)
        elementos_fisicos.append({"img": img, "pos": pos, "mask": mask})
        sprite = pygame.sprite.Sprite()
        sprite.image = img
        sprite.rect = img.get_rect(topleft=pos)
        grupo_colisiones.add(sprite)

    tormenta = TormentaTropical()
    tormenta_delay_inicial = 5
    inicio_escenario = pygame.time.get_ticks()

    disparos = pygame.sprite.Group()

    objetivo_actual = None
    mostrar_mira = False
    mira_img = pygame.Surface((10, 10), pygame.SRCALPHA)
    pygame.draw.circle(mira_img, (255, 0, 0), (5, 5), 5)

    while True:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if objetivo_actual:
                        huevo = HuevoDisparo(drone_rect.centerx, drone_rect.top, objetivo_actual.rect.center)
                    else:
                        huevo = HuevoDisparo(drone_rect.centerx, drone_rect.top)
                    disparos.add(huevo)

        screen.fill((255, 255, 255))

        keys = pygame.key.get_pressed()
        is_moving = False
        speed_multiplier = 3 if keys[pygame.K_LSHIFT] else 1
        actual_speed = DRONE_SPEED * speed_multiplier

        if keys[pygame.K_UP]: drone_y -= actual_speed; is_moving = True
        if keys[pygame.K_DOWN]: drone_y += actual_speed; is_moving = True
        if keys[pygame.K_LEFT]: drone_x -= actual_speed; is_moving = True
        if keys[pygame.K_RIGHT]: drone_x += actual_speed; is_moving = True

        drone_y = max(0, min(BACKGROUND_HEIGHT - drone_height, drone_y))
        margin_x = int(drone_width * (ZOOM_FACTOR - 1) / 2)
        drone_x = max(-margin_x, min(WIDTH - drone_width + margin_x, drone_x))

        drone_rect.x = drone_x
        drone_rect.y = drone_y

        scroll_y = drone_y + drone_height // 2 - HEIGHT // 2
        scroll_y = max(0, min(scroll_y, BACKGROUND_HEIGHT - HEIGHT))

        drone_timer += 1
        if drone_timer >= 10:
            drone_index = (drone_index + 1) % 2
            drone_timer = 0

        current_sprite = drone_sprites[drone_index]
        dron_ref_global.rect = drone_rect.copy()
        dron_ref_global.image = current_sprite
        dron_ref_global.mask = pygame.mask.from_surface(current_sprite)
        dron_ref_global.vida_manager = vida_manager

        mostrar_mira = keys[pygame.K_LALT] or keys[pygame.K_RALT]
        objetivo_actual = None
        if mostrar_mira:
            min_dist = float("inf")
            for npc in list(indios) + list(aves):
                dx = npc.rect.centerx - drone_rect.centerx
                dy = npc.rect.centery - drone_rect.centery
                dist = dx * dx + dy * dy
                if dist < min_dist:
                    min_dist = dist
                    objetivo_actual = npc

        screen.blit(background, (0, -scroll_y))

        if is_moving:
            zoomed_sprite = pygame.transform.scale(
                current_sprite,
                (int(current_sprite.get_width() * ZOOM_FACTOR), int(current_sprite.get_height() * ZOOM_FACTOR))
            )
            rect = zoomed_sprite.get_rect(center=(drone_x + drone_width // 2, drone_y - scroll_y + drone_height // 2))
            screen.blit(zoomed_sprite, rect.topleft)
        else:
            screen.blit(current_sprite, (drone_x, drone_y - scroll_y))

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
        
        for arbol in grupo_arboles:
            arbol.chequear_activacion(drone_rect.center)
            arbol.update()
            screen.blit(arbol.image, (arbol.rect.x, arbol.rect.y - scroll_y))


        for elem in elementos_fisicos:
            elem_x, elem_y = elem["pos"]
            screen.blit(elem["img"], (elem_x, elem_y - scroll_y))

        for vida in vidas_flotantes:
            recogida = vida.update(dron_ref_global)
            if recogida:
                vida_manager.ganar_vida()
            screen.blit(vida.image, (vida.rect.x, vida.rect.y - scroll_y))

        vida_manager.dibujar(screen)

        if not indios_creados and pygame.time.get_ticks() >= INDIO_START_DELAY * 1000:
            for pos in INDIO_POSICIONES:
                indio = Indio(pos[0], pos[1], dron_ref_global, flechas, grupo_colisiones)
                indios.add(indio)
            indios_creados = True

        indios.update(dron_ref_global)
        for indio in indios:
            screen.blit(indio.image, (indio.rect.x, indio.rect.y - scroll_y))

        flechas.update(dron_ref_global)
        for flecha in flechas:
            screen.blit(flecha.image, (flecha.rect.x, flecha.rect.y - scroll_y))

        if not aves_creadas and pygame.time.get_ticks() >= AVE_START_DELAY * 1000:
            for pos in AVE_POSICIONES:
                ave = Ave(pos, dron_ref_global, grupo_animaciones_ave, proyectiles_ave, grupo_colisiones)
                aves.add(ave)
            aves_creadas = True

        for ave in aves:
            ave.update(dron_ref_global)
            screen.blit(ave.image, (ave.rect.x, ave.rect.y - scroll_y))

        proyectiles_ave.update(dron_ref_global)
        for proyectil in proyectiles_ave:
            screen.blit(proyectil.image, (proyectil.rect.x, proyectil.rect.y - scroll_y))

        grupo_animaciones_ave.update()
        for anim in grupo_animaciones_ave:
            screen.blit(anim.image, (anim.rect.x, anim.rect.y - scroll_y))

        tiempo_actual = pygame.time.get_ticks() / 1000
        puede_iniciar = (
            not tormenta.activa and
            tiempo_actual > tormenta_delay_inicial and
            tiempo_actual - tormenta.ultimo_fin > 5
        )
        if puede_iniciar and random.random() < 0.01:
            tormenta.activar()
        tormenta.update(screen, scroll_y)

        disparos.update()
        manejar_colisiones_huevo(disparos, indios, aves, grupo_arboles)
        for disparo in disparos:
            screen.blit(disparo.image, (disparo.rect.x, disparo.rect.y - scroll_y))

        if mostrar_mira and objetivo_actual:
            mira_x = objetivo_actual.rect.centerx
            mira_y = objetivo_actual.rect.centery
            screen.blit(mira_img, (mira_x - 5, mira_y - scroll_y))

        if vida_manager.esta_muerto():
            resultado = mostrar_pantalla_gameover(screen)
            return resultado
        

        # --- Meta ---
        meta.update()
        meta.draw(screen, scroll_y)

        if meta.check_colision(dron_ref_global.rect):
            resultado = mostrar_pantalla_gano(screen)
            if resultado == "menu":
                return

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    print("Este archivo no debe ejecutarse directamente. Usa main.py para iniciar el juego.")
