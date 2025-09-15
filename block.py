import pygame
import random

# A dictionary to define the properties of each block type.
BLOCK_INFO = {
    'G': {'color': (34, 139, 34), 'walkable': True, 'tree': False, 'tree_bottom':False, 'tree_up':False,"house":False},  # Grass
    'P': {'color': (210, 180, 140), 'walkable': True, 'tree': False, 'tree_bottom':False, 'tree_up':False,"house":False}, # Path
    'W': {'color': (100, 100, 100), 'walkable': False, 'tree': False, 'tree_bottom':False, 'tree_up':False,"house":False},  # Wall
    'O': {'color': (168, 96, 50), 'walkable': False, 'tree': False, 'tree_bottom':False, 'tree_up':False,"house":False}, # Oak planks
    'T': {'color': (34, 139, 34), 'walkable': False, 'tree':True, 'tree_bottom':True, 'tree_up':False,"house":False},
    't': {'color': (34, 139, 34), 'walkable': False, 'tree':True, 'tree_bottom':False, 'tree_up':True, "house":False},
    
    # House parts - 36 total (6x6 grid)
    # Row 1 (A-F)
    'A': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(0,0)},
    'B': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(1,0)},
    'C': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(2,0)},
    'D': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(3,0)},
    'E': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(4,0)},
    'F': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(5,0)},
    
    # Row 2 (G-L)
    'H': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(0,1)},
    'I': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(1,1)},
    'J': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(2,1)},
    'K': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(3,1)},
    'L': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(4,1)},
    'M': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(5,1)},
    
    # Row 3 (N-S)
    'N': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(0,2)},
    'Q': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(1,2)},
    'R': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(2,2)},
    'S': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(3,2)},
    'U': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(4,2)},
    'V': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(5,2)},
    
    # Row 4 (X-Z, then 0-2)
    'X': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(0,3)},
    'Y': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(1,3)},
    'Z': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(2,3)},
    '0': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(3,3)},
    '$': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(4,3)},
    '%': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(5,3)},
    
    # Row 5 (1-6)
    '1': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(0,4)},
    '2': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(1,4)},
    '3': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(2,4)},
    '4': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(3,4)},
    '5': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(4,4)},
    '6': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(5,4)},
    
    # Row 6 (7-9, then special chars)
    '7': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(0,5)},
    '8': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(1,5)},
    '9': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(2,5)},
    '!': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(3,5)},
    '@': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(4,5)},
    '#': {'color': (34, 139, 34), 'walkable': False, 'tree':False, 'tree_bottom':False, 'tree_up':False,"house":True,"house_grid_pos":(5,5)},
}

# Use a cache to store pre-rendered block images for performance
block_cache = {}
# Cache for the full house image to avoid loading it multiple times
house_full_image = None

def load_house_image():
    """Load the full 192x192 house image once and cache it."""
    global house_full_image
    if house_full_image is None:
        try:
            house_full_image = pygame.image.load("images/background/house.png").convert_alpha()
            print("Full house image loaded successfully!")
        except pygame.error as e:
            print(f"Error loading full house image: {e}")
            house_full_image = False  # Mark as failed to avoid retrying
    return house_full_image

def generate_block_image(block_type, tile_size):
    """
    Generates a pygame Surface for a given block type with a random mask effect.
    Caches the generated image to prevent regenerating it every frame.
    """
    # First, check if the image is already in the cache
    if block_type in block_cache:
        return block_cache[block_type]

    info = BLOCK_INFO.get(block_type)
    if not info:
        # Default to a gray, non-walkable block if the type is not found
        info = {'color': (100, 100, 100), 'walkable': False, 'tree': False, "house":False}

    # Create the base surface for the block
    block_surface = pygame.Surface((tile_size, tile_size))
    block_surface.fill(info['color'])

    # Apply a randomized mask for visual variation
    if info['walkable'] or info['tree'] or info['house']:
        mask = pygame.mask.from_surface(block_surface)
        for _ in range(10):
            x = random.randint(0, tile_size - 1)
            y = random.randint(0, tile_size - 1)
            if random.random() < 0.5:
                mask.set_at((x, y), 1)
            else:
                mask.set_at((x, y), 0)
        
        # Re-create the surface from the modified mask
        new_surface = mask.to_surface(setcolor=info['color'])   
        new_surface.set_colorkey((0, 0, 0))
        block_surface = new_surface

    # If it's a tree block, draw the tree image onto the surface
    if info['tree']:
        if info['tree_bottom']:
            try:
                tree_img = pygame.image.load("images/background/tree.png").convert_alpha()
                # Scale the tree image to fit the tile
                tree_img = pygame.transform.scale(tree_img, (tile_size, tile_size * 2)) 
                
                # Position the tree image correctly on the block surface
                # This centers the tree image at the top of the block
                tree_rect = tree_img.get_rect(midbottom=(block_surface.get_width()/2 , block_surface.get_height()))
                block_surface.blit(tree_img, tree_rect)
            except pygame.error as e:
                print(f"Error loading tree image: {e}")
                # Fallback to just the grass block if the image can't be loaded
                pass
        if info['tree_up']:
            try:
                tree_img = pygame.image.load("images/background/tree.png").convert_alpha()
                # Scale the tree image to fit the tile
                tree_img = pygame.transform.scale(tree_img, (tile_size, tile_size * 2)) 
                
                # Position the tree image correctly on the block surface
                # This centers the tree image at the top of the block
                tree_rect = tree_img.get_rect(midbottom=(block_surface.get_width()/2 , block_surface.get_height()*2))
                block_surface.blit(tree_img, tree_rect)
            except pygame.error as e:
                print(f"Error loading tree image: {e}")
                # Fallback to just the grass block if the image can't be loaded
                pass
    
    # If it's a house block, extract the correct piece from the full house image
    if info["house"]:
        house_img = load_house_image()
        if house_img:
            try:
                grid_x, grid_y = info["house_grid_pos"]
                
                # Calculate the source rectangle in the 192x192 image
                src_x = grid_x * 32  # Each piece is 32x32
                src_y = grid_y * 32
                src_rect = (src_x, src_y, 32, 32)
                
                # Extract the piece from the full image
                house_piece = house_img.subsurface(src_rect)
                
                # Scale it to match the current tile size (in case tile_size != 32)
                if tile_size != 32:
                    house_piece = pygame.transform.scale(house_piece, (tile_size, tile_size))
                
                # Draw it onto our block surface
                block_surface.blit(house_piece, (0, 0))
                
            except (pygame.error, ValueError) as e:
                print(f"Error processing house piece at {info['house_grid_pos']}: {e}")
                # Fallback: draw a colored rectangle with the character
                pygame.draw.rect(block_surface, (139, 69, 19), (0, 0, tile_size, tile_size))
                font = pygame.font.Font(None, min(24, tile_size // 2))
                text = font.render(block_type, True, (255, 255, 255))
                block_surface.blit(text, (tile_size//4, tile_size//4))

    # Cache the generated image before returning
    block_cache[block_type] = block_surface
    return block_surface