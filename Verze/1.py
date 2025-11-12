import pygame
import sys

# Initialize Pygame
pygame.init()

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
WALL_COLOR = (139, 115, 85)
DOOR_COLOR = (101, 67, 33)
PLAYER_COLOR = (52, 152, 219)
BLUE = (41, 128, 185)
YELLOW = (241, 196, 15)
RED = (231, 76, 60)
DIALOG_BG = (20, 20, 20)

# Room layouts (0 = floor, 1 = wall, 2 = door)
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
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1]
        ],
        'doors': {
            'classroom': {'x': 1, 'y': 8, 'target_x': 18, 'target_y': 13},
            'locker': {'x': 18, 'y': 8, 'target_x': 1, 'target_y': 13},
            'bathroom': {'x': 9, 'y': 14, 'target_x': 10, 'target_y': 1}
        },
        'npcs': [
            {'id': 'principal', 'x': 10, 'y': 3, 'name': 'Principal Smith', 'sprite': '👔'}
        ]
    },
    'classroom': {
        'name': "Classroom",
        'layout': [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,1],
            [1,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,1],
            [1,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,1],
            [1,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ],
        'doors': {
            'hall': {'x': 18, 'y': 13, 'target_x': 1, 'target_y': 8}
        },
        'npcs': [
            {'id': 'teacher', 'x': 3, 'y': 2, 'name': 'Ms. Johnson', 'sprite': '👩‍🏫'},
            {'id': 'student1', 'x': 10, 'y': 5, 'name': 'Alex', 'sprite': '🧑'}
        ]
    },
    'locker': {
        'name': "Locker Room",
        'layout': [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,1],
            [1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,1],
            [1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,1],
            [1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ],
        'doors': {
            'hall': {'x': 1, 'y': 13, 'target_x': 18, 'target_y': 8}
        },
        'npcs': [
            {'id': 'janitor', 'x': 15, 'y': 7, 'name': 'Mr. Rodriguez', 'sprite': '🧹'}
        ]
    },
    'bathroom': {
        'name': "Bathroom",
        'layout': [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,0,1,1,1,0,1,1,1,0,0,1,1,1,1],
            [1,0,1,1,1,0,0,1,1,1,0,1,1,1,0,0,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,0,1,1,1,0,1,1,1,0,0,1,1,1,1],
            [1,0,1,1,1,0,0,1,1,1,0,1,1,1,0,0,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,0,1,1,1,0,1,1,1,0,0,1,1,1,1],
            [1,0,1,1,1,0,0,1,1,1,0,1,1,1,0,0,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ],
        'doors': {
            'hall': {'x': 10, 'y': 1, 'target_x': 9, 'target_y': 14}
        },
        'npcs': [
            {'id': 'student2', 'x': 5, 'y': 7, 'name': 'Jamie', 'sprite': '🧑‍🎓'}
        ]
    }
}

