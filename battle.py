# Modulo per la logica di battaglia e gli schemi di attacco
import pygame
import random
import time
import math
from dialogue_manager import DialogueManager

# To get access to constants from another file
from constants import BOX, WIDTH, HEIGHT

# === Attack Pattern Functions ===

# Easy Patterns
def pattern_wave(time_elapsed, player_rect, projectiles, image):
    if len(projectiles) < 10:
        for _ in range(5):
            x = random.randint(BOX.left, BOX.right - image.get_width())
            rect = pygame.Rect(x, BOX.top - 20, image.get_width(), image.get_height())
            projectiles.append({'rect': rect})
    hit = False
    for p in projectiles:
        p['rect'].y += 4
        if p['rect'].colliderect(player_rect):
            hit = True
    projectiles[:] = [p for p in projectiles if p['rect'].y < BOX.bottom + 20]
    return hit

def pattern_straight_line(time_elapsed, player_rect, projectiles, image):
    # A simple attack where projectiles move horizontally across the box
    if not projectiles:
        for i in range(5):
            y = BOX.top + (i * 50)
            rect = pygame.Rect(BOX.left - 20, y, image.get_width(), image.get_height())
            projectiles.append({'rect': rect})
    hit = False
    for p in projectiles:
        p['rect'].x += 3
        if p['rect'].colliderect(player_rect):
            hit = True
    projectiles[:] = [p for p in projectiles if p['rect'].x < BOX.right + 20]
    return hit

def pattern_top_to_bottom(time_elapsed, player_rect, projectiles, image):
    # Projectiles drop from the top of the box in columns.
    if len(projectiles) < 15 and random.random() < 0.1:
        x = random.choice([BOX.left + 50, BOX.left + 150, BOX.left + 250])
        rect = pygame.Rect(x, BOX.top - 20, image.get_width(), image.get_height())
        projectiles.append({'rect': rect, 'speed': 3})

    hit = False
    for p in projectiles:
        p['rect'].y += p['speed']
        if p['rect'].colliderect(player_rect):
            hit = True
    projectiles[:] = [p for p in projectiles if p['rect'].y < BOX.bottom + 20]
    return hit

def pattern_left_to_right(time_elapsed, player_rect, projectiles, image):
    # Projectiles shoot from the left in rows.
    if len(projectiles) < 15 and random.random() < 0.1:
        y = random.choice([BOX.top + 50, BOX.top + 150, BOX.top + 250])
        rect = pygame.Rect(BOX.left - 20, y, image.get_width(), image.get_height())
        projectiles.append({'rect': rect, 'speed': 3})
    
    hit = False
    for p in projectiles:
        p['rect'].x += p['speed']
        if p['rect'].colliderect(player_rect):
            hit = True
    projectiles[:] = [p for p in projectiles if p['rect'].x < BOX.right + 20]
    return hit

def pattern_center_out(time_elapsed, player_rect, projectiles, image):
    # Projectiles spawn at the center and move outwards in four directions.
    if not projectiles:
        spawn_vectors = [(3, 0), (-3, 0), (0, 3), (0, -3)]
        for dx, dy in spawn_vectors:
            rect = pygame.Rect(BOX.centerx, BOX.centery, image.get_width(), image.get_height())
            projectiles.append({'rect': rect, 'dx': dx, 'dy': dy})
            
    hit = False
    for p in projectiles:
        p['rect'].x += p['dx']
        p['rect'].y += p['dy']
        if p['rect'].colliderect(player_rect):
            hit = True
    projectiles[:] = [p for p in projectiles if BOX.colliderect(p['rect'])]
    return hit

