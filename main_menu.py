import pygame
import sys

# --- Global Config ---
WIDTH, HEIGHT = 1280, 720
FPS = 60

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
def mostrar_menu(screen):
    clock = pygame.time.Clock()
    assets = load_assets()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        screen.blit(assets["background"], (0, 0))

        # Button positions
        PLAY_BTN_POS = (705, 185)
        OPTIONS_BTN_POS = (705, 315)
        EXIT_BTN_POS = (705, 442)

        # Play
        play_rect = assets["play"].get_rect(topleft=PLAY_BTN_POS)
        if play_rect.collidepoint(mouse_pos):
            screen.blit(assets["play_hover"], PLAY_BTN_POS)
            if click:
                return "play"
        else:
            screen.blit(assets["play"], PLAY_BTN_POS)

        # Options (no funcional aún)
        options_rect = assets["options"].get_rect(topleft=OPTIONS_BTN_POS)
        if options_rect.collidepoint(mouse_pos):
            screen.blit(assets["options_hover"], OPTIONS_BTN_POS)
        else:
            screen.blit(assets["options"], OPTIONS_BTN_POS)

        # Exit
        exit_rect = assets["exit"].get_rect(topleft=EXIT_BTN_POS)
        if exit_rect.collidepoint(mouse_pos):
            screen.blit(assets["exit_hover"], EXIT_BTN_POS)
            if click:
                return "exit"
        else:
            screen.blit(assets["exit"], EXIT_BTN_POS)

        pygame.display.flip()
        clock.tick(FPS)

# Solo para pruebas individuales
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Main Menu")
    resultado = mostrar_menu(screen)
    print("Resultado:", resultado)
