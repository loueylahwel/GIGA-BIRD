import pygame

class Pipe:    
    def __init__(self, x, height, gap, velocity):
        self.x = x
        self.height = height
        self.gap = gap
        self.velocity = velocity
        self.scored = False

    def update(self):
        """Move pipe to the left"""
        self.x -= self.velocity

    def draw(self, screen, pipe_down_img, pipe_up_img, ui_width=0):
        """Draw both top and bottom pipes"""
        # Top pipe 
        screen.blit(pipe_down_img, 
                   (self.x + ui_width, self.height - pipe_down_img.get_height()))
        # Bottom pipe
        screen.blit(pipe_up_img, 
                   (self.x + ui_width, self.height + self.gap))

    def is_off_screen(self, pipe_width):
        """Check if pipe has moved off screen"""
        return self.x < -pipe_width

    def is_passed(self, bird_x):
        """Check if bird has passed this pipe"""
        return self.x + 52 < bird_x 
