import pygame
import random
import time
import os
import math
import json

from constants import WIDTH, HEIGHT, BOX
from player import Player
from dialogue_manager import DialogueManager
from battle import Attack, BossBattle, pattern_wave, pattern_spike, pattern_chase, pattern_circle_spiral, pattern_diagonal_cross, pattern_straight_line, pattern_center_out, pattern_left_to_right, pattern_random_spawn, pattern_random_walk, pattern_top_to_bottom
from block import BLOCK_INFO, generate_block_image

# === Global Variables for Game State ===
# We use this to switch between the overworld, dialogue, and battle
game_state = "overworld"
dialogue_text = [
    "hey.. a human",
    "I havent seen one for ages...",
    "I am Leafy, and these are the overshades",
    "Nice name isnt it? well uhh overshades need you",
    "there's a legend that says only a human can defeat the Void",
    "or I mean, a human soul",
    "prepare yourself, ITS GONNA BE RIPPED OUT OF YOUR BODY"
]
current_dialogue_line = 0

# Random Encounter Variables
encounter_rate = 0.001 # A value between 0.0 and 1.0. Higher means more frequent encounters.
steps_since_last_encounter = 0
min_steps_between_encounters = 100  # Minimum steps before a new encounter can occur

# === Map & Player Variables ===
world_map_data = None
full_map_tiles = []
full_map_surface = None
TILE_SIZE = 32
FULL_MAP_WIDTH_TILES = 0
FULL_MAP_HEIGHT_TILES = 0
FULL_MAP_WIDTH_PX = 0
FULL_MAP_HEIGHT_PX = 0

# Boss variables
leafy_img = pygame.transform.scale(pygame.image.load("images/leafy/idle.png"), (128, 128))
leafy_world_x = 300
leafy_world_y = 300
leafy_rect = leafy_img.get_rect(center=(leafy_world_x, leafy_world_y))
leafy_done = False

# Ghost variables
ghost_img = pygame.transform.scale(pygame.image.load("images/ghost/frame_0.png"), (128, 128))
scali_img = pygame.transform.scale(pygame.image.load("images/scali/idle.png"), (128, 128))
active_boss = None



# === Map Switching Variables and Data ===
current_map_state = None  # Tracks the current map state to avoid constant reloading

# The two different map configurations for map_0_2.json
MAP_0_2_DEFAULT = {
    "tile_size": 32,
    "map": [
        "WWWWWWWWWWWWWWWWWWWW",
        "OGGGGGGGGGGGGGGGGGGG",
        "OGGGGGGGGGGGGGGGGGGG",
        "OPPPPPPPPPPPPPPPPPPP",
        "OPPPPPPPPPPPPPPPPPPP",
        "OPPPPPPPPPPPPPPPPPPP",
        "OGGGGGGGGGGGGGGGGGGG",
        "OGGGGGGGGGGGGGGGGGGG",
        "WWWWWWWWWWWWWWWWWWWW",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG"
    ]
}

MAP_0_2_CHANGED = {
    "tile_size": 32,
    "map": [
        "WWWWWWWWWWWWWWWWWWWW",
        "OGGGGGGGGGGGGGGGGGGG",
        "OGGGGGGGGGGGGGGGGGGG",
        "PPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPP",
        "OGGGGGGGGGGGGGGGGGGG",
        "OGGGGGGGGGGGGGGGGGGG",
        "WWWWWWWWWWWWWWWWWWWW",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGG"
    ]
}