# Dialogue trees
DIALOGUES = {
    'principal': {
        'greeting': {
            'text': "Welcome to Gymlit High! I'm Principal Smith. How can I help you today?",
            'choices': [
                {'text': "What should I do here?", 'next': 'help'},
                {'text': "I'm looking for something to do.", 'next': 'quest'},
                {'text': "Just exploring, thanks!", 'next': 'bye'}
            ]
        },
        'help': {
            'text': "Explore the school, talk to teachers and students. Press E to interact with people!",
            'choices': [{'text': "Got it, thanks!", 'next': 'bye'}]
        },
        'quest': {
            'text': "Actually, could you help me? I lost my keys somewhere in the school. Can you find them?",
            'choices': [
                {'text': "Sure, I'll look for them!", 'next': 'accept_quest', 'item': 'Quest: Find Keys'},
                {'text': "Maybe later.", 'next': 'bye'}
            ]
        },
        'accept_quest': {
            'text': "Thank you! Check the locker room and bathroom. The janitor might have seen them.",
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
    }
}

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("GYMLIT - School RPG")
        self.clock = pygame.time.Clock()
        self.running = True
        
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
        
        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        self.font_tiny = pygame.font.Font(None, 14)
        
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
                # Inventory toggle
                if event.key == pygame.K_i:
                    if not self.dialogue_active:
                        self.show_inventory = not self.show_inventory
                
                # Escape key
                if event.key == pygame.K_ESCAPE:
                    if self.dialogue_active:
                        self.dialogue_active = False
                    elif self.show_inventory:
                        self.show_inventory = False
                
                # Dialogue controls
                if self.dialogue_active:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selected_choice = max(0, self.selected_choice - 1)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selected_choice = min(len(self.current_dialogue['choices']) - 1, 
                                                   self.selected_choice + 1)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_e:
                        self.handle_choice(self.current_dialogue['choices'][self.selected_choice])
                
                # Interaction
                elif not self.show_inventory:
                    if event.key == pygame.K_e or event.key == pygame.K_RETURN:
                        npc = self.get_nearby_npc()
                        if npc:
                            self.start_dialogue(npc)
    
    def update(self):
        if self.dialogue_active or self.show_inventory:
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
                    
                    # Wall collision
                    if tile == 1:
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
                                return
                    
                    # Normal move
                    self.player_x = new_x
                    self.player_y = new_y
                    self.move_timer = current_time
    
    def draw_room(self):
        room = ROOMS[self.current_room]
        layout = room['layout']
        
        for y, row in enumerate(layout):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                if tile == 0:
                    pygame.draw.rect(self.screen, GRAY, rect)
                elif tile == 1:
                    pygame.draw.rect(self.screen, WALL_COLOR, rect)
                elif tile == 2:
                    pygame.draw.rect(self.screen, DOOR_COLOR, rect)
                
                pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)
    
    def draw_npcs(self):
        room = ROOMS[self.current_room]
        for npc in room['npcs']:
            # Draw NPC emoji
            text = self.font_medium.render(npc['sprite'], True, WHITE)
            self.screen.blit(text, (npc['x'] * TILE_SIZE + 4, npc['y'] * TILE_SIZE + 4))
            
            # Draw name tag
            name_bg = pygame.Rect(npc['x'] * TILE_SIZE - 10, npc['y'] * TILE_SIZE - 15, 50, 12)
            pygame.draw.rect(self.screen, (0, 0, 0, 180), name_bg)
            name_text = self.font_tiny.render(npc['name'], True, WHITE)
            self.screen.blit(name_text, (npc['x'] * TILE_SIZE - 8, npc['y'] * TILE_SIZE - 13))
    
    def draw_player(self):
        # Player body
        player_rect = pygame.Rect(self.player_x * TILE_SIZE + 4, 
                                  self.player_y * TILE_SIZE + 4, 
                                  TILE_SIZE - 8, TILE_SIZE - 8)
        pygame.draw.rect(self.screen, PLAYER_COLOR, player_rect)
        
        # Eyes
        pygame.draw.rect(self.screen, WHITE, 
                        (self.player_x * TILE_SIZE + 10, self.player_y * TILE_SIZE + 8, 4, 4))
        pygame.draw.rect(self.screen, WHITE, 
                        (self.player_x * TILE_SIZE + 18, self.player_y * TILE_SIZE + 8, 4, 4))
    
    def draw_ui(self):
        # Room name
        room_name = self.font_medium.render(ROOMS[self.current_room]['name'], True, WHITE)
        bg_rect = pygame.Rect(10, 10, room_name.get_width() + 20, 40)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)
        self.screen.blit(room_name, (20, 20))
        
        # Inventory button
        inv_text = f"🎒 Items ({len(self.inventory)})"
        inv_surface = self.font_small.render(inv_text, True, WHITE)
        inv_bg = pygame.Rect(SCREEN_WIDTH - 140, 10, 130, 35)
        pygame.draw.rect(self.screen, (200, 150, 0), inv_bg)
        self.screen.blit(inv_surface, (SCREEN_WIDTH - 135, 18))
    
    def draw_dialogue(self):
        if not self.dialogue_active:
            return
        
        # Dialogue box
        dialog_rect = pygame.Rect(0, SCREEN_HEIGHT - 160, SCREEN_WIDTH, 160)
        pygame.draw.rect(self.screen, DIALOG_BG, dialog_rect)
        pygame.draw.rect(self.screen, BLUE, dialog_rect, 4)
        
        # NPC name
        npc_text = f"{self.current_npc['sprite']} {self.current_npc['name']}"
        npc_surface = self.font_medium.render(npc_text, True, YELLOW)
        self.screen.blit(npc_surface, (20, SCREEN_HEIGHT - 150))
        
        # Dialogue text
        text_surface = self.font_small.render(self.current_dialogue['text'], True, WHITE)
        self.screen.blit(text_surface, (20, SCREEN_HEIGHT - 120))
        
        # Choices
        y_offset = SCREEN_HEIGHT - 85
        for i, choice in enumerate(self.current_dialogue['choices']):
            choice_color = YELLOW if i == self.selected_choice else WHITE
            choice_text = f"→ {choice['text']}" if i == self.selected_choice else f"  {choice['text']}"
            choice_surface = self.font_small.render(choice_text, True, choice_color)
            self.screen.blit(choice_surface, (20, y_offset))
            y_offset += 25
        
        # Help text
        help_text = "W/S: Navigate • E: Select • ESC: Close"
        help_surface = self.font_tiny.render(help_text, True, (150, 150, 150))
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
        title = self.font_large.render("🎒 INVENTORY", True, WHITE)
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
                pygame.draw.rect(self.screen, (40, 40, 40), item_rect)
                pygame.draw.rect(self.screen, (80, 80, 80), item_rect, 2)
                item_text = self.font_medium.render(item, True, WHITE)
                self.screen.blit(item_text, (120, y_pos + 15))
                y_pos += 60
        
        # Close button
        close_text = "Press I or ESC to close"
        close_surface = self.font_small.render(close_text, True, RED)
        self.screen.blit(close_surface, (SCREEN_WIDTH // 2 - close_surface.get_width() // 2, 420))
    
    def draw(self):
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
