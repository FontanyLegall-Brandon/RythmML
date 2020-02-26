import pygame


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode()
    while True:
        events = pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                print(event.key)