def save_map_data(file_path, data):
    """Saves the given data dictionary to a JSON file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Map data saved to '{file_path}' successfully.")
    except IOError as e:
        print(f"Error: Could not save map file '{file_path}'. {e}")

def load_full_map(world_map_file_path):
    """
    Loads all map pages, stitches them together into a single large surface and tile grid.
    """
    global world_map_data, full_map_tiles, full_map_surface, TILE_SIZE
    global FULL_MAP_WIDTH_TILES, FULL_MAP_HEIGHT_TILES, FULL_MAP_WIDTH_PX, FULL_MAP_HEIGHT_PX

    try:
        with open(world_map_file_path, 'r') as f:
            world_map_data = json.load(f)
            print("World map data loaded successfully.")
    except FileNotFoundError:
        print(f"Error: World map file '{world_map_file_path}' not found.")
        world_map_data = {}
        return False
    
    # Determine the total size of the world map in tiles
    map_pages_y = len(world_map_data)
    map_pages_x = max(len(world_map_data[y]) for y in world_map_data)
            
    # Load the first map to get the tile size and dimensions
    first_map_file = world_map_data.get('0', {}).get('0')
    if not first_map_file:
        print("Error: Starting map (0,0) not found.")
        return False
        
    try:
        with open(first_map_file, 'r') as f:
            data = json.load(f)
            TILE_SIZE = data['tile_size']
            page_width_tiles = len(data['map'][0])
            page_height_tiles = len(data['map'])
    except FileNotFoundError:
        print(f"Error: Map file '{first_map_file}' not found.")
        return False
        
    FULL_MAP_WIDTH_TILES = map_pages_x * page_width_tiles
    FULL_MAP_HEIGHT_TILES = map_pages_y * page_height_tiles
    FULL_MAP_WIDTH_PX = FULL_MAP_WIDTH_TILES * TILE_SIZE
    FULL_MAP_HEIGHT_PX = FULL_MAP_HEIGHT_TILES * TILE_SIZE
    
    # Initialize the full map surface and tile grid
    full_map_surface = pygame.Surface((FULL_MAP_WIDTH_PX, FULL_MAP_HEIGHT_PX))
    full_map_tiles = [[None for _ in range(FULL_MAP_WIDTH_TILES)] for _ in range(FULL_MAP_HEIGHT_TILES)]
    
    print(f"Creating a {map_pages_x}x{map_pages_y} world map...")
    print(f"Total size: {FULL_MAP_WIDTH_PX}x{FULL_MAP_HEIGHT_PX} pixels")

    # Stitch all maps together
    for y in range(map_pages_y):
        for x in range(map_pages_x):
            map_file_name = world_map_data.get(str(y), {}).get(str(x))
            if not map_file_name:
                continue
                
            with open(map_file_name, 'r') as f:
                data = json.load(f)
                map_tiles = data['map']
                
                # Draw tiles onto the full surface and copy tile data to the grid
                for row_idx, tile_row in enumerate(map_tiles):
                    for col_idx, block_type in enumerate(tile_row):
                        block_image = generate_block_image(block_type, TILE_SIZE)
                        
                        full_x_px = (x * page_width_tiles + col_idx) * TILE_SIZE
                        full_y_px = (y * page_height_tiles + row_idx) * TILE_SIZE
                        
                        full_map_surface.blit(block_image, (full_x_px, full_y_px))
                        
                        full_map_tiles[y * page_height_tiles + row_idx][x * page_width_tiles + col_idx] = block_type
    print("Map fully loaded and stitched.")
    return True

def get_block_at_coords(x, y):
    """Returns the block type at a given world coordinate."""
    tile_x = int(x // TILE_SIZE)
    tile_y = int(y // TILE_SIZE)
    
    if 0 <= tile_y < FULL_MAP_HEIGHT_TILES and 0 <= tile_x < FULL_MAP_WIDTH_TILES:
        return full_map_tiles[tile_y][tile_x]
    return 'W' # Default to a wall if outside the map boundaries

def is_walkable(x, y):
    """Checks if a given world coordinate is on a walkable block."""
    block_type = get_block_at_coords(x, y)
    return BLOCK_INFO.get(block_type, {}).get('walkable', False)

def check_player_collision(new_x, new_y, player_rect_width, player_rect_height):
    """
    Checks if the player's entire sprite can move to the new position.
    This checks all four corners of the player's bounding box.
    """
    # Define the points to check on the player's sprite
    # We check a few pixels in from each corner to avoid false positives on tile edges
    points_to_check = [
        (new_x, new_y),  # Top-left corner
        (new_x + player_rect_width - 1, new_y),  # Top-right corner
        (new_x, new_y + player_rect_height - 1),  # Bottom-left corner
        (new_x + player_rect_width - 1, new_y + player_rect_height - 1)  # Bottom-right corner
    ]

    for point_x, point_y in points_to_check:
        if not is_walkable(point_x, point_y):
            return False  # Found a non-walkable tile, so stop and return False

    return True  # All checked points are on walkable tiles

# === Main Game Loop ===
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Initial check and save for map_0_2.json before loading the full map
    save_map_data("maps/map_0_2.json", MAP_0_2_DEFAULT)
    current_map_state = "default"

    if not load_full_map("world_map.json"):
        pygame.quit()
        exit()
    
    # Player starts in the middle of the first map page (0,0)
    player_start_x = 200
    player_start_y = 200
    player = Player(player_start_x, player_start_y)
    
    dialogue_manager = DialogueManager()

    # Create the battle instance for Leafy
    leafy_attacks = [
        Attack("Wave", "images/leafy/attack1.png", pattern_wave),
        Attack("Straight Line", "images/leafy/attack2.png", pattern_straight_line),
        Attack("Top to Bottom", "images/leafy/attack1.png", pattern_top_to_bottom),
        Attack("Left to Right", "images/leafy/attack2.png", pattern_left_to_right),
        Attack("Center Out", "images/leafy/attack1.png", pattern_center_out),
        Attack("Random Spawn", "images/leafy/attack2.png", pattern_random_spawn),
        Attack("Random Walk", "images/leafy/attack1.png", pattern_random_walk),
        Attack("Spike", "images/leafy/attack2.png", pattern_spike),
        Attack("Diagonal Cross", "images/leafy/attack1.png", pattern_diagonal_cross),
        Attack("Circle Spiral", "images/leafy/attack1.png", pattern_circle_spiral),
        Attack("Chase", "images/leafy/attack2.png", pattern_chase)
    ]
    leafy_battle = BossBattle(
        boss_name="Leafy",
        boss_img_path="images/leafy/idle.png",
        heart_img_path="images/player/heart/heart.png",
        attacks=leafy_attacks,
        boss_hp=100,
        boss_leafy=True,
        dialogue_manager=dialogue_manager,
        spare_phrase="IN THIS WORLD ITS KILL OR BE KILLED",
        max_happiness=20000
    )

    # Create the battle instance for Ghost
    ghost_attacks = [
        Attack("Random Spawn", "images/ghost/frame_2.png", pattern_random_spawn),
        Attack("Diagonal Cross", "images/ghost/frame_1.png", pattern_diagonal_cross),
        Attack("Random Walk", "images/ghost/frame_1.png", pattern_random_walk)
    ]
    ghost_battle = BossBattle(
        boss_name="Ghost",
        boss_img_path="images/ghost/frame_0.png",
        heart_img_path="images/player/heart/heart.png",
        attacks=ghost_attacks,
        boss_hp=10,
        dialogue_manager=dialogue_manager,
        max_happiness=20,
        spare_phrase="* Ghost seems confused *"
    )

    scali_attacks = [
        Attack("wave", "images/scali/attack0.png", pattern_wave),
        Attack("Circle Spiral", "images/scali/attack1.png", pattern_circle_spiral)
    ]
    scali_battle = BossBattle(
        boss_name="Scali",
        boss_img_path="images/scali/idle.png",
        heart_img_path="images/player/heart/heart.png",
        attacks=scali_attacks,
        boss_hp=15,
        dialogue_manager=dialogue_manager,
        max_happiness=30,
        spare_phrase="* Scali seems confused *"
    )
    
    # Load and play overworld music
    pygame.mixer.music.load("songs/ruins.mp3")
    pygame.mixer.music.play(loops=-1)
    
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Check for key presses to skip dialogue
            if game_state == "dialogue" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if dialogue_manager.current_text != dialogue_manager.full_text:
                        dialogue_manager.skip()
                    else:
                        current_dialogue_line += 1
                        if active_boss == "leafy" and current_dialogue_line < len(dialogue_text):
                            dialogue_manager.start_dialogue(dialogue_text[current_dialogue_line])
                        else:
                            game_state = "battle"
                            
        screen.fill((0, 0, 0)) # Set background to black
        
        # Game State Logic
        if game_state == "overworld":
            # === Map Switching Logic ===
            if 1200 <= player.world_x <= 1328 and 50 <= player.world_y <= 192:
                if current_map_state != "changed":
                    print("Player entered the special zone! Changing map...")
                    save_map_data("maps/map_0_2.json", MAP_0_2_CHANGED)
                    if load_full_map("world_map.json"):
                        current_map_state = "changed"
            else:
                if current_map_state != "default":
                    print("Player left the special zone! Changing map back...")
                    save_map_data("maps/map_0_2.json", MAP_0_2_DEFAULT)
                    if load_full_map("world_map.json"):
                        current_map_state = "default"
            
            keys = pygame.key.get_pressed()
            
            # Get player's intended new position
            new_x, new_y = player.world_x, player.world_y
            moving = False
            direction = "down"
            
            if keys[pygame.K_LEFT]:
                new_x -= player.speed
                moving = True
                direction = "left"
            if keys[pygame.K_RIGHT]:
                new_x += player.speed
                moving = True
                direction = "right"
            if keys[pygame.K_UP]:
                new_y -= player.speed
                moving = True
                direction = "up"
            if keys[pygame.K_DOWN]:
                new_y += player.speed
                moving = True
                direction = "down"

            # Check for boundaries of the full map
            new_x = max(0, min(new_x, FULL_MAP_WIDTH_PX - player.rect.width))
            new_y = max(0, min(new_y, FULL_MAP_HEIGHT_PX - player.rect.height))

            # Only update player position if the entire sprite is on walkable ground
            if check_player_collision(new_x, new_y, player.rect.width, player.rect.height):
                player.world_x = new_x
                player.world_y = new_y
                
                # Random encounter check
                if moving and random.random() < encounter_rate and steps_since_last_encounter >= min_steps_between_encounters:
                    game_state = "dialogue"
                    active_boss = random.choice(["ghost", "scali"])
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    
                    current_dialogue_line = 0 # Reset dialogue counter for new encounter
                    if active_boss == "ghost":
                        dialogue_manager.start_dialogue("* You found a Ghost! *")
                        pygame.mixer.music.load("songs/ghost_fight.mp3")
                    if active_boss == "scali":
                        dialogue_manager.start_dialogue("* You found a Scali! *")
                        pygame.mixer.music.load("songs/enemy.mp3")
                    
                    steps_since_last_encounter = 0
                    pygame.mixer.music.play(loops=-1)

                else:
                    steps_since_last_encounter += 1

            # Update player animation
            player.update_animation(moving, direction)

            # === Draw Map and Objects with Camera Offset ===
            camera_offset_x = player.screen_x - player.world_x
            camera_offset_y = player.screen_y - player.world_y
            
            # Draw the full map surface
            screen.blit(full_map_surface, (camera_offset_x, camera_offset_y))

            # Draw player at the center of the screen
            screen.blit(player.get_frame(), (player.screen_x, player.screen_y))

            # Draw Leafy
            if not leafy_done:
                boss_screen_x = leafy_world_x + camera_offset_x
                boss_screen_y = leafy_world_y + camera_offset_y
                screen.blit(leafy_img, (boss_screen_x, boss_screen_y))

                # Update leafy_rect for collision detection
                leafy_rect.center = (boss_screen_x + leafy_img.get_width() / 2, boss_screen_y + leafy_img.get_height() / 2)

                # Check for collision with Leafy
                if player.rect.colliderect(leafy_rect):
                    game_state = "dialogue"
                    active_boss = "leafy"
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load("songs/enemy.mp3")
                    pygame.mixer.music.play(loops=-1)
                    current_dialogue_line = 0 # Reset dialogue counter for new encounter
                    dialogue_manager.start_dialogue(dialogue_text[current_dialogue_line])

        elif game_state == "dialogue":
            # Display the correct boss and dialogue
            if active_boss == "leafy":
                screen.blit(leafy_img, (WIDTH - 150, 100))
                dialogue_manager.update()
                dialogue_manager.draw(screen)
            elif active_boss == "ghost":
                screen.blit(ghost_img, (WIDTH - 150, 100))
                dialogue_manager.update()
                dialogue_manager.draw(screen)
            elif active_boss == "scali":
                screen.blit(scali_img, (WIDTH - 150, 100))
                dialogue_manager.update()
                dialogue_manager.draw(screen)


        elif game_state == "battle":
            # Run the battle loop
            battle_is_over = False
            if active_boss == "leafy":
                battle_is_over = leafy_battle.run(screen)
            elif active_boss == "ghost":
                battle_is_over = ghost_battle.run(screen)
            elif active_boss == "scali":
                battle_is_over = scali_battle.run(screen)

            # Check if the battle is over
            if battle_is_over:
                game_state = "overworld"
                if active_boss == "ghost":
                    # Reset the ghost battle instance with proper dialogue_manager
                    ghost_battle = BossBattle(
                        boss_name="Ghost",
                        boss_img_path="images/ghost/frame_0.png",
                        heart_img_path="images/player/heart/heart.png",
                        attacks=ghost_attacks,
                        boss_hp=10,
                        dialogue_manager=DialogueManager(),  # Add this line!
                        max_happiness=20,
                        spare_phrase="* Ghost seems confused *"
                    )
                if active_boss == "scali":
                    # Reset the scali battle instance with proper dialogue_manager
                    scali_battle = BossBattle(
                        boss_name="Scali",
                        boss_img_path="images/scali/idle.png",
                        heart_img_path="images/player/heart/heart.png",
                        attacks=scali_attacks,
                        boss_hp=15,
                        dialogue_manager=DialogueManager(),  # Add this line!
                        max_happiness=30,
                        spare_phrase="* Scali seems confused *"
                    )
                if active_boss == "leafy":
                    leafy_done = True
                
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                if not player.world_y >= 1472:
                    pygame.mixer.music.load("songs/ruins.mp3")
                else:
                    pygame.mixer.music.load("songs/snowy.mp3")
                pygame.mixer.music.play()
            
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    exit()