def pattern_random_spawn(time_elapsed, player_rect, projectiles, image):
    # Projectiles spawn at random spots and move slowly in a random direction.
    if len(projectiles) < 20 and random.random() < 0.08:
        x = random.randint(BOX.left, BOX.right)
        y = random.randint(BOX.top, BOX.bottom)
        dx = random.uniform(-2, 2)
        dy = random.uniform(-2, 2)
        rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        projectiles.append({'rect': rect, 'dx': dx, 'dy': dy})
        
    hit = False
    for p in projectiles:
        p['rect'].x += p['dx']
        p['rect'].y += p['dy']
        if p['rect'].colliderect(player_rect):
            hit = True
    projectiles[:] = [p for p in projectiles if BOX.colliderect(p['rect'])]
    return hit

def pattern_random_walk(time_elapsed, player_rect, projectiles, image):
    # Projectiles spawn at the top and 'walk' down with random horizontal movement.
    if len(projectiles) < 10 and random.random() < 0.2:
        x = random.randint(BOX.left, BOX.right)
        rect = pygame.Rect(x, BOX.top - 20, image.get_width(), image.get_height())
        projectiles.append({'rect': rect, 'dy': 2, 'dx': random.uniform(-1, 1)})
        
    hit = False
    for p in projectiles:
        p['rect'].x += p['dx']
        p['rect'].y += p['dy']
        if p['rect'].colliderect(player_rect):
            hit = True
    projectiles[:] = [p for p in projectiles if p['rect'].y < BOX.bottom + 20]
    return hit

# Medium Patterns
def pattern_spike(time_elapsed, player_rect, projectiles, image):
    if len(projectiles) < 20:
        for _ in range(1):
            side = random.choice(["left", "right", "top", "bottom"])
            if side == "left":
                x, y, dx, dy = BOX.left - 20, random.randint(BOX.top, BOX.bottom), 4, 0
            elif side == "right":
                x, y, dx, dy = BOX.right + 20, random.randint(BOX.top, BOX.bottom), -4, 0
            elif side == "top":
                x, y, dx, dy = random.randint(BOX.left, BOX.right), BOX.top - 20, 0, 4
            else:
                x, y, dx, dy = random.randint(BOX.left, BOX.right), BOX.bottom + 20, 0, -4
            rect = pygame.Rect(x, y, image.get_width(), image.get_height())
            projectiles.append({'rect': rect, 'dx': dx, 'dy': dy})
    hit = False
    for p in projectiles:
        p['rect'].x += p['dx']
        p['rect'].y += p['dy']
        if p['rect'].colliderect(player_rect):
            hit = True
    projectiles[:] = [p for p in projectiles if BOX.left - 40 < p['rect'].x < BOX.right + 40 and BOX.top - 40 < p['rect'].y < BOX.bottom + 40]
    return hit

def pattern_diagonal_cross(time_elapsed, player_rect, projectiles, image):
    # Projectiles shoot from corners towards the center
    if not projectiles:
        spawn_points = [
            (BOX.left - 20, BOX.top - 20, 3, 3), # Top-left to bottom-right
            (BOX.right + 20, BOX.top - 20, -3, 3), # Top-right to bottom-left
            (BOX.left - 20, BOX.bottom + 20, 3, -3), # Bottom-left to top-right
            (BOX.right + 20, BOX.bottom + 20, -3, -3) # Bottom-right to top-left
        ]
        for x, y, dx, dy in spawn_points:
            rect = pygame.Rect(x, y, image.get_width(), image.get_height())
            projectiles.append({'rect': rect, 'dx': dx, 'dy': dy})
    hit = False
    for p in projectiles:
        p['rect'].x += p['dx']
        p['rect'].y += p['dy']
        if p['rect'].colliderect(player_rect):
            hit = True
    projectiles[:] = [p for p in projectiles if BOX.left - 40 < p['rect'].x < BOX.right + 40 and BOX.top - 40 < p['rect'].y < BOX.bottom + 40]
    return hit

