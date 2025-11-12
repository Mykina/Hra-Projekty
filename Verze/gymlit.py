import pygame
import sys
import math
import urllib.request
from io import BytesIO

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
PLAYER_SIZE = 48
NPC_SIZE = 48
FPS = 60
MOVE_SPEED = 2.5

# Colors - Omori-inspired palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CREAM = (255, 248, 231)
DARK_PURPLE = (45, 35, 60)
LIGHT_PURPLE = (90, 70, 110)
SOFT_BLUE = (135, 175, 210)
WARM_BROWN = (139, 115, 85)
DARK_BROWN = (80, 60, 50)
BEIGE = (210, 180, 140)
SOFT_GREEN = (160, 195, 140)
DARK_GREEN = (80, 120, 80)
SOFT_RED = (200, 100, 100)
SOFT_YELLOW = (240, 220, 140)
SHADOW = (20, 20, 40, 120)

# Enhanced texture creation with Omori-style aesthetics
def create_player_sprite(frame=0):
    surf = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
    
    # Shadow
    pygame.draw.ellipse(surf, (0, 0, 0, 60), (8, 40, 32, 8))
    
    # Body - blue shirt
    body_color = (80, 130, 200)
    pygame.draw.ellipse(surf, body_color, (14, 20, 20, 18))
    
    # Head
    head_color = (255, 220, 180)
    pygame.draw.circle(surf, head_color, (24, 14), 10)
    
    # Hair - simple anime style
    hair_color = (60, 50, 40)
    pygame.draw.arc(surf, hair_color, (16, 6, 16, 12), 0, math.pi, 4)
    
    # Eyes - expressive
    eye_y = 13
    if frame % 60 > 55:  # Blink
        pygame.draw.line(surf, BLACK, (19, eye_y), (21, eye_y), 2)
        pygame.draw.line(surf, BLACK, (27, eye_y), (29, eye_y), 2)
    else:
        pygame.draw.circle(surf, BLACK, (20, eye_y), 2)
        pygame.draw.circle(surf, BLACK, (28, eye_y), 2)
        pygame.draw.circle(surf, WHITE, (21, eye_y-1), 1)
        pygame.draw.circle(surf, WHITE, (29, eye_y-1), 1)
    
    # Simple smile
    pygame.draw.arc(surf, BLACK, (19, 15, 10, 6), 0, math.pi, 1)
    
    # Arms
    arm_color = (70, 120, 180)
    pygame.draw.rect(surf, arm_color, (10, 24, 6, 12))
    pygame.draw.rect(surf, arm_color, (32, 24, 6, 12))
    
    # Legs - walking animation
    leg_offset = math.sin(frame * 0.2) * 2 if frame > 0 else 0
    pygame.draw.rect(surf, (50, 50, 80), (16, 36 + leg_offset, 6, 8))
    pygame.draw.rect(surf, (50, 50, 80), (26, 36 - leg_offset, 6, 8))
    
    return surf

def create_npc_sprite(color, personality="normal", frame=0):
    surf = pygame.Surface((NPC_SIZE, NPC_SIZE), pygame.SRCALPHA)
    
    # Shadow
    pygame.draw.ellipse(surf, (0, 0, 0, 60), (8, 40, 32, 8))
    
    # Body
    pygame.draw.ellipse(surf, color, (14, 20, 20, 18))
    
    # Head
    head_color = (255, 220, 180)
    pygame.draw.circle(surf, head_color, (24, 14), 10)
    
    # Hair based on personality
    hair_color = (60, 50, 40)
    if personality == "teacher":
        pygame.draw.arc(surf, (100, 80, 60), (16, 6, 16, 12), 0, math.pi, 4)
    elif personality == "janitor":
        pygame.draw.rect(surf, hair_color, (18, 8, 12, 8))
    else:
        pygame.draw.arc(surf, hair_color, (16, 6, 16, 12), 0, math.pi, 4)
    
    # Eyes - different expressions
    eye_y = 13
    if personality == "friendly":
        # Happy eyes
        pygame.draw.arc(surf, BLACK, (18, 11, 5, 5), math.pi, 2*math.pi, 2)
        pygame.draw.arc(surf, BLACK, (26, 11, 5, 5), math.pi, 2*math.pi, 2)
    elif personality == "serious":
        # Serious eyes
        pygame.draw.line(surf, BLACK, (19, eye_y-1), (21, eye_y+1), 2)
        pygame.draw.line(surf, BLACK, (27, eye_y-1), (29, eye_y+1), 2)
    else:
        # Normal eyes
        pygame.draw.circle(surf, BLACK, (20, eye_y), 2)
        pygame.draw.circle(surf, BLACK, (28, eye_y), 2)
        pygame.draw.circle(surf, WHITE, (21, eye_y-1), 1)
    
    # Mouth
    pygame.draw.arc(surf, BLACK, (19, 15, 10, 6), 0, math.pi, 1)
    
    # Arms
    darker = tuple(max(0, c - 30) for c in color)
    pygame.draw.rect(surf, darker, (10, 24, 6, 12))
    pygame.draw.rect(surf, darker, (32, 24, 6, 12))
    
    # Legs
    pygame.draw.rect(surf, (50, 50, 80), (16, 36, 6, 8))
    pygame.draw.rect(surf, (50, 50, 80), (26, 36, 6, 8))
    
    return surf

