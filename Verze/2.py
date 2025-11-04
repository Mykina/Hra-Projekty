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
TILE_SIZE = 32
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (74, 74, 74)
DARK_GRAY = (42, 42, 42)
LIGHT_GRAY = (150, 150, 150)
BROWN = (139, 115, 85)
DARK_BROWN = (101, 67, 33)
BLUE = (52, 152, 219)
DARK_BLUE = (41, 128, 185)
YELLOW = (241, 196, 15)
RED = (231, 76, 60)
GREEN = (46, 204, 113)
BEIGE = (210, 180, 140)
LIGHT_BLUE = (173, 216, 230)
DARK_GREEN = (34, 139, 34)
GRASS = (124, 252, 0)
DIALOG_BG = (20, 20, 20)

# Texture creation functions
def create_player_texture():
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    # Body
    pygame.draw.rect(surf, BLUE, (8, 10, 16, 18))
    # Head
    pygame.draw.circle(surf, BEIGE, (16, 8), 6)
    # Eyes
    pygame.draw.rect(surf, BLACK, (13, 6, 2, 2))
    pygame.draw.rect(surf, BLACK, (19, 6, 2, 2))
    # Legs
    pygame.draw.rect(surf, DARK_BLUE, (10, 28, 5, 4))
    pygame.draw.rect(surf, DARK_BLUE, (17, 28, 5, 4))
    return surf

def create_npc_texture(color):
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    # Body
    pygame.draw.rect(surf, color, (8, 10, 16, 18))
    # Head
    pygame.draw.circle(surf, BEIGE, (16, 8), 6)
    # Eyes
    pygame.draw.rect(surf, BLACK, (13, 6, 2, 2))
    pygame.draw.rect(surf, BLACK, (19, 6, 2, 2))
    # Legs
    darker = (max(0, color[0]-20), max(0, color[1]-20), max(0, color[2]-20))
    pygame.draw.rect(surf, darker, (10, 28, 5, 4))
    pygame.draw.rect(surf, darker, (17, 28, 5, 4))
    return surf

def create_wall_texture():
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surf.fill(BROWN)
    # Brick pattern
    for i in range(0, TILE_SIZE, 8):
        pygame.draw.line(surf, DARK_BROWN, (0, i), (TILE_SIZE, i), 2)
    for i in range(0, TILE_SIZE, 16):
        pygame.draw.line(surf, DARK_BROWN, (i, 0), (i, TILE_SIZE), 2)
    return surf

def create_floor_texture():
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surf.fill(LIGHT_GRAY)
    pygame.draw.rect(surf, GRAY, (2, 2, TILE_SIZE-4, TILE_SIZE-4), 1)
    return surf

def create_door_texture():
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surf.fill(DARK_BROWN)
    pygame.draw.rect(surf, (80, 50, 20), (4, 4, TILE_SIZE-8, TILE_SIZE-8))
    pygame.draw.circle(surf, YELLOW, (24, 16), 3)
    return surf

def create_desk_texture():
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surf.fill(BROWN)
    pygame.draw.rect(surf, DARK_BROWN, (2, 2, TILE_SIZE-4, TILE_SIZE-4))
    return surf

def create_urinal_texture():
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surf.fill(LIGHT_GRAY)
    pygame.draw.ellipse(surf, WHITE, (8, 8, 16, 20))
    pygame.draw.circle(surf, LIGHT_BLUE, (16, 12), 3)
    return surf

def create_locker_texture():
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surf.fill(GRAY)
    pygame.draw.rect(surf, DARK_GRAY, (4, 4, TILE_SIZE-8, TILE_SIZE-8))
    pygame.draw.circle(surf, BLACK, (16, 16), 2)
    return surf

def create_counter_texture():
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surf.fill((160, 82, 45))
    pygame.draw.rect(surf, (139, 69, 19), (2, 2, TILE_SIZE-4, TILE_SIZE-4))
    return surf

def create_grass_texture():
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surf.fill(GRASS)
    for i in range(5):
        x = (i * 7) % TILE_SIZE
        y = (i * 11) % TILE_SIZE
        pygame.draw.line(surf, DARK_GREEN, (x, y), (x+2, y-4), 1)
    return surf

