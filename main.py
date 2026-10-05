import pygame
import random
import sys

pygame.init()

# Configuration de la fenêtre
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Ball")
clock = pygame.time.Clock()

# Couleurs
WHITE = (255, 255, 255)
DARK_BG = (20, 24, 33)
ACCENT_BLUE = (0, 162, 255)
GREEN = (0, 255, 157)
RED = (255, 75, 75)
GRAY = (150, 150, 150)

# Polices
font_large = pygame.font.SysFont("Arial", 46, bold=True)
font_medium = pygame.font.SysFont("Arial", 28, bold=True)
font_small = pygame.font.SysFont("Arial", 20)

# Variables du jeu
paddle_w, paddle_h = 100, 15
paddle_speed = 8
ball_r = 12

def reset_game():
    return {
        "paddle_x": (WIDTH - paddle_w) // 2,
        "paddle_y": HEIGHT - 40,
        "ball_x": random.randint(ball_r, WIDTH - ball_r),
        "ball_y": 0,
        "ball_speed": 5,
        "score": 0,
        "game_over": False
    }

game = reset_game()
high_score = 0

# Boucle principale
running = True
while running:
    screen.fill(DARK_BG)
    
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game["game_over"]:
                game = reset_game()

    if not game["game_over"]:
        # Déplacement de la raquette
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and game["paddle_x"] > 0:
            game["paddle_x"] -= paddle_speed
        if keys[pygame.K_RIGHT] and game["paddle_x"] < WIDTH - paddle_w:
            game["paddle_x"] += paddle_speed

        # Déplacement de la balle
        game["ball_y"] += game["ball_speed"]

        # Collisions avec la raquette
        paddle_rect = pygame.Rect(game["paddle_x"], game["paddle_y"], paddle_w, paddle_h)
        ball_rect = pygame.Rect(game["ball_x"] - ball_r, game["ball_y"] - ball_r, ball_r * 2, ball_r * 2)

        if ball_rect.colliderect(paddle_rect):
            game["score"] += 1
            game["ball_y"] = 0
            game["ball_x"] = random.randint(ball_r, WIDTH - ball_r)
            game["ball_speed"] += 0.3  # Augmente la difficulté

        # Balle ratée = Game Over
        if game["ball_y"] > HEIGHT:
            game["game_over"] = True
            if game["score"] > high_score:
                high_score = game["score"]

        # Dessin du jeu actif
        pygame.draw.rect(screen, ACCENT_BLUE, (game["paddle_x"], game["paddle_y"], paddle_w, paddle_h), border_radius=6)
        pygame.draw.circle(screen, GREEN, (game["ball_x"], game["ball_y"]), ball_r)
        
        # Score en direct
        score_txt = font_medium.render(f"Score: {game['score']}", True, WHITE)
        screen.blit(score_txt, (20, 20))

    else:
        # Écran de Game Over
        go_txt = font_large.render("GAME OVER", True, RED)
        final_score_txt = font_medium.render(f"Score final: {game['score']}", True, WHITE)
        best_score_txt = font_medium.render(f"Meilleur score: {high_score}", True, GREEN)
        replay_txt = font_small.render("Appuie sur ESPACE pour rejouer", True, GRAY)

        screen.blit(go_txt, (WIDTH // 2 - go_txt.get_width() // 2, 180))
        screen.blit(final_score_txt, (WIDTH // 2 - final_score_txt.get_width() // 2, 260))
        screen.blit(best_score_txt, (WIDTH // 2 - best_score_txt.get_width() // 2, 300))
        screen.blit(replay_txt, (WIDTH // 2 - replay_txt.get_width() // 2, 380))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()