import pygame
import sys
from copy import deepcopy
from terminal_ui import find_solution

# Initialize pygame
pygame.init()

# Constants for the display
WIDTH, HEIGHT = 1000, 700  # Increased height to make space for history display
BUTTON_HEIGHT = 30

# Colors for cube faces
COLORS = {
    'g': (0, 255, 0),     # Green
    'o': (255, 165, 0),   # Orange
    'b': (0, 0, 255),     # Blue
    'r': (255, 0, 0),     # Red
    'y': (255, 255, 0),   # Yellow
    'w': (255, 255, 255), # White
}

# Initial cube state
def get_initial_cube():
    return [
        ['g'] * 9,  # Left face
        ['o'] * 9,  # Front face
        ['b'] * 9,  # Right face
        ['r'] * 9,  # Back face
        ['y'] * 9,  # Top face
        ['w'] * 9,  # Bottom face
    ]

# Initialize state
cube = get_initial_cube()
history = []  # Store states after every move

def draw_cube(screen, cube):
    """Draw the cube on the screen."""
    size = 40
    start_x, start_y = 50, 50
    offsets = {
        0: (-3 * size, size),   # Left face
        1: (0, size),           # Front face
        2: (3 * size, size),    # Right face
        3: (6 * size, size),    # Back face
        4: (0, -2 * size),      # Top face
        5: (0, 4 * size),       # Bottom face
    }

    for face_index, face in enumerate(cube):
        offset_x, offset_y = offsets[face_index]
        for i, color in enumerate(face):
            x = start_x + offset_x + (i % 3) * size
            y = start_y + offset_y + (i // 3) * size
            pygame.draw.rect(screen, COLORS[color], (x, y, size - 2, size - 2))

# Cube operations functions
def rotate_face(face):
    """Rotate a face 90 degrees clockwise."""
    return [face[6], face[3], face[0], face[7], face[4], face[1], face[8], face[5], face[2]]

def rotate_face_ccw(face):
    """Rotate a face 90 degrees counter-clockwise."""
    return [face[2], face[5], face[8], face[1], face[4], face[7], face[0], face[3], face[6]]

# Move functions
def r_move(cube):
    """Perform the R move."""
    new_cube = deepcopy(cube)
    new_cube[2] = rotate_face(cube[2])
    temp = [cube[4][2], cube[4][5], cube[4][8]]
    new_cube[4][2], new_cube[4][5], new_cube[4][8] = cube[1][2], cube[1][5], cube[1][8]
    new_cube[1][2], new_cube[1][5], new_cube[1][8] = cube[5][2], cube[5][5], cube[5][8]
    new_cube[5][2], new_cube[5][5], new_cube[5][8] = cube[3][6], cube[3][3], cube[3][0]
    new_cube[3][6], new_cube[3][3], new_cube[3][0] = temp
    return new_cube

def r_prime(cube):
    """Perform the R' move."""
    new_cube = deepcopy(cube)
    for _ in range(3):
        new_cube = r_move(new_cube)
    return new_cube

def u_move(cube):
    """Perform the U move."""
    new_cube = deepcopy(cube)
    new_cube[4] = rotate_face(cube[4])
    temp = cube[0][:3]
    new_cube[0][:3] = cube[1][:3]
    new_cube[1][:3] = cube[2][:3]
    new_cube[2][:3] = cube[3][:3]
    new_cube[3][:3] = temp
    return new_cube

def u_prime(cube):
    """Perform the U' move."""
    new_cube = deepcopy(cube)
    for _ in range(3):
        new_cube = u_move(new_cube)
    return new_cube

def l_move(cube):
    """Perform the L move."""
    new_cube = deepcopy(cube)
    new_cube[0] = rotate_face(cube[0])
    temp = [cube[4][0], cube[4][3], cube[4][6]]
    new_cube[4][0], new_cube[4][3], new_cube[4][6] = cube[3][8], cube[3][5], cube[3][2]
    new_cube[3][8], new_cube[3][5], new_cube[3][2] = cube[5][0], cube[5][3], cube[5][6]
    new_cube[5][0], new_cube[5][3], new_cube[5][6] = cube[1][0], cube[1][3], cube[1][6]
    new_cube[1][0], new_cube[1][3], new_cube[1][6] = temp
    return new_cube

def l_prime(cube):
    """Perform the L' move."""
    new_cube = deepcopy(cube)
    for _ in range(3):
        new_cube = l_move(new_cube)
    return new_cube

def f_move(cube):
    """Perform the F move."""
    new_cube = deepcopy(cube)
    new_cube[1] = rotate_face(cube[1])
    temp = [cube[4][6], cube[4][7], cube[4][8]]
    new_cube[4][6], new_cube[4][7], new_cube[4][8] = cube[0][8], cube[0][5], cube[0][2]
    new_cube[0][8], new_cube[0][5], new_cube[0][2] = cube[5][2], cube[5][1], cube[5][0]
    new_cube[5][2], new_cube[5][1], new_cube[5][0] = cube[2][0], cube[2][3], cube[2][6]
    new_cube[2][0], new_cube[2][3], new_cube[2][6] = temp
    return new_cube

def f_prime(cube):
    """Perform the F' move."""
    new_cube = deepcopy(cube)
    for _ in range(3):
        new_cube = f_move(new_cube)
    return new_cube

def b_move(cube):
    """Perform the B move."""
    new_cube = deepcopy(cube)
    new_cube[3] = rotate_face(cube[3])
    temp = [cube[4][0], cube[4][1], cube[4][2]]
    new_cube[4][0], new_cube[4][1], new_cube[4][2] = cube[2][2], cube[2][5], cube[2][8]
    new_cube[2][2], new_cube[2][5], new_cube[2][8] = cube[5][8], cube[5][7], cube[5][6]
    new_cube[5][8], new_cube[5][7], new_cube[5][6] = cube[0][6], cube[0][3], cube[0][0]
    new_cube[0][6], new_cube[0][3], new_cube[0][0] = temp
    return new_cube

def b_prime(cube):
    """Perform the B' move."""
    new_cube = deepcopy(cube)
    for _ in range(3):
        new_cube = b_move(new_cube)
    return new_cube

def y_move(cube):
    """Perform the Y move (rotate the cube around the y-axis)."""
    new_cube = deepcopy(cube)
    new_cube[4] = rotate_face(cube[4])
    new_cube[5] = rotate_face_ccw(cube[5])
    new_cube[0], new_cube[1], new_cube[2], new_cube[3] = cube[1], cube[2], cube[3], cube[0]
    return new_cube

def y_prime(cube):
    """Perform the Y' move (rotate the cube around the y-axis counter-clockwise)."""
    new_cube = deepcopy(cube)
    for _ in range(3):
        new_cube = y_move(new_cube)
    return new_cube

def x_move(cube):
    """Perform the X move."""
    new_cube = deepcopy(cube)

    # Cycle and reorient faces (following R, U, L pattern)
    temp = [new_cube[4][6], new_cube[4][3], new_cube[4][0]]
    new_cube[4][6], new_cube[4][3], new_cube[4][0] = new_cube[1][6], new_cube[1][3], new_cube[1][0]
    new_cube[1][6], new_cube[1][3], new_cube[1][0] = new_cube[5][6], new_cube[5][3], new_cube[5][0]
    new_cube[5][6], new_cube[5][3], new_cube[5][0] = new_cube[3][2], new_cube[3][5], new_cube[3][8]
    new_cube[3][2], new_cube[3][5], new_cube[3][8] = temp
    
    temp = [new_cube[4][7], new_cube[4][4], new_cube[4][1]]
    new_cube[4][7], new_cube[4][4], new_cube[4][1] = new_cube[1][7], new_cube[1][4], new_cube[1][1]
    new_cube[1][7], new_cube[1][4], new_cube[1][1] = new_cube[5][7], new_cube[5][4], new_cube[5][1]
    new_cube[5][7], new_cube[5][4], new_cube[5][1] = new_cube[3][1], new_cube[3][4], new_cube[3][7]
    new_cube[3][1], new_cube[3][4], new_cube[3][7] = temp

    temp = [new_cube[4][8], new_cube[4][5], new_cube[4][2]]
    new_cube[4][8], new_cube[4][5], new_cube[4][2] = new_cube[1][8], new_cube[1][5], new_cube[1][2]
    new_cube[1][8], new_cube[1][5], new_cube[1][2] = new_cube[5][8], new_cube[5][5], new_cube[5][2]
    new_cube[5][8], new_cube[5][5], new_cube[5][2] = new_cube[3][0], new_cube[3][3], new_cube[3][6]
    new_cube[3][0], new_cube[3][3], new_cube[3][6] = temp
    
    new_cube[2] = rotate_face(cube[2])
    new_cube[0] = rotate_face_ccw(cube[0])
    return new_cube

def x_prime(cube):
    """Perform the X' move."""
    new_cube = deepcopy(cube)

    temp = [new_cube[4][6], new_cube[4][3], new_cube[4][0]]
    new_cube[4][6], new_cube[4][3], new_cube[4][0] = new_cube[3][2], new_cube[3][5], new_cube[3][8]
    new_cube[3][2], new_cube[3][5], new_cube[3][8] = new_cube[5][6], new_cube[5][3], new_cube[5][0]
    new_cube[5][6], new_cube[5][3], new_cube[5][0] = new_cube[1][6], new_cube[1][3], new_cube[1][0]
    new_cube[1][6], new_cube[1][3], new_cube[1][0] = temp
    
    temp = [new_cube[4][7], new_cube[4][4], new_cube[4][1]]
    new_cube[4][7], new_cube[4][4], new_cube[4][1] = new_cube[3][1], new_cube[3][4], new_cube[3][7]
    new_cube[3][1], new_cube[3][4], new_cube[3][7] = new_cube[5][7], new_cube[5][4], new_cube[5][1]
    new_cube[5][7], new_cube[5][4], new_cube[5][1] = new_cube[1][7], new_cube[1][4], new_cube[1][1]
    new_cube[1][7], new_cube[1][4], new_cube[1][1] = temp

    temp = [new_cube[4][8], new_cube[4][5], new_cube[4][2]]
    new_cube[4][8], new_cube[4][5], new_cube[4][2] = new_cube[3][0], new_cube[3][3], new_cube[3][6]
    new_cube[3][0], new_cube[3][3], new_cube[3][6] = new_cube[5][8], new_cube[5][5], new_cube[5][2]
    new_cube[5][8], new_cube[5][5], new_cube[5][2] = new_cube[1][8], new_cube[1][5], new_cube[1][2]
    new_cube[1][8], new_cube[1][5], new_cube[1][2] = temp

    new_cube[2] = rotate_face_ccw(cube[2])
    new_cube[0] = rotate_face(cube[0])

    return new_cube

def z_move(cube):
    """Perform the Z move (rotate the cube around the z-axis)."""
    new_cube = deepcopy(cube)
    new_cube[1] = rotate_face(cube[1])
    new_cube[3] = rotate_face_ccw(cube[3])
    new_cube[0], new_cube[2], new_cube[4], new_cube[5] = cube[2], cube[0], cube[5], cube[4]
    return new_cube

def z_prime(cube):
    """Perform the Z' move (rotate the cube around the z-axis counter-clockwise)."""
    new_cube = deepcopy(cube)
    for _ in range(3):
        new_cube = z_move(new_cube)
    return new_cube


def d_move(cube):
    """Perform the D move."""
    new_cube = deepcopy(cube)
    # Rotate the Down face (cube[5]) clockwise
    new_cube[5] = rotate_face(cube[5])
    
    # Cycle the bottom rows of adjacent faces: Front -> Right -> Back -> Left
    temp = cube[0][6:9]  # Save Front bottom row
    new_cube[0][6:9] = cube[3][6:9]  # Back → Front
    new_cube[3][6:9] = cube[2][6:9]  # Right → Back
    new_cube[2][6:9] = cube[1][6:9]  # Left → Right
    new_cube[1][6:9] = temp  # Front → Left

    return new_cube


def d_move(cube):
    """Perform the D move."""
    new_cube = deepcopy(cube)
    # Rotate the Down face (cube[5]) clockwise
    new_cube[5] = rotate_face(cube[5])
    
    # Cycle the bottom rows of adjacent faces: Front -> Right -> Back -> Left
    temp = cube[0][6:9]  # Save Front bottom row
    new_cube[0][6:9] = cube[3][6:9]  # Back → Front
    new_cube[3][6:9] = cube[2][6:9]  # Right → Back
    new_cube[2][6:9] = cube[1][6:9]  # Left → Right
    new_cube[1][6:9] = temp  # Front → Left

    return new_cube


def d_prime(cube):
    """Perform the D' move."""
    new_cube = deepcopy(cube)
    # Rotate the Down face (cube[5]) counter-clockwise
    new_cube[5] = rotate_face_ccw(cube[5])
    
    # Cycle the bottom rows of adjacent faces: Front -> Left -> Back -> Right
    temp = cube[0][6:9]  # Save Front bottom row
    new_cube[0][6:9] = cube[1][6:9]  # Left → Front
    new_cube[1][6:9] = cube[2][6:9]  # Right → Left
    new_cube[2][6:9] = cube[3][6:9]  # Back → Right
    new_cube[3][6:9] = temp  # Front → Back

    return new_cube

# Adding the function to output the cube state in the desired format.
def print_cube_state(cube):
    """Format and print the current cube state."""
    formatted_state = []
    for face in cube:
        formatted_state.append([face[0], face[1], face[2], face[3], face[4], face[5], face[6], face[7], face[8]])
    print(formatted_state)
    cube = solve(formatted_state , cube)

    return cube

# Main display loop
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rubik's Cube Simulator")

font = pygame.font.Font(None, 24)

def draw_buttons():
    button_x = WIDTH - 90
    """Draw buttons for cube operations."""
    buttons = ["R", "R'", "U", "U'", "L", "L'", "F", "F'", "D", "D'", "Y", "Y'", "X", "X'", "Z", "Z'", "Save State", "Print State"]
    for i, label in enumerate(buttons):
        pygame.draw.rect(screen, (200, 200, 200), (10, 10 + i * BUTTON_HEIGHT, 80, BUTTON_HEIGHT))
        text = font.render(label, True, (0, 0, 0))
        screen.blit(text, (15, 15 + i * BUTTON_HEIGHT))

def draw_history():
    """Draw the history of saved states."""
    text = font.render(f"History (Saved {len(history)} states):", True, (255, 255, 255))
    screen.blit(text, (150, 10))
    for i, state in enumerate(history):
        state_text = font.render(f"State {i+1}", True, (255, 255, 255))
        screen.blit(state_text, (150, 40 + i * BUTTON_HEIGHT))

# Add solve() function
def solve(state, cube):
    """Solve the cube and apply the solution moves."""
    print("Solving...")
    solution = find_solution(state)

    for move in solution:
        move = move.lower()
        move = move.replace("-", "'")
        print(move)
        if move.endswith("'"):  # Check if the move is a prime move
            move_name = move[:-1]  # Remove the "'" to get the move name (e.g., 'r' from 'r\'')
            # Call the corresponding prime move function
            if move_name == 'r':
                cube = r_prime(cube)
            elif move_name == 'u':
                cube = u_prime(cube)
            elif move_name == 'l':
                cube = l_prime(cube)
            elif move_name == 'f':
                cube = f_prime(cube)
            elif move_name == 'b':
                cube = b_prime(cube)
            elif move_name == 'y':
                cube = y_prime(cube)
            elif move_name == 'x':
                cube = x_prime(cube)
            elif move_name == 'z':
                cube = z_prime(cube)
            elif move_name == 'd':
                cube = d_prime(cube)
        else:  # If it's a normal move
            # Call the corresponding normal move function
            if move == 'r':
                cube = r_move(cube)
            elif move == 'u':
                cube = u_move(cube)
            elif move == 'l':
                cube = l_move(cube)
            elif move == 'f':
                cube = f_move(cube)
            elif move == 'b':
                cube = b_move(cube)
            elif move == 'y':
                cube = y_move(cube)
            elif move == 'x':
                cube = x_move(cube)
            elif move == 'z':
                cube = z_move(cube)
            elif move == 'd':
                cube = d_move(cube)

        pygame.time.delay(500)  # Delay time in milliseconds


        # Redraw the cube state after every move
        draw_cube(screen, cube)
        pygame.display.flip()

    print("Cube solved!")
    return cube

while True:
    screen.fill((30, 30, 30))
    draw_cube(screen, cube)
    draw_buttons()
    draw_history()
    pygame.display.flip()




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 10 <= x <= 90:
                for i, move_func in enumerate([r_move, r_prime, u_move, u_prime, l_move, l_prime, f_move, f_prime, d_move, d_prime, y_move, y_prime, x_move, x_prime, z_move, z_prime]):
                    if 10 + i * BUTTON_HEIGHT <= y <= 40 + i * BUTTON_HEIGHT:
                        cube = move_func(cube)
                        break
                # Save the current state when "Save State" button is clicked
                if 10 + 16 * BUTTON_HEIGHT <= y <= 40 + 16 * BUTTON_HEIGHT:
                    history.append(deepcopy(cube))
                    print(f"State saved. Total saved states: {len(history)}")
                # Print the current state when "Print State" button is clicked
                if 10 + 17 * BUTTON_HEIGHT <= y <= 40 + 17 * BUTTON_HEIGHT:
                    cube = print_cube_state(cube)

    # Optionally add functionality for undo/redo, etc.
