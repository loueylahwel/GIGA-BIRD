import pygame
import sys
import random
from Bird import Bird
from Pipe import Pipe
from Population import Population

# Initialize Game
pygame.init()

# Game State
game_state = 1
score = 0
generation = 0

# Window Setup
window_w = 400
window_h = 600
screen = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("GIGA BIRD")
clock = pygame.time.Clock()
fps = 60

# Load Fonts
try:
    font = pygame.font.Font("GIGA BIRD/fonts/BaiJamjuree-Bold.ttf", 60)
    small_font = pygame.font.Font("GIGA BIRD/fonts/BaiJamjuree-Bold.ttf", 20)
except:
    font = pygame.font.SysFont("Arial", 30)
    small_font = pygame.font.SysFont("Arial", 30)

# Load Sounds
try:
    slap_sfx = pygame.mixer.Sound("GIGA BIRD/sounds/slap.wav")
    score_sfx = pygame.mixer.Sound("GIGA BIRD/sounds/score.wav")
except:
    slap_sfx = score_sfx = None

player_img = pygame.image.load("GIGA BIRD/images/player.png").convert_alpha()
pipe_up_img = pygame.image.load("GIGA BIRD/images/pipe_up.png").convert_alpha()
pipe_down_img = pygame.image.load("GIGA BIRD/images/pipe_down.png").convert_alpha()
ground_img = pygame.image.load("GIGA BIRD/images/ground.png").convert_alpha()
bg_img = pygame.image.load("GIGA BIRD/images/background.png").convert()
bg_width = bg_img.get_width()
ground_height = 64  

POPULATION_SIZE = 150 

def scoreboard():
    # Display current score
    show_score = font.render(str(score), True, (255, 0, 0))
    score_rect = show_score.get_rect(center=(window_w // 2, 64))
    screen.blit(show_score, score_rect)


def display_stats(gen, alive_count, best_fitness, best_score, avg_fitness):
    # Display generation stats
    gen_text = small_font.render(f"Gen: {gen}", True, (255, 0, 0))
    alive_text = small_font.render(f"Alive: {alive_count}", True, (255, 0, 0))
    best_text = small_font.render(f"Best fitness: {int(best_fitness)}", True, (255, 0, 0))
    score_text = small_font.render(f"Highest score: {best_score}", True, (255, 0, 0))
    
    screen.blit(gen_text, (10, 10))
    screen.blit(alive_text, (10, 30))
    screen.blit(best_text, (10, 50))
    screen.blit(score_text, (10, 70))


def game():
    global game_state, score, generation

    # Initial setup
    bg_x_pos = 0
    ground_x_pos = 0
    best_score = 0
    
    # Create population
    population = Population(POPULATION_SIZE)
    birds = [Bird(168, 300, genome, player_img, window_h, window_w) 
             for genome in population.genomes]
    
    pipes = [Pipe(600, random.randint(30, 250), 220, 2.4)]

    while game_state != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = 0

        # Count alive birds
        alive_birds = [b for b in birds if b.alive]
        
        # If no birds, evolve new generation
        if not alive_birds:
            population.evaluate_fitness(birds)
            population.evolve()
            generation += 1
            
            # Reset game
            birds = [Bird(168, 300, genome, player_img, window_h, window_w) 
                    for genome in population.genomes]
            pipes = [Pipe(600, random.randint(30, 250), 220, 2.4)]
            score = 0
            bg_x_pos = 0
            ground_x_pos = 0

        # GIGA birds think and act
        for bird in alive_birds:
            bird.think(pipes)
            bird.update(ground_height)
            
            # Check collision with pipes
            bird_rect = pygame.Rect(bird.x, bird.y, player_img.get_width(), player_img.get_height())
            
            for pipe in pipes:
                # Pipe hitboxes
                top_rect = pygame.Rect(pipe.x, 0, pipe_up_img.get_width(), pipe.height)
                bottom_rect = pygame.Rect(pipe.x, pipe.height + pipe.gap, pipe_up_img.get_width(), window_h)
                
                if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                    bird.alive = False
                    break

        # Update pipes
        for pipe in pipes:
            pipe.update()

        # Remove off-screen pipes
        if pipes and pipes[0].x < -pipe_up_img.get_width():
            pipes.pop(0)
        
        # Add new pipe
        if not pipes or pipes[-1].x < 250:
            pipes.append(Pipe(600, random.randint(30, 280), 220, 2.4))

        # Score logic
        if alive_birds:
            for pipe in pipes:
                if not pipe.scored and pipe.x + pipe_up_img.get_width() < alive_birds[0].x:
                    score += 1
                    if score > best_score:
                        best_score = score
                    if score_sfx:
                        score_sfx.play()
                    pipe.scored = True
                    
                    # Bonus fitness for passing pipe
                    for bird in alive_birds:
                        bird.fitness += 100 

        # Scroll background
        bg_x_pos -= 1
        if bg_x_pos <= -bg_width:
            bg_x_pos = 0

        ground_x_pos -= 2
        if ground_x_pos <= -bg_width:
            ground_x_pos = 0

        # Draw background, ground
        screen.blit(bg_img, (bg_x_pos, 0))
        screen.blit(bg_img, (bg_x_pos + bg_width, 0))
        screen.blit(ground_img, (ground_x_pos, 536))
        screen.blit(ground_img, (ground_x_pos + bg_width, 536))

        # Draw pipes
        for pipe in pipes:
            pipe.draw(screen, pipe_down_img, pipe_up_img)

        # Draw birds
        for bird in alive_birds:
            screen.blit(player_img, (bird.x, bird.y))

        # Draw UI
        scoreboard()
        best_fitness = max(bird.fitness for bird in birds) if birds else 0
        avg_fitness = sum(bird.fitness for bird in birds) / len(birds) if birds else 0
        display_stats(generation, len(alive_birds), best_fitness, best_score, avg_fitness)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()


# Start game
if __name__ == "__main__":
    game()