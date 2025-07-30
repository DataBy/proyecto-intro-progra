import pygame
import sys
import main_menu
from instrucciones import mostrar_instrucciones  
from scenary01 import jugar_escenario
import musica 


def main():
    pygame.init()
    musica.reproducir_musica()  # ✅ Inicia música de fondo
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Héroes del Hambre")

    while True:
        accion = main_menu.mostrar_menu(screen)
        if accion == "play":
            mostrar_instrucciones(screen)  # ✅ Primero mostramos instrucciones
            resultado = jugar_escenario(screen)
            if resultado == "menu":
                continue
            elif resultado == "exit":
                break
        elif accion == "exit":
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