def create_tree_texture():
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    # Trunk
    pygame.draw.rect(surf, DARK_BROWN, (12, 16, 8, 16))
    # Leaves
    pygame.draw.circle(surf, GREEN, (16, 12), 12)
    pygame.draw.circle(surf, DARK_GREEN, (16, 12), 12, 2)
    return surf

def create_fence_texture():
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surf.fill(GRASS)
    pygame.draw.rect(surf, DARK_BROWN, (0, 12, TILE_SIZE, 8))
    pygame.draw.rect(surf, DARK_BROWN, (8, 8, 4, 16))
    pygame.draw.rect(surf, DARK_BROWN, (20, 8, 4, 16))
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
        # Fallback text logo
        font = pygame.font.Font(None, 72)
        return font.render("GYMLIT", True, WHITE)

# Room layouts (0 = floor, 1 = wall, 2 = door, 3 = desk, 4 = locker, 5 = urinal, 6 = counter, 7 = fence, 8 = tree)
ROOMS = {
    'hall': {
        'name': "School Hall",
        'layout': [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,2,2,1,1,2,2,1,1,1,1,1,1,1]
        ],
        'doors': {
            'buffet': {'x': 1, 'y': 7, 'target_x': 18, 'target_y': 7},
            'locker': {'x': 18, 'y': 7, 'target_x': 1, 'target_y': 7},
            'bathroom': {'x': 7, 'y': 14, 'target_x': 7, 'target_y': 1},
            'classroom': {'x': 11, 'y': 14, 'target_x': 10, 'target_y': 1}
        },
        'npcs': [
            {'id': 'principal', 'x': 10, 'y': 3, 'name': 'Principal Smith', 'color': RED}
        ]
    },
    'classroom': {
        'name': "Classroom",
        'layout': [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1],
            [1,0,3,3,0,0,3,3,0,0,0,0,0,3,3,0,0,3,3,1],
            [1,0,3,3,0,0,3,3,0,0,0,0,0,3,3,0,0,3,3,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,3,3,0,0,3,3,0,0,0,0,0,3,3,0,0,3,3,1],
            [1,0,3,3,0,0,3,3,0,0,0,0,0,3,3,0,0,3,3,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,3,3,0,0,3,3,0,0,0,0,0,3,3,0,0,3,3,1],
            [1,0,3,3,0,0,3,3,0,0,0,0,0,3,3,0,0,3,3,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ],
        'doors': {
            'hall': {'x': 10, 'y': 1, 'target_x': 11, 'target_y': 14}
        },
        'npcs': [
            {'id': 'teacher', 'x': 10, 'y': 4, 'name': 'Ms. Johnson', 'color': (128, 0, 128)},
            {'id': 'student1', 'x': 3, 'y': 5, 'name': 'Alex', 'color': GREEN}
        ]
    },
    'locker': {
        'name': "Locker Room",
        'layout': [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,4,4,4,0,0,0,0,0,0,0,0,0,0,4,4,4,0,1],
            [1,0,4,4,4,0,0,0,0,0,0,0,0,0,0,4,4,4,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,4,4,4,0,0,0,0,0,0,0,0,0,0,4,4,4,0,1],
            [1,0,4,4,4,0,0,0,0,0,0,0,0,0,0,4,4,4,0,1],
            [1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,4,4,4,0,0,0,0,0,0,0,0,0,0,4,4,4,0,1],
            [1,0,4,4,4,0,0,0,0,0,0,0,0,0,0,4,4,4,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ],
        'doors': {
            'hall': {'x': 1, 'y': 7, 'target_x': 18, 'target_y': 7},
            'outside': {'x': 18, 'y': 13, 'target_x': 1, 'target_y': 7}
        },
        'npcs': [
            {'id': 'janitor', 'x': 10, 'y': 7, 'name': 'Mr. Rodriguez', 'color': BROWN}
        ]
    },
    'bathroom': {
        'name': "Boys Bathroom",
        'layout': [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,0,0,0,0,0,5,5,5,0,0,1,1,1,1],
            [1,0,1,1,1,0,0,0,0,0,0,5,5,5,0,0,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,0,0,0,0,0,5,5,5,0,0,1,1,1,1],
            [1,0,1,1,1,0,0,0,0,0,0,5,5,5,0,0,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,0,0,0,0,0,5,5,5,0,0,1,1,1,1],
            [1,0,1,1,1,0,0,0,0,0,0,5,5,5,0,0,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ],
        'doors': {
            'hall': {'x': 7, 'y': 1, 'target_x': 7, 'target_y': 14}
        },
        'npcs': [
            {'id': 'student2', 'x': 5, 'y': 7, 'name': 'Jamie', 'color': YELLOW}
        ]
    },
    'buffet': {
        'name': "School Buffet",
        'layout': [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,6,6,6,6,6,6,6,6,6,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ],
        'doors': {
            'hall': {'x': 18, 'y': 7, 'target_x': 1, 'target_y': 7}
        },
        'npcs': [
            {'id': 'shopkeeper', 'x': 10, 'y': 4, 'name': 'Mrs. Baker', 'color': (255, 192, 203)}
        ]
    },
    'outside': {
        'name': "School Yard",
        'layout': [
            [7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],
            [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7],
            [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,7],
            [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7],
            [7,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7],
            [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7],
            [7,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,7],
            [7,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7],
            [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7],
            [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,7],
            [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7],
            [7,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,7],
            [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7],
            [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7],
            [7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]
        ],
        'doors': {
            'locker': {'x': 1, 'y': 7, 'target_x': 18, 'target_y': 13}
        },
        'npcs': [
            {'id': 'student3', 'x': 10, 'y': 7, 'name': 'Chris', 'color': (0, 128, 255)}
        ]
    }
}

