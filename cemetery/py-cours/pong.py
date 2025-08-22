import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Vitesse de rafraîchissement
clock = pygame.time.Clock()

# Dimensions des éléments
ball_size = 20
paddle_width, paddle_height = 10, 100

# Position initiale de la balle
ball_x = width // 2 - ball_size // 2
ball_y = height // 2 - ball_size // 2
ball_dx = 5  # Direction horizontale
ball_dy = 5  # Direction verticale

# Position initiale des raquettes
paddle1_x, paddle1_y = 50, height // 2 - paddle_height // 2  # Joueur
paddle2_x, paddle2_y = width - 50 - paddle_width, height // 2 - paddle_height // 2  # IA
paddle_speed = 10

# Vitesse de l'IA
ia_speed = 5

# Boucle de jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Déplacement de la raquette du joueur
    keys = pygame.key.get_pressed()
    if keys[pygame.K_z] and paddle1_y > 0:
        paddle1_y -= paddle_speed
    if keys[pygame.K_s] and paddle1_y < height - paddle_height:
        paddle1_y += paddle_speed

    # Déplacement de la raquette de l'IA
    if paddle2_y + paddle_height // 2 < ball_y:
        paddle2_y += ia_speed
    if paddle2_y + paddle_height // 2 > ball_y:
        paddle2_y -= ia_speed

    # Empêcher l'IA de sortir de l'écran
    if paddle2_y < 0:
        paddle2_y = 0
    if paddle2_y > height - paddle_height:
        paddle2_y = height - paddle_height

    # Déplacement de la balle
    ball_x += ball_dx
    ball_y += ball_dy

    # Collision avec les murs supérieurs et inférieurs
    if ball_y <= 0 or ball_y >= height - ball_size:
        ball_dy *= -1

    # Collision avec les raquettes
    if (paddle1_x < ball_x < paddle1_x + paddle_width and paddle1_y < ball_y < paddle1_y + paddle_height) or \
       (paddle2_x < ball_x + ball_size < paddle2_x + paddle_width and paddle2_y < ball_y < paddle2_y + paddle_height):
        ball_dx *= -1

    # Balle sort du terrain (reset)
    if ball_x <= 0 or ball_x >= width - ball_size:
        ball_x = width // 2 - ball_size // 2
        ball_y = height // 2 - ball_size // 2
        ball_dx *= -1

    # Affichage
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (paddle1_x, paddle1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, WHITE, (paddle2_x, paddle2_y, paddle_width, paddle_height))
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, ball_size, ball_size))
    pygame.draw.aaline(screen, WHITE, (width // 2, 0), (width // 2, height))

    # Mettre à jour l'écran
    pygame.display.flip()

    # Limiter la vitesse de rafraîchissement
    clock.tick(60)

# Quitter Pygame
pygame.quit()
sys.exit()
