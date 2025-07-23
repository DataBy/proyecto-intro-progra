import pygame
import sys
import subprocess

# --- Global Config ---
WIDTH, HEIGHT = 1280, 720
FPS = 60

# --- Init PyGame ---
def init():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Drone Task Manager")
    return screen

# --- Load Resources ---
def load_assets():
    background = pygame.image.load("assets/background_menu.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    play = pygame.image.load("assets/play.png")
    play_hover = pygame.image.load("assets/play_hover.png")
    options = pygame.image.load("assets/options.png")
    options_hover = pygame.image.load("assets/options_hover.png")
    exit_btn = pygame.image.load("assets/exit.png")
    exit_hover = pygame.image.load("assets/exit_hover.png")

    return {
        "background": background,
        "play": play,
        "play_hover": play_hover,
        "options": options,
        "options_hover": options_hover,
        "exit": exit_btn,
        "exit_hover": exit_hover
    }

# --- Main Menu ---
def main_menu(screen, assets):
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_rect.collidepoint(mouse_pos):
                    # Ejecutar scenary01.py como una nueva ventana
                    subprocess.Popen(["python", "scenary01.py"])
                    return  # Cierra el menú para no duplicar ventanas

        # Background draw
        screen.blit(assets["background"], (0, 0))

        # Hover de btn
        mouse_pos = pygame.mouse.get_pos()


        # Button positions
        PLAY_BTN_POS = (705, 185)
        OPTIONS_BTN_POS = (705, 315)
        EXIT_BTN_POS = (705, 442)

        # Play
        play_rect = assets["play"].get_rect(topleft=PLAY_BTN_POS)
        if play_rect.collidepoint(mouse_pos):
            screen.blit(assets["play_hover"], PLAY_BTN_POS)
        else:
            screen.blit(assets["play"], PLAY_BTN_POS)

        # Options
        options_rect = assets["options"].get_rect(topleft=OPTIONS_BTN_POS)
        if options_rect.collidepoint(mouse_pos):
            screen.blit(assets["options_hover"], OPTIONS_BTN_POS)
        else:
            screen.blit(assets["options"], OPTIONS_BTN_POS)

        # Exit
        exit_rect = assets["exit"].get_rect(topleft=EXIT_BTN_POS)
        if exit_rect.collidepoint(mouse_pos):
            screen.blit(assets["exit_hover"], EXIT_BTN_POS)
        else:
            screen.blit(assets["exit"], EXIT_BTN_POS)

        pygame.display.flip()
        clock.tick(FPS)

# --- Inputs ---
def main():
    screen = init()
    assets = load_assets()
    main_menu(screen, assets)


main()
