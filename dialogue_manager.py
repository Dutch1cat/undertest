import pygame
import time

# To get access to constants from another file
from constants import WIDTH, HEIGHT, BLACK, WHITE, LIGHT_GRAY

class DialogueManager:
    def __init__(self, font_size=24, text_color=WHITE, box_color=BLACK, border_color=WHITE):
        self.font = pygame.font.SysFont(None, font_size)
        self.text_color = text_color
        self.box_color = box_color
        self.border_color = border_color
        self.dialogue_box = pygame.Rect(50, HEIGHT - 150, WIDTH - 100, 100)
        self.talking_sound = pygame.mixer.Sound("songs/talking.wav")
        self.current_text = ""
        self.full_text = ""
        self.text_speed = 0.05
        self.last_update_time = 0
        self.is_choice_mode = False
        self.options = []
        self.selected_option_index = 0
        self.choice_made = None

    def start_dialogue(self, text):
        """Starts a standard text dialogue."""
        self.full_text = text
        self.current_text = ""
        self.last_update_time = time.time()
        self.is_choice_mode = False
        self.choice_made = None

    def start_choice_dialogue(self, text, options):
        """Starts a dialogue with choices."""
        self.full_text = text
        self.current_text = ""
        self.last_update_time = time.time()
        self.is_choice_mode = True
        self.options = options
        self.selected_option_index = 0
        self.choice_made = None
        
    def update(self):
        """Updates the dialogue text (typewriter effect)."""
        if self.current_text != self.full_text:
            if time.time() - self.last_update_time > self.text_speed:
                if len(self.current_text) < len(self.full_text):
                    self.current_text += self.full_text[len(self.current_text)]
                    try:
                        if self.full_text[len(self.current_text)] != " " and self.full_text[len(self.current_text)] != "*":
                            self.talking_sound.play()
                    except:
                        pass
                    self.last_update_time = time.time()
                return False
        return True

    def handle_input(self, event):
        """Handles input for choice selection using mouse clicks."""
        if self.is_choice_mode and self.current_text == self.full_text:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                button_width = 120
                button_height = 40
                button_spacing = 20
                
                for i, option in enumerate(self.options):
                    x = WIDTH // 2 - (len(self.options) * (button_width + button_spacing) - button_spacing) // 2 + i * (button_width + button_spacing)
                    y = self.dialogue_box.y + self.dialogue_box.height + 20
                    button_rect = pygame.Rect(x, y, button_width, button_height)
                    
                    if button_rect.collidepoint(mouse_pos):
                        self.choice_made = option
                        return True
        return False

    def skip(self):
        """Skips the typewriter effect to show the full text instantly."""
        self.current_text = self.full_text
    
    def draw(self, screen):
        """Draws the dialogue box and text."""
        pygame.draw.rect(screen, self.box_color, self.dialogue_box)
        pygame.draw.rect(screen, self.border_color, self.dialogue_box, 2)
        
        # Render the dialogue text
        text_surface = self.font.render(self.current_text, True, self.text_color)
        screen.blit(text_surface, (self.dialogue_box.x + 10, self.dialogue_box.y + 10))

        # If in choice mode and text is fully displayed, render the options
        if self.is_choice_mode and self.current_text == self.full_text:
            button_width = 120
            button_height = 40
            button_spacing = 20
            
            for i, option in enumerate(self.options):
                x = WIDTH // 2 - (len(self.options) * (button_width + button_spacing) - button_spacing) // 2 + i * (button_width + button_spacing)
                y = self.dialogue_box.y + self.dialogue_box.height + 20
                
                button_rect = pygame.Rect(x, y, button_width, button_height)
                
                color = LIGHT_GRAY if i == self.selected_option_index else WHITE
                pygame.draw.rect(screen, color, button_rect, 2)
                
                text_surface = self.font.render(option, True, WHITE)
                text_rect = text_surface.get_rect(center=button_rect.center)
                screen.blit(text_surface, text_rect)