def pattern_circle_spiral(time_elapsed, player_rect, projectiles, image):
    # Projectiles spiral outwards from the center of the box
    if len(projectiles) < 50 and random.random() < 0.2:
        angle = random.randint(0, 360)
        rad = math.radians(angle)
        rect = pygame.Rect(BOX.centerx, BOX.centery, image.get_width(), image.get_height())
        projectiles.append({'rect': rect, 'angle': angle, 'speed': 2, 'dx': 2 * math.cos(rad), 'dy': 2 * math.sin(rad)})
    
    hit = False
    for p in projectiles:
        p['rect'].x += p['dx']
        p['rect'].y += p['dy']
        if p['rect'].colliderect(player_rect):
            hit = True
    projectiles[:] = [p for p in projectiles if BOX.colliderect(p['rect'])]
    return hit

# Hard Pattern
def pattern_chase(time_elapsed, player_rect, projectiles, image):
    # Projectiles spawn at random points and chase the player
    if len(projectiles) < 5 and random.random() < 0.05:
        x = random.randint(BOX.left, BOX.right)
        y = random.randint(BOX.top, BOX.bottom)
        rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        projectiles.append({'rect': rect, 'speed': 2})
    
    hit = False
    for p in projectiles:
        # Calculate direction towards the player
        dx = player_rect.centerx - p['rect'].centerx
        dy = player_rect.centery - p['rect'].centery
        distance = math.sqrt(dx**2 + dy**2)
        
        # Normalize the vector and update projectile position
        if distance > 0:
            p['rect'].x += p['speed'] * (dx / distance)
            p['rect'].y += p['speed'] * (dy / distance)

        if p['rect'].colliderect(player_rect):
            hit = True
    
    return hit


# === Classes ===
class Attack:
    def __init__(self, name, image_path, pattern_func):
        self.name = name
        self.image_path = image_path
        self.pattern_func = pattern_func
        self.image = None
        self.projectiles = []

    def load(self):
        self.image = pygame.transform.scale(pygame.image.load(self.image_path).convert_alpha(), (20, 20))

    def update(self, time_elapsed, player_rect):
        return self.pattern_func(time_elapsed, player_rect, self.projectiles, self.image)

    def draw(self, screen):
        for obj in self.projectiles:
            if isinstance(obj, dict) and 'rect' in obj:
                screen.blit(self.image, obj['rect'])
            elif isinstance(obj, pygame.Rect):
                screen.blit(self.image, obj)