# Dialogue trees
DIALOGUES = {
    'principal': {
        'greeting': {
            'text': "Welcome to Gymlit High! How can I help you today?",
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
            'text': "Hello there! I'm Ms. Johnson. Ready to learn something new?",
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
            'text': "Hey! I'm Alex. New here?",
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
            'text': "Hey kid, I'm Mr. Rodriguez. Need something?",
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
            'text': "Oh hey... I'm Jamie. What's up?",
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
        
        # Load textures
        self.textures = {
            'player': create_player_texture(),
            'wall': create_wall_texture(),
            'floor': create_floor_texture(),
            'door': create_door_texture(),
            'desk': create_desk_texture(),
            'urinal': create_urinal_texture(),
            'locker': create_locker_texture(),
            'counter': create_counter_texture(),
            'grass': create_grass_texture(),
            'tree': create_tree_texture(),
            'fence': create_fence_texture()
        }
        
        # Load sounds
        self.sounds = {
            'door': create_simple_sound(440, 0.1),
            'select': create_simple_sound(880, 0.05)
        }
        
        # Load logo
        self.logo = load_logo()
        
        # Player state
        self.player_x = 10
        self.player_y = 10
        self.current_room = 'hall'
        self.move_timer = 0
        self.move_delay = 150
        
        # Game state
        self.inventory = []
        self.npc_states = {}
        self.dialogue_active = False
        self.current_dialogue = None
        self.current_npc = None
        self.selected_choice = 0
        self.show_inventory = False
        
        # NPC textures cache
        self.npc_textures = {}
        
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
    
    def get_nearby_npc(self):
        room = ROOMS[self.current_room]
        for npc in room['npcs']:
            if abs(npc['x'] - self.player_x) <= 1 and abs(npc['y'] - self.player_y) <= 1:
                return npc
        return None
    
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
        
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        
        if current_time - self.move_timer > self.move_delay:
            new_x, new_y = self.player_x, self.player_y
            moved = False
            
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                new_y -= 1
                moved = True
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                new_y += 1
                moved = True
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                new_x -= 1
                moved = True
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                new_x += 1
                moved = True
            
            if moved:
                room = ROOMS[self.current_room]
                layout = room['layout']
                
                # Check bounds
                if 0 <= new_y < len(layout) and 0 <= new_x < len(layout[0]):
                    tile = layout[new_y][new_x]
                    
                    # Wall and obstacle collision
                    if tile in [1, 3, 4, 5, 6, 7, 8]:
                        return
                    
                    # NPC collision
                    npc_collision = any(npc['x'] == new_x and npc['y'] == new_y 
                                       for npc in room['npcs'])
                    if npc_collision:
                        return
                    
                    # Door transition
                    if tile == 2:
                        for target_room, door_data in room['doors'].items():
                            if door_data['x'] == new_x and door_data['y'] == new_y:
                                self.current_room = target_room
                                self.player_x = door_data['target_x']
                                self.player_y = door_data['target_y']
                                self.move_timer = current_time
                                self.play_sound('door')
                                return
                    
                    # Normal move
                    self.player_x = new_x
                    self.player_y = new_y
                    self.move_timer = current_time
    
    def draw_tile(self, tile, x, y):
        pos = (x * TILE_SIZE, y * TILE_SIZE)
        
        if tile == 0:
            self.screen.blit(self.textures['floor'], pos)
        elif tile == 1:
            self.screen.blit(self.textures['wall'], pos)
        elif tile == 2:
            self.screen.blit(self.textures['door'], pos)
        elif tile == 3:
            self.screen.blit(self.textures['desk'], pos)
        elif tile == 4:
            self.screen.blit(self.textures['locker'], pos)
        elif tile == 5:
            self.screen.blit(self.textures['urinal'], pos)
        elif tile == 6:
            self.screen.blit(self.textures['counter'], pos)
        elif tile == 7:
            self.screen.blit(self.textures['fence'], pos)
        elif tile == 8:
            self.screen.blit(self.textures['tree'], pos)
    
    def draw_room(self):
        room = ROOMS[self.current_room]
        layout = room['layout']
        
        for y, row in enumerate(layout):
            for x, tile in enumerate(row):
                self.draw_tile(tile, x, y)
    
    def draw_npcs(self):
        room = ROOMS[self.current_room]
        for npc in room['npcs']:
            # Create NPC texture if not cached
            if npc['id'] not in self.npc_textures:
                self.npc_textures[npc['id']] = create_npc_texture(npc['color'])
            
            # Draw NPC
            self.screen.blit(self.npc_textures[npc['id']], 
                           (npc['x'] * TILE_SIZE, npc['y'] * TILE_SIZE))
            
            # Draw name tag
            name_width = len(npc['name']) * 6
            name_bg = pygame.Rect(npc['x'] * TILE_SIZE - 5, npc['y'] * TILE_SIZE - 12, 
                                 name_width + 6, 10)
            pygame.draw.rect(self.screen, BLACK, name_bg)
            pygame.draw.rect(self.screen, WHITE, name_bg, 1)
            name_text = self.font_tiny.render(npc['name'], True, WHITE)
            self.screen.blit(name_text, (npc['x'] * TILE_SIZE - 3, npc['y'] * TILE_SIZE - 11))
    
    def draw_player(self):
        self.screen.blit(self.textures['player'], 
                        (self.player_x * TILE_SIZE, self.player_y * TILE_SIZE))
    
    def draw_ui(self):
        # Room name
        room_name = self.font_medium.render(ROOMS[self.current_room]['name'], True, WHITE)
        bg_rect = pygame.Rect(10, 10, room_name.get_width() + 20, 40)
        pygame.draw.rect(self.screen, BLACK, bg_rect)
        pygame.draw.rect(self.screen, WHITE, bg_rect, 2)
        self.screen.blit(room_name, (20, 20))
        
        # Inventory button
        inv_text = f"Items ({len(self.inventory)})"
        inv_surface = self.font_small.render(inv_text, True, WHITE)
        inv_bg = pygame.Rect(SCREEN_WIDTH - 110, 10, 100, 35)
        pygame.draw.rect(self.screen, (200, 150, 0), inv_bg)
        pygame.draw.rect(self.screen, WHITE, inv_bg, 2)
        self.screen.blit(inv_surface, (SCREEN_WIDTH - 105, 18))
    
    def draw_dialogue(self):
        if not self.dialogue_active:
            return
        
        # Dialogue box
        dialog_rect = pygame.Rect(0, SCREEN_HEIGHT - 160, SCREEN_WIDTH, 160)
        pygame.draw.rect(self.screen, DIALOG_BG, dialog_rect)
        pygame.draw.rect(self.screen, BLUE, dialog_rect, 4)
        
        # NPC name
        npc_text = self.current_npc['name']
        npc_surface = self.font_medium.render(npc_text, True, YELLOW)
        self.screen.blit(npc_surface, (20, SCREEN_HEIGHT - 150))
        
        # Dialogue text
        text_surface = self.font_small.render(self.current_dialogue['text'], True, WHITE)
        self.screen.blit(text_surface, (20, SCREEN_HEIGHT - 120))
        
        # Choices
        y_offset = SCREEN_HEIGHT - 85
        for i, choice in enumerate(self.current_dialogue['choices']):
            choice_color = YELLOW if i == self.selected_choice else WHITE
            choice_text = f"> {choice['text']}" if i == self.selected_choice else f"  {choice['text']}"
            choice_surface = self.font_small.render(choice_text, True, choice_color)
            self.screen.blit(choice_surface, (20, y_offset))
            y_offset += 25
        
        # Help text
        help_text = "W/S: Navigate - E: Select - ESC: Close"
        help_surface = self.font_tiny.render(help_text, True, LIGHT_GRAY)
        self.screen.blit(help_surface, (20, SCREEN_HEIGHT - 20))
    
    def draw_inventory_screen(self):
        if not self.show_inventory:
            return
        
        # Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(240)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Title
        title = self.font_large.render("INVENTORY", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))
        
        # Items
        if not self.inventory:
            empty_text = self.font_medium.render("Your inventory is empty.", True, GRAY)
            self.screen.blit(empty_text, (SCREEN_WIDTH // 2 - empty_text.get_width() // 2, 150))
            hint_text = self.font_small.render("Talk to NPCs to get items!", True, GRAY)
            self.screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, 180))
        else:
            y_pos = 100
            for item in self.inventory:
                item_rect = pygame.Rect(100, y_pos, SCREEN_WIDTH - 200, 50)
                pygame.draw.rect(self.screen, DARK_GRAY, item_rect)
                pygame.draw.rect(self.screen, GRAY, item_rect, 2)
                item_text = self.font_medium.render(item, True, WHITE)
                self.screen.blit(item_text, (120, y_pos + 15))
                y_pos += 60
        
        # Close button
        close_text = "Press I or ESC to close"
        close_surface = self.font_small.render(close_text, True, RED)
        self.screen.blit(close_surface, (SCREEN_WIDTH // 2 - close_surface.get_width() // 2, 420))
    
    def draw_menu(self):
        self.screen.fill(BLACK)
        
        if self.show_controls:
            # Controls screen
            title = self.font_large.render("CONTROLS", True, WHITE)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
            
            controls = [
                "WASD / Arrow Keys - Move",
                "E / Enter - Interact / Select",
                "I - Open Inventory",
                "ESC - Close Dialog / Inventory",
                "",
                "Press any key to go back"
            ]
            
            y = 150
            for text in controls:
                surf = self.font_small.render(text, True, WHITE)
                self.screen.blit(surf, (SCREEN_WIDTH // 2 - surf.get_width() // 2, y))
                y += 40
        else:
            # Main menu
            # Logo
            logo_x = SCREEN_WIDTH // 2 - self.logo.get_width() // 2
            self.screen.blit(self.logo, (logo_x, 80))
            
            # Subtitle
            subtitle = self.font_medium.render("School RPG Adventure", True, GRAY)
            self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 200))
            
            # Menu buttons
            for i, button in enumerate(self.menu_buttons):
                color = YELLOW if i == self.menu_selected else WHITE
                text = f"> {button['text']}" if i == self.menu_selected else f"  {button['text']}"
                surf = self.font_medium.render(text, True, color)
                self.screen.blit(surf, (SCREEN_WIDTH // 2 - surf.get_width() // 2, button['y']))
            
            # Hint
            hint = self.font_tiny.render("W/S: Navigate - Enter: Select", True, GRAY)
            self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 420))
    
    def draw(self):
        if self.in_menu:
            self.draw_menu()
        else:
            self.screen.fill(DARK_GRAY)
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