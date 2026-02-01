import pygame


class Bird:    
    def __init__(self, x, y, genome, bird_img, window_h, game_width):
        self.x = x
        self.y = y
        self.velocity = 0
        self.genome = genome
        self.fitness = 0
        self.alive = True
        self.bird_img = bird_img
        self.window_h = window_h
        self.game_width = game_width

    def think(self, pipes):
        if not self.alive or not pipes:
            return
        
        # Find the next pipe
        target_pipe = None
        for pipe in pipes:
            # Check if pipe is ahead of bird
            if pipe.x + 52 > self.x:
                target_pipe = pipe
                break

        if not target_pipe:
            target_pipe = pipes[-1]
        
        # Normalize inputs for neural network
        inputs = [
            self.y / self.window_h,  # Bird Y 
            (target_pipe.x - self.x) / self.game_width,  # Distance to pipe
            target_pipe.height / self.window_h,  # Top pipe  Y
            (target_pipe.height + target_pipe.gap) / self.window_h,  # Bottom Pipe Y
            (self.velocity + 10) / 20  # Bird velocity 
        ]
        
        # Get decision from neural network
        output = self.genome.feed_forward(inputs)
        
        # Jump if output > 0.5
        if output > 0.5:
            self.jump()

    def jump(self):
        if self.alive:
            self.velocity = -10

    def update(self, ground_height):
        if not self.alive:
            return
        
        # Apply gravity
        self.velocity += 0.75
        self.y += self.velocity
        
        # Increase fitness while alive
        self.fitness += 1
        
        # Check if bird out of bounds
        if self.y > 536 or self.y < -64:
            self.alive = False

    def draw(self, screen, ui_width=0):
        if self.alive:
            screen.blit(self.bird_img, (self.x + ui_width, self.y))

    def get_status(self):
        return self.alive