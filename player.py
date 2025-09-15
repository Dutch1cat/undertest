import pygame
import time

# To get access to constants from another file
from constants import WIDTH, HEIGHT

class Player:
    def __init__(self, x, y):
        # The player's world position (absolute coordinates in the entire game world)
        self.world_x = x
        self.world_y = y
        # The player's screen position (will be fixed at the center of the screen)
        self.screen_x = WIDTH // 2
        self.screen_y = HEIGHT // 2
        self.rect = pygame.Rect(self.screen_x, self.screen_y, 48, 64) # Player size
        self.speed = 5
        self.animations = {}
        self.current_animation = "idle_down"
        self.frame_index = 0
        self.animation_speed = 0.15 # Time in seconds per frame
        self.last_frame_time = time.time()
        self.load_animations()
        
    def load_animations(self):
        # Corrected idle animation frame counts from 1 to 2 to prevent the IndexError.
        anim_data = {
            "idle_down": 1, "idle_left": 2, "idle_right": 2, "idle_up": 1,
            "walk_down": 4, "walk_left": 2, "walk_right": 2, "walk_up": 4
        }
        for anim_name, frame_count in anim_data.items():
            frames = []
            for i in range(frame_count):
                path = f"images/player/{anim_name}/frame_{i}.png"
                img = pygame.image.load(path).convert_alpha()
                # Using a consistent size for all sprites
                frames.append(pygame.transform.scale(img, (24*2, 32*2)))
            self.animations[anim_name] = frames
            
    def get_frame(self):
        """Returns the current animation frame to be drawn."""
        return self.animations[self.current_animation][self.frame_index]

    def update_animation(self, moving, direction):
        """Handles the animation logic based on player's movement and direction."""
        new_animation = f"walk_{direction}" if moving else f"idle_{direction}"
        
        # If the animation has changed, reset the frame index
        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.frame_index = 0

        # Update frame index for animation
        if time.time() - self.last_frame_time > self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_animation])
            self.last_frame_time = time.time()