def create_room_background(room_name):
    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    if room_name == "School Hall":
        # Main hall - warm and inviting
        surf.fill((220, 210, 200))
        
        # Floor tiles
        for x in range(0, SCREEN_WIDTH, 64):
            for y in range(SCREEN_HEIGHT//2, SCREEN_HEIGHT, 64):
                color = (190, 185, 180) if (x+y) % 128 == 0 else (200, 195, 190)
                pygame.draw.rect(surf, color, (x, y, 64, 64))
                pygame.draw.rect(surf, (180, 175, 170), (x, y, 64, 64), 1)
        
        # Walls with wainscoting
        pygame.draw.rect(surf, (160, 140, 120), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT//2))
        pygame.draw.rect(surf, (140, 120, 100), (0, SCREEN_HEIGHT//2-40, SCREEN_WIDTH, 40))
        
        # Windows on top wall
        for i in range(3):
            x = 150 + i * 150
            pygame.draw.rect(surf, (150, 200, 240), (x, 30, 80, 100))
            pygame.draw.rect(surf, (100, 80, 70), (x, 30, 80, 100), 4)
            pygame.draw.line(surf, (100, 80, 70), (x+40, 30), (x+40, 130), 4)
        
        # LEFT SIDE DOOR - Buffet
        pygame.draw.rect(surf, (100, 80, 60), (40, 180, 60, 80))
        pygame.draw.rect(surf, (80, 60, 40), (45, 185, 50, 70))
        pygame.draw.circle(surf, (200, 180, 100), (85, 220), 5)
        
        # RIGHT SIDE DOOR - Locker Room
        pygame.draw.rect(surf, (100, 80, 60), (SCREEN_WIDTH-100, 180, 60, 80))
        pygame.draw.rect(surf, (80, 60, 40), (SCREEN_WIDTH-95, 185, 50, 70))
        pygame.draw.circle(surf, (200, 180, 100), (SCREEN_WIDTH-55, 220), 5)
        
        # BOTTOM LEFT DOOR - Bathroom
        pygame.draw.rect(surf, (100, 80, 60), (160, SCREEN_HEIGHT-40, 60, 40))
        pygame.draw.rect(surf, (80, 60, 40), (165, SCREEN_HEIGHT-38, 50, 35))
        pygame.draw.circle(surf, (200, 180, 100), (190, SCREEN_HEIGHT-20), 4)
        
        # BOTTOM RIGHT DOOR - Classroom
        pygame.draw.rect(surf, (100, 80, 60), (360, SCREEN_HEIGHT-40, 60, 40))
        pygame.draw.rect(surf, (80, 60, 40), (365, SCREEN_HEIGHT-38, 50, 35))
        pygame.draw.circle(surf, (200, 180, 100), (390, SCREEN_HEIGHT-20), 4)
    
    elif room_name == "Classroom":
        # Classroom - studious atmosphere
        surf.fill((210, 220, 215))
        
        # Floor
        for x in range(0, SCREEN_WIDTH, 48):
            for y in range(SCREEN_HEIGHT//2, SCREEN_HEIGHT, 48):
                color = (180, 185, 180) if (x+y) % 96 == 0 else (190, 195, 190)
                pygame.draw.rect(surf, color, (x, y, 48, 48))
        
        # Wall
        pygame.draw.rect(surf, (170, 190, 180), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT//2))
        
        # Blackboard
        pygame.draw.rect(surf, (40, 60, 50), (150, 50, 340, 120))
        pygame.draw.rect(surf, (80, 100, 90), (155, 55, 330, 110))

        # Door at top (leads back to hall)
        pygame.draw.rect(surf, (100, 80, 60), (SCREEN_WIDTH//2-40, 0, 80, 50))
        pygame.draw.rect(surf, (80, 60, 40), (SCREEN_WIDTH//2-30, 5, 60, 40))
        pygame.draw.circle(surf, (200, 180, 100), (SCREEN_WIDTH//2, 25), 5)
        
        # Desks (non-collidable visual elements)
        for i in range(4):
            for j in range(3):
                x = 80 + i * 120
                y = 240 + j * 70
                pygame.draw.rect(surf, (140, 110, 80), (x, y, 60, 40))
                pygame.draw.rect(surf, (120, 90, 60), (x, y, 60, 40), 2)
    
    elif room_name == "Locker Room":
        # Locker room - metallic and institutional
        surf.fill((200, 205, 210))
        
        # Floor
        for x in range(0, SCREEN_WIDTH, 32):
            for y in range(SCREEN_HEIGHT//2, SCREEN_HEIGHT, 32):
                pygame.draw.rect(surf, (160, 165, 170), (x, y, 32, 32))
                pygame.draw.rect(surf, (140, 145, 150), (x, y, 32, 32), 1)
        
        # Walls
        pygame.draw.rect(surf, (180, 185, 190), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT//2))

        # LEFT DOOR - back to hall
        pygame.draw.rect(surf, (100, 80, 60), (50, 160, 80, 100))
        pygame.draw.rect(surf, (80, 60, 40), (60, 170, 60, 80))
        pygame.draw.circle(surf, (200, 180, 100), (105, 210), 5)
        
        # RIGHT DOOR - to outside
        pygame.draw.rect(surf, (100, 80, 60), (SCREEN_WIDTH-130, 160, 80, 100))
        pygame.draw.rect(surf, (80, 60, 40), (SCREEN_WIDTH-120, 170, 60, 80))
        pygame.draw.circle(surf, (200, 180, 100), (SCREEN_WIDTH-75, 210), 5)
        
        # Lockers on sides
        for side_x in [20, SCREEN_WIDTH-120]:
            for i in range(6):
                y = 40 + i * 60
                pygame.draw.rect(surf, (120, 130, 140), (side_x, y, 100, 55))
                pygame.draw.rect(surf, (100, 110, 120), (side_x, y, 100, 55), 2)
                pygame.draw.circle(surf, (80, 80, 80), (side_x+50, y+30), 4)
    
    elif room_name == "Boys Bathroom":
        # Bathroom - clean but institutional
        surf.fill((210, 220, 225))
        
        # Tile floor
        for x in range(0, SCREEN_WIDTH, 32):
            for y in range(SCREEN_HEIGHT//2, SCREEN_HEIGHT, 32):
                color = WHITE if (x+y) % 64 == 0 else (230, 240, 245)
                pygame.draw.rect(surf, color, (x, y, 32, 32))
                pygame.draw.rect(surf, (200, 210, 215), (x, y, 32, 32), 1)

        # Door at top (leads back to hall)
        pygame.draw.rect(surf, (100, 80, 60), (SCREEN_WIDTH//2-40, 0, 80, 50))
        pygame.draw.rect(surf, (80, 60, 40), (SCREEN_WIDTH//2-30, 5, 60, 40))
        pygame.draw.circle(surf, (200, 180, 100), (SCREEN_WIDTH//2, 25), 5)
        
        # Wall tiles
        for x in range(0, SCREEN_WIDTH, 32):
            for y in range(0, SCREEN_HEIGHT//2, 32):
                pygame.draw.rect(surf, (240, 245, 250), (x, y, 32, 32))
                pygame.draw.rect(surf, (220, 225, 230), (x, y, 32, 32), 1)
        
        # Stalls
        for i in range(3):
            x = 100 + i * 160
            pygame.draw.rect(surf, (200, 180, 170), (x, 100, 100, 120))
            pygame.draw.rect(surf, (180, 160, 150), (x, 100, 100, 120), 3)
    
    elif room_name == "School Buffet":
        # Buffet - warm and inviting
        surf.fill((225, 210, 190))
        
        # Floor
        for x in range(0, SCREEN_WIDTH, 48):
            for y in range(SCREEN_HEIGHT//2, SCREEN_HEIGHT, 48):
                color = (200, 180, 160) if (x+y) % 96 == 0 else (210, 190, 170)
                pygame.draw.rect(surf, color, (x, y, 48, 48))
        
        # Walls
        pygame.draw.rect(surf, (210, 190, 170), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT//2))
        
        # Counter
        pygame.draw.rect(surf, (160, 120, 90), (150, 150, 340, 60))
        pygame.draw.rect(surf, (140, 100, 70), (150, 150, 340, 60), 4)

        # Door on right side (leads back to hall)
        pygame.draw.rect(surf, (100, 80, 60), (SCREEN_WIDTH-130, 160, 80, 100))
        pygame.draw.rect(surf, (80, 60, 40), (SCREEN_WIDTH-120, 170, 60, 80))
        pygame.draw.circle(surf, (200, 180, 100), (SCREEN_WIDTH-75, 210), 5)
        
        # Menu board
        pygame.draw.rect(surf, (80, 60, 40), (200, 40, 240, 80))
        pygame.draw.rect(surf, (100, 80, 60), (210, 50, 220, 60))
    
    elif room_name == "School Yard":
        # Outside - natural and refreshing
        surf.fill((160, 210, 180))
        
        # Grass texture
        for i in range(200):
            x = (i * 37) % SCREEN_WIDTH
            y = (i * 53) % SCREEN_HEIGHT
            pygame.draw.line(surf, (140, 190, 160), (x, y), (x+2, y-5), 1)
        
        # Path
        for x in range(SCREEN_WIDTH//2-80, SCREEN_WIDTH//2+80, 40):
            for y in range(0, SCREEN_HEIGHT, 40):
                pygame.draw.rect(surf, (180, 170, 160), (x, y, 40, 40))
                pygame.draw.rect(surf, (160, 150, 140), (x, y, 40, 40), 1)
        
        # Door on left (leads back to locker room)
        pygame.draw.rect(surf, (100, 80, 60), (50, 160, 80, 100))
        pygame.draw.rect(surf, (80, 60, 40), (60, 170, 60, 80))
        pygame.draw.circle(surf, (200, 180, 100), (105, 210), 5)

        # Sky
        pygame.draw.rect(surf, (180, 220, 240), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT//3))
        
        # Clouds
        for i in range(3):
            x = 100 + i * 200
            y = 40 + (i * 20) % 40
            pygame.draw.ellipse(surf, WHITE, (x, y, 80, 30))
            pygame.draw.ellipse(surf, WHITE, (x+20, y-10, 60, 30))
    
    else:
        surf.fill((200, 200, 200))
    
    return surf

def create_simple_sound(frequency, duration):
    try:
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        buf = []
        for i in range(n_samples):
            value = int(32767 * 0.2 * math.sin(2 * math.pi * frequency * i / sample_rate))
            buf.append([value, value])
        sound = pygame.sndarray.make_sound(buf)
        return sound
    except:
        return None

def load_logo():
    try:
        url = "https://raw.githubusercontent.com/Mykina/Hra-Projekty/main/textury/logo-skoly.png"
        with urllib.request.urlopen(url, timeout=5) as response:
            image_data = response.read()
        image = pygame.image.load(BytesIO(image_data))
        scaled = pygame.transform.scale(image, (300, 100))
        return scaled
    except:
        font = pygame.font.Font(None, 72)
        return font.render("GYMLIT", True, WHITE)

def load_character_sprite(url, size=(PLAYER_SIZE, PLAYER_SIZE)):
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            image_data = response.read()
        image = pygame.image.load(BytesIO(image_data))
        scaled = pygame.transform.scale(image, size)
        return scaled
    except Exception as e:
        print(f"Failed to load sprite from {url}: {e}")
        # Return fallback sprite
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.circle(surf, (200, 100, 100), (size[0]//2, size[1]//2), size[0]//3)
        return surf

# Room data - now includes collision rectangles instead of grid
ROOMS = {
    'hall': {
        'name': "School Hall",
        'spawn': (320, 300),
        'collision_rects': [
            pygame.Rect(0, 0, SCREEN_WIDTH, 140),  # Top wall
            pygame.Rect(0, 0, 40, SCREEN_HEIGHT),  # Left wall
            pygame.Rect(SCREEN_WIDTH-40, 0, 40, SCREEN_HEIGHT),  # Right wall
            pygame.Rect(0, SCREEN_HEIGHT-40, 160, 40),  # Bottom wall left part
            pygame.Rect(300, SCREEN_HEIGHT-40, 60, 40),  # Bottom wall middle part
            pygame.Rect(480, SCREEN_HEIGHT-40, SCREEN_WIDTH-480, 40),  # Bottom wall right part
        ],
        'doors': {
            'buffet': {'rect': pygame.Rect(40, 180, 60, 80), 'target': 'buffet', 'spawn': (540, 240)},
            'locker': {'rect': pygame.Rect(SCREEN_WIDTH-100, 180, 60, 80), 'target': 'locker', 'spawn': (100, 240)},
            'bathroom': {'rect': pygame.Rect(160, SCREEN_HEIGHT-40, 60, 40), 'target': 'bathroom', 'spawn': (240, 120)},
            'classroom': {'rect': pygame.Rect(360, SCREEN_HEIGHT-40, 60, 40), 'target': 'classroom', 'spawn': (320, 120)}
        },
        'npcs': [
            {'id': 'principal', 'x': 320, 'y': 240, 'name': 'Profesorka Rozumova', 'color': (200, 100, 100), 'personality': 'serious', 'sprite_url': 'https://raw.githubusercontent.com/Mykina/Hra-Projekty/main/textury/rozumova%20pixel%20default.png'}
        ]
    },
    'classroom': {
        'name': "Classroom",
        'spawn': (320, 350),
        'collision_rects': [
            pygame.Rect(0, 0, SCREEN_WIDTH, 100),
            pygame.Rect(0, 0, 40, SCREEN_HEIGHT),
            pygame.Rect(SCREEN_WIDTH-40, 0, 40, SCREEN_HEIGHT),
            pygame.Rect(0, SCREEN_HEIGHT-40, SCREEN_WIDTH, 40),
            pygame.Rect(SCREEN_WIDTH//2-40, 100, 80, 10),  # Small wall section above door
        ],
        'doors': {
            'hall': {'rect': pygame.Rect(SCREEN_WIDTH//2-40, 100, 80, 40), 'target': 'hall', 'spawn': (390, 400)}
        },
        'npcs': [
            {'id': 'teacher', 'x': 320, 'y': 220, 'name': 'Profesor Sirl', 'color': (128, 0, 128), 'personality': 'teacher', 'sprite_url': 'https://raw.githubusercontent.com/Mykina/Hra-Projekty/main/textury/sirl%20pixel%20default.png'},
            {'id': 'student1', 'x': 180, 'y': 320, 'name': 'Mlezos', 'color': (100, 180, 100), 'personality': 'friendly', 'sprite_url': 'https://raw.githubusercontent.com/Mykina/Hra-Projekty/main/textury/mlezos%20pixel%20default.png'}
        ]
    },
    'locker': {
        'name': "Locker Room",
        'spawn': (320, 280),
        'collision_rects': [
            pygame.Rect(0, 0, SCREEN_WIDTH, 140),
            pygame.Rect(0, 0, 40, SCREEN_HEIGHT),
            pygame.Rect(SCREEN_WIDTH-40, 0, 40, SCREEN_HEIGHT),
            pygame.Rect(0, SCREEN_HEIGHT-40, SCREEN_WIDTH, 40),
        ],
        'doors': {
            'hall': {'rect': pygame.Rect(40, 180, 60, 80), 'target': 'hall', 'spawn': (540, 240)},
            'outside': {'rect': pygame.Rect(SCREEN_WIDTH-100, 180, 60, 80), 'target': 'outside', 'spawn': (100, 240)}
        },
        'npcs': [
            {'id': 'janitor', 'x': 320, 'y': 280, 'name': 'Pan Skolnik', 'color': (139, 115, 85), 'personality': 'janitor', 'sprite_url': 'https://raw.githubusercontent.com/Mykina/Hra-Projekty/main/textury/mlezos%20pixel%20default.png'}
        ]
    },
    'bathroom': {
        'name': "Boys Bathroom",
        'spawn': (320, 350),
        'collision_rects': [
            pygame.Rect(0, 0, SCREEN_WIDTH, 100),
            pygame.Rect(0, 0, 40, SCREEN_HEIGHT),
            pygame.Rect(SCREEN_WIDTH-40, 0, 40, SCREEN_HEIGHT),
            pygame.Rect(0, SCREEN_HEIGHT-40, SCREEN_WIDTH, 40),
            pygame.Rect(SCREEN_WIDTH//2-40, 100, 80, 10),
        ],
        'doors': {
            'hall': {'rect': pygame.Rect(SCREEN_WIDTH//2-40, 100, 80, 40), 'target': 'hall', 'spawn': (210, 400)}
        },
        'npcs': [
            {'id': 'student2', 'x': 200, 'y': 300, 'name': 'Rossi', 'color': (240, 220, 100), 'personality': 'normal', 'sprite_url': 'https://raw.githubusercontent.com/Mykina/Hra-Projekty/main/textury/rosy-fein%20pixel%20default.png'}
        ]
    },
    'buffet': {
        'name': "School Buffet",
        'spawn': (320, 320),
        'collision_rects': [
            pygame.Rect(0, 0, SCREEN_WIDTH, 140),
            pygame.Rect(0, 0, 40, SCREEN_HEIGHT),
            pygame.Rect(SCREEN_WIDTH-40, 0, 40, SCREEN_HEIGHT),
            pygame.Rect(0, SCREEN_HEIGHT-40, SCREEN_WIDTH, 40),
            pygame.Rect(150, 200, 340, 50),  # Counter
        ],
        'doors': {
            'hall': {'rect': pygame.Rect(SCREEN_WIDTH-100, 180, 60, 80), 'target': 'hall', 'spawn': (100, 240)}
        },
        'npcs': [
            {'id': 'shopkeeper', 'x': 320, 'y': 220, 'name': 'GOAT', 'color': (255, 180, 200), 'personality': 'friendly', 'sprite_url': 'https://raw.githubusercontent.com/Mykina/Hra-Projekty/main/textury/rozumova%20pixel%20default.png'}
        ]
    },
    'outside': {
        'name': "School Yard",
        'spawn': (320, 280),
        'collision_rects': [
            pygame.Rect(0, 0, SCREEN_WIDTH, 100),
            pygame.Rect(0, 0, 40, SCREEN_HEIGHT),
            pygame.Rect(SCREEN_WIDTH-40, 0, 40, SCREEN_HEIGHT),
            pygame.Rect(0, SCREEN_HEIGHT-40, SCREEN_WIDTH, 40),
        ],
        'doors': {
            'locker': {'rect': pygame.Rect(40, 180, 60, 80), 'target': 'locker', 'spawn': (540, 280)}
        },
        'npcs': [
            {'id': 'student3', 'x': 400, 'y': 280, 'name': 'Chris', 'color': (100, 160, 220), 'personality': 'friendly', 'sprite_url': None}
        ]
    }
}

# Dialogue trees (unchanged)
DIALOGUES = {
    'principal': {
        'greeting': {
            'text': "Welcome to Gymlit High! I'm Profesorka Rozumova. How can I help you today?",
            'choices': [
                {'text': "What should I do here?", 'next': 'help'},
                {'text': "I'm looking for something to do.", 'next': 'quest'},
                {'text': "Just exploring, thanks!", 'next': 'bye'}
            ]
        },
        'help': {
            'text': "Explore the school, talk to teachers and students. Press E to interact!",
            'choices': [{'text': "Got it, thanks!", 'next': 'bye'}]
        },
        'quest': {
            'text': "I lost my keys somewhere in the school. Can you find them?",
            'choices': [
                {'text': "Sure, I'll look for them!", 'next': 'accept_quest', 'item': 'Quest: Find Keys'},
                {'text': "Maybe later.", 'next': 'bye'}
            ]
        },
        'accept_quest': {
            'text': "Thank you! Check the locker room. The janitor might have seen them.",
            'choices': [{'text': "I'll find them!", 'next': None}]
        },
        'bye': {
            'text': "Have a great day!",
            'choices': [{'text': "You too!", 'next': None}]
        }
    },
    'teacher': {
        'greeting': {
            'text': "Hello there! I'm Profesor Sirl. Ready to learn something new?",
            'choices': [
                {'text': "What do you teach?", 'next': 'subject'},
                {'text': "Any homework for me?", 'next': 'homework'},
                {'text': "Just passing through!", 'next': 'bye'}
            ]
        },
        'subject': {
            'text': "I teach mathematics! Numbers are everywhere, you know.",
            'choices': [
                {'text': "Cool! Math is fun!", 'next': 'bye'},
                {'text': "Not my favorite subject...", 'next': 'encourage'}
            ]
        },
        'homework': {
            'text': "Here's a textbook for you. Study hard!",
            'choices': [{'text': "Thanks, I'll read it!", 'next': 'bye', 'item': 'Math Textbook'}]
        },
        'encourage': {
            'text': "Give it a chance! Math can be really rewarding once you get into it.",
            'choices': [{'text': "I'll try!", 'next': 'bye'}]
        },
        'bye': {
            'text': "Good luck with your studies!",
            'choices': [{'text': "Thanks!", 'next': None}]
        }
    },
    'student1': {
        'greeting': {
            'text': "Hey! I'm Mlezos. New here?",
            'choices': [
                {'text': "Yeah, just started!", 'next': 'advice'},
                {'text': "Just exploring.", 'next': 'cool'}
            ]
        },
        'advice': {
            'text': "Pro tip: Stay on the teachers' good side and you'll have an easier time!",
            'choices': [{'text': "Good to know!", 'next': 'bye'}]
        },
        'cool': {
            'text': "Cool! Let me know if you need to know where anything is.",
            'choices': [{'text': "Will do!", 'next': 'bye'}]
        },
        'bye': {
            'text': "Catch you later!",
            'choices': [{'text': "See ya!", 'next': None}]
        }
    },
    'janitor': {
        'greeting': {
            'text': "Hey kid, I'm Pan Skolnik. Need something?",
            'choices': [
                {'text': "Have you seen any keys?", 'next': 'keys'},
                {'text': "Just looking around.", 'next': 'bye'}
            ]
        },
        'keys': {
            'text': "Keys? Yeah, found some by the lockers earlier. Here you go!",
            'choices': [{'text': "Perfect! Thanks so much!", 'next': 'bye', 'item': "Principal's Keys"}]
        },
        'bye': {
            'text': "Keep the place clean, alright?",
            'choices': [{'text': "Will do!", 'next': None}]
        }
    },
    'student2': {
        'greeting': {
            'text': "Oh hey... I'm Rossi. What's up?",
            'choices': [
                {'text': "How's it going?", 'next': 'ok'},
                {'text': "Nothing much.", 'next': 'bye'}
            ]
        },
        'ok': {
            'text': "Pretty good. Just trying to avoid the next test, you know?",
            'choices': [
                {'text': "Haha, I feel that!", 'next': 'laugh'},
                {'text': "You should study!", 'next': 'study'}
            ]
        },
        'laugh': {
            'text': "Right? School can be rough sometimes. But we'll make it through!",
            'choices': [{'text': "Definitely!", 'next': 'bye'}]
        },
        'study': {
            'text': "Yeah, yeah... I know. Maybe I will.",
            'choices': [{'text': "Good luck!", 'next': 'bye'}]
        },
        'bye': {
            'text': "Later!",
            'choices': [{'text': "Bye!", 'next': None}]
        }
    },
    'shopkeeper': {
        'greeting': {
            'text': "Welcome to the buffet! Want to buy a toast?",
            'choices': [
                {'text': "Yes please!", 'next': 'buy'},
                {'text': "Maybe later.", 'next': 'bye'}
            ]
        },
        'buy': {
            'text': "Here you go! That'll be 5 coins. Enjoy!",
            'choices': [{'text': "Thanks!", 'next': 'bye', 'item': 'Toast'}]
        },
        'bye': {
            'text': "Come back anytime!",
            'choices': [{'text': "Will do!", 'next': None}]
        }
    },
    'student3': {
        'greeting': {
            'text': "Nice day outside, isn't it?",
            'choices': [
                {'text': "Yeah, it's great!", 'next': 'weather'},
                {'text': "Just taking a break.", 'next': 'bye'}
            ]
        },
        'weather': {
            'text': "Way better than being stuck inside all day!",
            'choices': [{'text': "True that!", 'next': 'bye'}]
        },
        'bye': {
            'text': "See you around!",
            'choices': [{'text': "Later!", 'next': None}]
        }
    }
}

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("GYMLIT - School RPG")
        self.clock = pygame.time.Clock()
        self.running = True
        self.in_menu = True
        
        # Load sounds
        self.sounds = {
            'door': create_simple_sound(440, 0.1),
            'select': create_simple_sound(880, 0.05)
        }
        
        # Load logo
        self.logo = load_logo()

        # Load character sprites
        self.david_idle = load_character_sprite('https://raw.githubusercontent.com/Mykina/Hra-Projekty/main/textury/david%20pixel%20default.png')
        self.david_walk1 = load_character_sprite('https://raw.githubusercontent.com/Mykina/Hra-Projekty/main/textury/david%20pixel%20walking1.png')
        self.david_walk2 = load_character_sprite('https://raw.githubusercontent.com/Mykina/Hra-Projekty/main/textury/david%20pixel%20walking2.png')
        
        # Load NPC sprites
        self.npc_sprite_cache = {}
        for room_key, room_data in ROOMS.items():
            for npc in room_data['npcs']:
                if npc.get('sprite_url'):
                    self.npc_sprite_cache[npc['id']] = load_character_sprite(npc['sprite_url'], (NPC_SIZE, NPC_SIZE))
        
        # Load room backgrounds
        self.room_backgrounds = {}
        for room_key, room_data in ROOMS.items():
            self.room_backgrounds[room_key] = create_room_background(room_data['name'])
        
        # Player state - smooth movement
        self.player_x = 320.0
        self.player_y = 350.0
        self.player_target_x = 320.0
        self.player_target_y = 350.0
        self.current_room = 'hall'
        self.animation_frame = 0
        self.is_moving = False
        
        # Game state
        self.inventory = []
        self.npc_states = {}
        self.dialogue_active = False
        self.current_dialogue = None
        self.current_npc = None
        self.selected_choice = 0
        self.show_inventory = False
        
        # NPC sprites cache
        self.npc_sprites = {}
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        self.font_tiny = pygame.font.Font(None, 14)
        
        # Menu state
        self.menu_buttons = [
            {'text': 'START GAME', 'y': 280},
            {'text': 'CONTROLS', 'y': 340}
        ]
        self.menu_selected = 0
        self.show_controls = False
    
    def play_sound(self, sound_name):
        if self.sounds.get(sound_name):
            try:
                self.sounds[sound_name].play()
            except:
                pass
    
    def get_player_rect(self):
        return pygame.Rect(self.player_x - PLAYER_SIZE//2, self.player_y - PLAYER_SIZE//2, 
                          PLAYER_SIZE, PLAYER_SIZE)
    
    def check_collision(self, x, y):
        test_rect = pygame.Rect(x - PLAYER_SIZE//2, y - PLAYER_SIZE//2, PLAYER_SIZE, PLAYER_SIZE)
        room = ROOMS[self.current_room]
        
        # Check room boundaries
        for rect in room['collision_rects']:
            if test_rect.colliderect(rect):
                return True
        
        # Check NPC collision
        for npc in room['npcs']:
            npc_rect = pygame.Rect(npc['x'] - NPC_SIZE//2, npc['y'] - NPC_SIZE//2, 
                                  NPC_SIZE, NPC_SIZE)
            if test_rect.colliderect(npc_rect):
                return True
        
        return False
    
    def get_nearby_npc(self):
        room = ROOMS[self.current_room]
        player_rect = self.get_player_rect()
        
        for npc in room['npcs']:
            npc_rect = pygame.Rect(npc['x'] - NPC_SIZE//2, npc['y'] - NPC_SIZE//2, 
                                  NPC_SIZE, NPC_SIZE)
            # Check if player is near NPC (within 80 pixels)
            distance = math.sqrt((self.player_x - npc['x'])**2 + (self.player_y - npc['y'])**2)
            if distance < 80:
                return npc
        return None
    
    def check_door_transition(self):
        room = ROOMS[self.current_room]
        player_rect = self.get_player_rect()
        
        for door_data in room['doors'].values():
            if player_rect.colliderect(door_data['rect']):
                self.current_room = door_data['target']
                spawn = door_data['spawn']
                self.player_x = float(spawn[0])
                self.player_y = float(spawn[1])
                self.player_target_x = self.player_x
                self.player_target_y = self.player_y
                self.play_sound('door')
                return True
        return False
    
    def start_dialogue(self, npc):
        self.current_npc = npc
        state = self.npc_states.get(npc['id'], 'greeting')
        self.current_dialogue = DIALOGUES[npc['id']][state]
        self.dialogue_active = True
        self.selected_choice = 0
    
    def handle_choice(self, choice):
        if 'item' in choice:
            self.inventory.append(choice['item'])
        
        if choice['next']:
            state = choice['next']
            self.current_dialogue = DIALOGUES[self.current_npc['id']][state]
            self.npc_states[self.current_npc['id']] = state
            self.selected_choice = 0
        else:
            self.dialogue_active = False
            self.current_dialogue = None
            self.current_npc = None
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                # Menu controls
                if self.in_menu:
                    if self.show_controls:
                        self.show_controls = False
                        self.play_sound('select')
                    else:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.menu_selected = max(0, self.menu_selected - 1)
                            self.play_sound('select')
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.menu_selected = min(len(self.menu_buttons) - 1, self.menu_selected + 1)
                            self.play_sound('select')
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_e:
                            if self.menu_selected == 0:
                                self.in_menu = False
                                self.play_sound('door')
                            elif self.menu_selected == 1:
                                self.show_controls = True
                                self.play_sound('select')
                    return
                
                # Inventory toggle
                if event.key == pygame.K_i:
                    if not self.dialogue_active:
                        self.show_inventory = not self.show_inventory
                        self.play_sound('select')
                
                # Escape key
                if event.key == pygame.K_ESCAPE:
                    if self.dialogue_active:
                        self.dialogue_active = False
                        self.play_sound('select')
                    elif self.show_inventory:
                        self.show_inventory = False
                        self.play_sound('select')
                
                # Dialogue controls
                if self.dialogue_active:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selected_choice = max(0, self.selected_choice - 1)
                        self.play_sound('select')
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selected_choice = min(len(self.current_dialogue['choices']) - 1, 
                                                   self.selected_choice + 1)
                        self.play_sound('select')
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_e:
                        self.handle_choice(self.current_dialogue['choices'][self.selected_choice])
                        self.play_sound('select')
                
                # Interaction
                elif not self.show_inventory:
                    if event.key == pygame.K_e or event.key == pygame.K_RETURN:
                        npc = self.get_nearby_npc()
                        if npc:
                            self.start_dialogue(npc)
                            self.play_sound('select')
    
    def update(self):
        if self.in_menu or self.dialogue_active or self.show_inventory:
            return
        
        self.animation_frame += 1
        
        # Smooth movement
        keys = pygame.key.get_pressed()
        
        move_x = 0
        move_y = 0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move_y = -MOVE_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move_y = MOVE_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_x = -MOVE_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_x = MOVE_SPEED
        
        # Normalize diagonal movement
        if move_x != 0 and move_y != 0:
            move_x *= 0.707
            move_y *= 0.707
        
        self.is_moving = move_x != 0 or move_y != 0
        
        # Try to move
        if move_x != 0:
            new_x = self.player_x + move_x
            if not self.check_collision(new_x, self.player_y):
                self.player_x = new_x
        
        if move_y != 0:
            new_y = self.player_y + move_y
            if not self.check_collision(self.player_x, new_y):
                self.player_y = new_y
        
        # Check for door transitions
        self.check_door_transition()
    
    def draw_room(self):
        # Draw background
        self.screen.blit(self.room_backgrounds[self.current_room], (0, 0))
    
    def draw_npcs(self):
        room = ROOMS[self.current_room]
        for npc in room['npcs']:
            # Use cached sprite if available
            if npc['id'] in self.npc_sprite_cache:
                sprite = self.npc_sprite_cache[npc['id']]
            else:
                # Only create generated sprite if no custom sprite URL exists
                if npc.get('sprite_url') is None:
                    cache_key = f"{npc['id']}_{self.animation_frame // 10}"
                    if cache_key not in self.npc_sprites:
                        self.npc_sprites[cache_key] = create_npc_sprite(
                            npc['color'], 
                            npc.get('personality', 'normal'),
                            self.animation_frame
                        )
                    sprite = self.npc_sprites[cache_key]
                else:
                    # Skip if sprite URL exists but failed to load
                    continue
            
            # Draw NPC
            self.screen.blit(sprite, (npc['x'] - NPC_SIZE//2, npc['y'] - NPC_SIZE//2))
            
            # Draw name tag with better styling
            name_width = len(npc['name']) * 7 + 10
            name_bg = pygame.Rect(npc['x'] - name_width//2, npc['y'] - NPC_SIZE//2 - 18, 
                                 name_width, 16)
            
            # Draw shadow
            shadow_rect = name_bg.copy()
            shadow_rect.x += 2
            shadow_rect.y += 2
            s = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
            s.fill((0, 0, 0, 100))
            self.screen.blit(s, shadow_rect)
            
            # Draw name background
            pygame.draw.rect(self.screen, DARK_PURPLE, name_bg)
            pygame.draw.rect(self.screen, WHITE, name_bg, 1)
            
            # Draw name text
            name_text = self.font_tiny.render(npc['name'], True, WHITE)
            text_x = npc['x'] - name_text.get_width()//2
            text_y = npc['y'] - NPC_SIZE//2 - 16
            self.screen.blit(name_text, (text_x, text_y))
            
            # Draw interaction prompt if nearby
            distance = math.sqrt((self.player_x - npc['x'])**2 + (self.player_y - npc['y'])**2)
            if distance < 80:
                prompt = self.font_tiny.render("[E] Talk", True, WHITE)
                prompt_bg = pygame.Rect(npc['x'] - 30, npc['y'] + NPC_SIZE//2 + 5, 60, 16)
                pygame.draw.rect(self.screen, (0, 0, 0, 150), prompt_bg)
                self.screen.blit(prompt, (npc['x'] - prompt.get_width()//2, npc['y'] + NPC_SIZE//2 + 6))
    
    def draw_player(self):
        # Use David's sprites with walking animation
        if self.is_moving:
            # Alternate between walk1 and walk2
            if (self.animation_frame // 10) % 2 == 0:
                player_sprite = self.david_walk1
            else:
                player_sprite = self.david_walk2
        else:
            player_sprite = self.david_idle
        
        self.screen.blit(player_sprite, (self.player_x - PLAYER_SIZE//2, self.player_y - PLAYER_SIZE//2))
    
    def draw_ui(self):
        # Room name with better styling
        room_name = self.font_medium.render(ROOMS[self.current_room]['name'], True, WHITE)
        bg_width = room_name.get_width() + 30
        bg_rect = pygame.Rect(10, 10, bg_width, 45)
        
        # Shadow
        shadow = pygame.Surface((bg_width, 45), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 100))
        self.screen.blit(shadow, (12, 12))
        
        # Background
        pygame.draw.rect(self.screen, DARK_PURPLE, bg_rect)
        pygame.draw.rect(self.screen, SOFT_YELLOW, bg_rect, 2)
        
        # Text
        self.screen.blit(room_name, (25, 22))
        
        # Inventory button with better styling
        inv_text = f"Bag ({len(self.inventory)})"
        inv_surface = self.font_small.render(inv_text, True, WHITE)
        inv_bg = pygame.Rect(SCREEN_WIDTH - 120, 10, 110, 40)
        
        # Shadow
        shadow = pygame.Surface((110, 40), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 100))
        self.screen.blit(shadow, (SCREEN_WIDTH - 118, 12))
        
        # Background
        pygame.draw.rect(self.screen, DARK_PURPLE, inv_bg)
        pygame.draw.rect(self.screen, SOFT_YELLOW, inv_bg, 2)
        
        # Text
        self.screen.blit(inv_surface, (SCREEN_WIDTH - 110, 20))
        
        # Small hint
        hint = self.font_tiny.render("[I] to open", True, (200, 200, 200))
        self.screen.blit(hint, (SCREEN_WIDTH - 115, 35))
    
    def draw_dialogue(self):
        if not self.dialogue_active:
            return
        
        # Dialogue box with Omori-style design
        dialog_height = 180
        dialog_rect = pygame.Rect(20, SCREEN_HEIGHT - dialog_height - 20, SCREEN_WIDTH - 40, dialog_height)
        
        # Shadow
        shadow = pygame.Surface((SCREEN_WIDTH - 40, dialog_height), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 150))
        self.screen.blit(shadow, (22, SCREEN_HEIGHT - dialog_height - 18))
        
        # Main box
        pygame.draw.rect(self.screen, DARK_PURPLE, dialog_rect)
        pygame.draw.rect(self.screen, WHITE, dialog_rect, 3)
        
        # Inner decoration
        inner_rect = dialog_rect.inflate(-20, -20)
        pygame.draw.rect(self.screen, LIGHT_PURPLE, inner_rect, 1)
        
        # NPC name with colored background
        name_text = self.current_npc['name']
        name_surface = self.font_medium.render(name_text, True, WHITE)
        name_bg = pygame.Rect(40, dialog_rect.y - 18, name_surface.get_width() + 20, 30)
        pygame.draw.rect(self.screen, self.current_npc['color'], name_bg)
        pygame.draw.rect(self.screen, WHITE, name_bg, 2)
        self.screen.blit(name_surface, (50, dialog_rect.y - 14))
        
        # Dialogue text with word wrap
        text = self.current_dialogue['text']
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if self.font_small.size(test_line)[0] < SCREEN_WIDTH - 100:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        
        y_offset = dialog_rect.y + 20
        for line in lines[:2]:  # Max 2 lines
            text_surface = self.font_small.render(line, True, WHITE)
            self.screen.blit(text_surface, (40, y_offset))
            y_offset += 25
        
        # Choices with better styling
        y_offset = dialog_rect.y + 80
        for i, choice in enumerate(self.current_dialogue['choices']):
            is_selected = i == self.selected_choice
            
            # Choice background
            choice_bg = pygame.Rect(40, y_offset - 5, SCREEN_WIDTH - 100, 30)
            if is_selected:
                pygame.draw.rect(self.screen, SOFT_YELLOW, choice_bg)
                pygame.draw.rect(self.screen, WHITE, choice_bg, 2)
                text_color = DARK_PURPLE
            else:
                pygame.draw.rect(self.screen, LIGHT_PURPLE, choice_bg)
                text_color = WHITE
            
            # Choice text
            choice_text = f"> {choice['text']}" if is_selected else f"  {choice['text']}"
            choice_surface = self.font_small.render(choice_text, True, text_color)
            self.screen.blit(choice_surface, (50, y_offset))
            y_offset += 35
        
        # Help text
        help_text = "W/S: Navigate  |  E: Select  |  ESC: Close"
        help_surface = self.font_tiny.render(help_text, True, (180, 180, 200))
        self.screen.blit(help_surface, (40, dialog_rect.bottom - 25))
    
    def draw_inventory_screen(self):
        if not self.show_inventory:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 20, 40, 230))
        self.screen.blit(overlay, (0, 0))
        
        # Title with decoration
        title = self.font_large.render("INVENTORY", True, SOFT_YELLOW)
        title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
        self.screen.blit(title, (title_x, 40))
        
        # Underline
        pygame.draw.line(self.screen, SOFT_YELLOW, (title_x, 85), 
                        (title_x + title.get_width(), 85), 2)
        
        # Items
        if not self.inventory:
            empty_text = self.font_medium.render("Your bag is empty.", True, (180, 180, 200))
            self.screen.blit(empty_text, (SCREEN_WIDTH // 2 - empty_text.get_width() // 2, 180))
            hint_text = self.font_small.render("Talk to people to collect items!", True, (150, 150, 170))
            self.screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, 220))
        else:
            y_pos = 120
            for item in self.inventory:
                # Item card
                item_rect = pygame.Rect(100, y_pos, SCREEN_WIDTH - 200, 60)
                
                # Shadow
                shadow_rect = item_rect.copy()
                shadow_rect.x += 3
                shadow_rect.y += 3
                s = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
                s.fill((0, 0, 0, 120))
                self.screen.blit(s, shadow_rect)
                
                # Card background
                pygame.draw.rect(self.screen, LIGHT_PURPLE, item_rect)
                pygame.draw.rect(self.screen, SOFT_YELLOW, item_rect, 2)
                
                # Item text
                item_text = self.font_medium.render(item, True, WHITE)
                self.screen.blit(item_text, (120, y_pos + 20))
                y_pos += 75
        
        # Close button
        close_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, 420, 160, 40)
        pygame.draw.rect(self.screen, SOFT_RED, close_rect)
        pygame.draw.rect(self.screen, WHITE, close_rect, 2)
        close_text = self.font_small.render("Press I or ESC", True, WHITE)
        self.screen.blit(close_text, (SCREEN_WIDTH // 2 - close_text.get_width() // 2, 430))
    
    def draw_menu(self):
        # Gradient background
        for y in range(SCREEN_HEIGHT):
            color_val = int(20 + (y / SCREEN_HEIGHT) * 40)
            pygame.draw.line(self.screen, (color_val, color_val//2, color_val), 
                           (0, y), (SCREEN_WIDTH, y))
        
        if self.show_controls:
            # Controls screen
            title = self.font_large.render("CONTROLS", True, SOFT_YELLOW)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
            
            controls = [
                ("WASD / Arrow Keys", "Move around"),
                ("E / Enter", "Interact / Select"),
                ("I", "Open Inventory"),
                ("ESC", "Close menus"),
                ("", ""),
                ("", "Press any key to go back")
            ]
            
            y = 150
            for label, desc in controls:
                if label:
                    label_surf = self.font_medium.render(label, True, SOFT_YELLOW)
                    desc_surf = self.font_small.render(desc, True, WHITE)
                    self.screen.blit(label_surf, (150, y))
                    self.screen.blit(desc_surf, (150, y + 25))
                else:
                    desc_surf = self.font_small.render(desc, True, (180, 180, 200))
                    self.screen.blit(desc_surf, (SCREEN_WIDTH // 2 - desc_surf.get_width() // 2, y))
                y += 50
        else:
            # Main menu
            # Logo
            logo_x = SCREEN_WIDTH // 2 - self.logo.get_width() // 2
            self.screen.blit(self.logo, (logo_x, 80))
            
            # Subtitle
            subtitle = self.font_medium.render("A School RPG Adventure", True, SOFT_BLUE)
            self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 200))
            
            # Menu buttons
            for i, button in enumerate(self.menu_buttons):
                is_selected = i == self.menu_selected
                
                button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, button['y'] - 10, 240, 50)
                
                if is_selected:
                    # Selected button
                    pygame.draw.rect(self.screen, SOFT_YELLOW, button_rect)
                    pygame.draw.rect(self.screen, WHITE, button_rect, 3)
                    text_color = DARK_PURPLE
                else:
                    # Unselected button
                    pygame.draw.rect(self.screen, DARK_PURPLE, button_rect)
                    pygame.draw.rect(self.screen, LIGHT_PURPLE, button_rect, 2)
                    text_color = WHITE
                
                text = button['text']
                surf = self.font_medium.render(text, True, text_color)
                text_x = SCREEN_WIDTH // 2 - surf.get_width() // 2
                self.screen.blit(surf, (text_x, button['y'] + 5))
            
            # Hint
            hint = self.font_tiny.render("W/S: Navigate  |  Enter: Select", True, (150, 150, 170))
            self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 420))
    
    def draw(self):
        if self.in_menu:
            self.draw_menu()
        else:
            self.draw_room()
            self.draw_npcs()
            self.draw_player()
            self.draw_ui()
            self.draw_dialogue()
            self.draw_inventory_screen()
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()