class BossBattle:
    def __init__(self, boss_name, boss_img_path, heart_img_path, attacks, boss_hp, player_stats, 
                 exp_reward=10, max_happiness=20, spare_phrase=None, boss_leafy=False, dialogue_manager=None):
        self.boss_name = boss_name
        self.boss_img_path = boss_img_path
        self.heart_img_path = heart_img_path
        self.attacks = attacks
        self.boss_img = None
        self.heart_img = None
        self.heart_rect = None
        self.boss_hp = boss_hp
        self.boss_max_hp = boss_hp
        self.player_stats = player_stats  # Reference to player stats
        self.exp_reward = exp_reward
        self.phase = "attack"
        self.selected_attack = None
        self.is_leafy_boss = boss_leafy
        # Create a new dialogue manager if none provided
        self.dialogue_manager = dialogue_manager if dialogue_manager else DialogueManager()
        self.final_dialogue_started = False
        self.max_happiness = max_happiness
        self.spare_phrase = spare_phrase
        self.happiness = 0
        self.battle_won = False
        self.battle_spared = False
        self.level_up_message = None

    def run(self, screen):
        clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 36)
        small_font = pygame.font.SysFont(None, 24)
        
        self.boss_img = pygame.transform.scale(pygame.image.load(self.boss_img_path), (128, 128))
        self.heart_img = pygame.transform.scale(pygame.image.load(self.heart_img_path), (32, 32))
        self.heart_rect = self.heart_img.get_rect(center=BOX.center)
        for attack in self.attacks:
            attack.load()

        attack_start = time.time()
        fight_bar_x = 300
        fight_direction = 1

        while self.boss_hp > 0 and self.player_stats.current_hp > 0:
            screen.fill((0, 0, 0))
            dt = clock.tick(60) / 1000
            
            # Check happiness threshold BEFORE processing events
            if self.happiness >= self.max_happiness and self.phase != "spare_dialogue":
                self.dialogue_manager.start_dialogue(f"* you spared {self.boss_name} *")
                self.phase = "spare_dialogue"
                self.battle_spared = True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if self.phase == "dialogue" or self.phase == "spare_dialogue":
                            if self.dialogue_manager.current_text == self.dialogue_manager.full_text:
                                if self.phase == "dialogue":
                                    self.phase = "attack"
                                    attack_start = time.time()
                                else:
                                    self.boss_hp = 0
                            else:
                                self.dialogue_manager.skip()
                        elif self.phase == "victory" or self.phase == "level_up":
                            if self.dialogue_manager.current_text == self.dialogue_manager.full_text:
                                if self.phase == "level_up":
                                    self.phase = "victory"
                                    self.dialogue_manager.start_dialogue(f"* You defeated {self.boss_name}! *")
                                else:
                                    return True  # End battle
                            else:
                                self.dialogue_manager.skip()
                # Check for input events during all phases
                if self.phase == "final_dialogue":
                    if self.dialogue_manager.handle_input(event):
                        choice = self.dialogue_manager.choice_made
                        if choice == "run":
                            self.boss_hp = 0  # End battle successfully
                        elif choice == "do not":
                            self.player_stats.current_hp = 0  # Player loses
                elif self.phase == "choice":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mx, my = pygame.mouse.get_pos()
                        fight_btn = pygame.Rect(200, 500, 100, 40)
                        item_btn = pygame.Rect(500, 500, 100, 40)
                        if fight_btn.collidepoint(mx, my):
                            self.phase = "fight"
                        elif item_btn.collidepoint(mx, my):
                            self.happiness += 10
                            if self.spare_phrase:
                                self.dialogue_manager.start_dialogue(self.spare_phrase)
                            else:
                                self.dialogue_manager.start_dialogue("* You showed mercy *")
                            self.phase = "dialogue"
                elif self.phase == "fight":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        if 370 <= fight_bar_x <= 420:
                            damage_dealt = self.player_stats.get_damage()
                            self.boss_hp -= damage_dealt
                            if self.boss_hp <= 0:
                                self.battle_won = True
                                # Give EXP and check for level up
                                leveled_up = self.player_stats.gain_exp(self.exp_reward)
                                if leveled_up:
                                    hp_gained = self.player_stats.get_max_hp() - (self.player_stats.get_max_hp() - 8)
                                    self.level_up_message = f"* LEVEL UP! You are now level {self.player_stats.level}! *\n* Max HP increased by {hp_gained}! *\n* ATK increased by 3! *"
                                    self.dialogue_manager.start_dialogue(self.level_up_message)
                                    self.phase = "level_up"
                                else:
                                    self.dialogue_manager.start_dialogue(f"* You defeated {self.boss_name}! *\n* You gained {self.exp_reward} EXP! *")
                                    self.phase = "victory"
                            else:
                                self.phase = "attack"
                                attack_start = time.time()
                        else:
                            # Miss - still go to attack phase but no damage
                            self.phase = "attack"
                            attack_start = time.time()

            if self.is_leafy_boss and self.player_stats.current_hp <= 2 and not self.final_dialogue_started:
                self.phase = "final_dialogue"
                self.dialogue_manager.start_choice_dialogue("MUAHAHAHAHA YOUR SOUL IS GONNA BE MINE", ["run", "do not"])
                self.final_dialogue_started = True

            if self.phase == "dialogue":
                self.dialogue_manager.update()
                self.dialogue_manager.draw(screen)
                    
            elif self.phase == "spare_dialogue":
                self.dialogue_manager.update()
                self.dialogue_manager.draw(screen)
                
            elif self.phase == "victory" or self.phase == "level_up":
                self.dialogue_manager.update()
                self.dialogue_manager.draw(screen)
                    
            elif self.phase == "attack":
                keys = pygame.key.get_pressed()
                # Movement logic only in 'attack' phase
                if keys[pygame.K_LEFT]: self.heart_rect.x -= 5
                if keys[pygame.K_RIGHT]: self.heart_rect.x += 5
                if keys[pygame.K_UP]: self.heart_rect.y -= 5
                if keys[pygame.K_DOWN]: self.heart_rect.y += 5
                self.heart_rect.clamp_ip(BOX)

                if time.time() - attack_start > 15:
                    self.phase = "choice"
                else:
                    if not self.selected_attack or random.random() < 0.01:
                        self.selected_attack = random.choice(self.attacks)
                        self.selected_attack.projectiles.clear()
                    hit = self.selected_attack.update(time.time() - attack_start, self.heart_rect)
                    if hit:

                        if self.player_stats.take_damage(0.1):
                            raise SystemExit()
                    self.selected_attack.draw(screen)
                

            elif self.phase == "choice":
                fight_btn = pygame.Rect(200, 500, 100, 40)
                item_btn = pygame.Rect(500, 500, 100, 40)
                pygame.draw.rect(screen, (255, 0, 0), fight_btn)
                pygame.draw.rect(screen, (0, 255, 0), item_btn)
                screen.blit(font.render("FIGHT", True, (255, 255, 255)), (210, 510))
                screen.blit(font.render("SPARE", True, (255, 255, 255)), (510, 510))

            elif self.phase == "fight":
                pygame.draw.rect(screen, (255, 255, 255), (300, 400, 200, 10))
                pygame.draw.rect(screen, (255, 0, 0), (fight_bar_x, 395, 10, 20))
                pygame.draw.rect(screen, (0, 255, 0), (390, 395, 20, 20))

                fight_bar_x += fight_direction * 5
                if fight_bar_x <= 300 or fight_bar_x >= 490:
                    fight_direction *= -1
            
            elif self.phase == "final_dialogue":
                # Draw the boss on screen during dialogue
                screen.blit(self.boss_img, (WIDTH - 200, 50))
                
                # Use DialogueManager for the final dialogue
                self.dialogue_manager.update()
                self.dialogue_manager.draw(screen)

            # Always draw boss
            screen.blit(self.boss_img, (WIDTH - 200, 50))
            
            # Only draw heart during attack phase
            if self.phase == "attack": 
                screen.blit(self.heart_img, self.heart_rect)
                pygame.draw.rect(screen, (255, 255, 255), BOX, 2)
            
            # Draw boss HP bar
            
            
            # Draw player stats
            stats = self.player_stats.get_stats_display()
            screen.blit(font.render(f"{self.boss_name} HP: {self.boss_hp}/{self.boss_max_hp}", True, (255, 255, 255)), (50, 50))
            screen.blit(font.render(f"Player HP: {math.floor(stats['hp'])}/{stats['max_hp']}", True, (255, 255, 255)), (50, 80))
            
            boss_hp_percentage = stats['hp'] / stats['max_hp']
            boss_hp_bar_width = int(200 * boss_hp_percentage)
            pygame.draw.rect(screen, (255, 0, 0), (50, 110, boss_hp_bar_width, 20))
            pygame.draw.rect(screen, (255, 255, 255), (50, 110, 200, 20), 2)

            # Draw additional stats
            screen.blit(small_font.render(f"Level: {stats['level']}", True, (255, 255, 255)), (400, 50))
            screen.blit(small_font.render(f"EXP: {stats['exp']}", True, (255, 255, 255)), (400, 70))
            screen.blit(small_font.render(f"ATK: {stats['damage']}", True, (255, 255, 255)), (400, 90))

            pygame.display.flip()
        
        return True # Battle ended