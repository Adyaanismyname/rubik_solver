import tkinter as tk
from tkinter import messagebox
import time
from terminal_ui import find_solution

class RubiksCube:
    def __init__(self):
        # Initial cube state (6 faces, 3x3 each)
        # Each face is represented by a 3x3 matrix
        self.faces = {
            'U': [['Y'] * 3 for _ in range(3)],  # Yellow (Top)
            'D': [['W'] * 3 for _ in range(3)],  # White (Bottom)
            'F': [['O'] * 3 for _ in range(3)],  # Orange (Front)
            'B': [['R'] * 3 for _ in range(3)],  # Red (Back)
            'L': [['G'] * 3 for _ in range(3)],  # Green (Left)
            'R': [['B'] * 3 for _ in range(3)],  # Blue (Right)
        }

    def rotate_face(self, face):
        # Rotate a face clockwise
        self.faces[face] = [
            [self.faces[face][2][0], self.faces[face][1][0], self.faces[face][0][0]],
            [self.faces[face][2][1], self.faces[face][1][1], self.faces[face][0][1]],
            [self.faces[face][2][2], self.faces[face][1][2], self.faces[face][0][2]]
        ]

    def rotate_face_counterclockwise(self, face):
        # Rotate a face counterclockwise
        self.faces[face] = [
            [self.faces[face][0][2], self.faces[face][1][2], self.faces[face][2][2]],
            [self.faces[face][0][1], self.faces[face][1][1], self.faces[face][2][1]],
            [self.faces[face][0][0], self.faces[face][1][0], self.faces[face][2][0]]
        ]

    def apply_move(self, move):
        if move == 'U':
            self._rotate_u()
        elif move == 'R':
            self._rotate_r()
        elif move == 'F':
            self._rotate_f()
        elif move == 'D':
            self._rotate_d()

    def _rotate_u(self):
        self.rotate_face('U')  # Rotate the top face itself
        temp = self.faces['F'][0][:]  # Save the top row of F
        self.faces['F'][0] = self.faces['R'][0]
        self.faces['R'][0] = self.faces['B'][0]
        self.faces['B'][0] = self.faces['L'][0]
        self.faces['L'][0] = temp


    def _rotate_u_prime(self):
        self.rotate_face_counterclockwise('U')
        temp = self.faces['F'][0][:]
        self.faces['F'][0] = self.faces['L'][0]
        self.faces['L'][0] = self.faces['B'][0]
        self.faces['B'][0] = self.faces['R'][0]
        self.faces['R'][0] = temp


    def _rotate_r(self):
        self.rotate_face('R')  # Rotate the right face itself
        temp = [self.faces['U'][i][2] for i in range(3)]  # Save the right column of U
        for i in range(3):
            self.faces['U'][i][2] = self.faces['F'][i][2]
            self.faces['F'][i][2] = self.faces['D'][i][2]
            self.faces['D'][i][2] = self.faces['B'][2 - i][0]
            self.faces['B'][2 - i][0] = temp[i]


    def _rotate_r_prime(self):
        self.rotate_face_counterclockwise('R')
        temp = [self.faces['U'][i][2] for i in range(3)]
        for i in range(3):
            self.faces['U'][i][2] = self.faces['B'][2 - i][0]
            self.faces['B'][2 - i][0] = self.faces['D'][i][2]
            self.faces['D'][i][2] = self.faces['F'][i][2]
            self.faces['F'][i][2] = temp[i]
    
    def _rotate_l(self):
        self.rotate_face('L')  # Rotate the left face itself clockwise
        temp = [self.faces['U'][i][0] for i in range(3)]  # Save the left column of U
        for i in range(3):
            self.faces['U'][i][0] = self.faces['B'][2 - i][2]  # Move B to U
            self.faces['B'][2 - i][2] = self.faces['D'][i][0]  # Move D to B
            self.faces['D'][i][0] = self.faces['F'][i][0]  # Move F to D
            self.faces['F'][i][0] = temp[i]  # Move U to F

    def _rotate_l_prime(self):
        self.rotate_face_counterclockwise('L')  # Rotate the left face itself counterclockwise
        temp = [self.faces['U'][i][0] for i in range(3)]  # Save the left column of U
        for i in range(3):
            self.faces['U'][i][0] = self.faces['F'][i][0]  # Move F to U
            self.faces['F'][i][0] = self.faces['D'][i][0]  # Move D to F
            self.faces['D'][i][0] = self.faces['B'][2 - i][2]  # Move B to D
            self.faces['B'][2 - i][2] = temp[i]  # Move U to B



    def _rotate_f(self):
        self.rotate_face('F')  # Rotate the front face itself clockwise
        temp = self.faces['U'][2][:]  # Save the bottom row of U
        self.faces['U'][2] = [self.faces['L'][2 - i][2] for i in range(3)]  # Move L to U
        for i in range(3):
            self.faces['L'][2 - i][2] = self.faces['D'][0][i]  # Move D to L
            self.faces['D'][0][i] = self.faces['R'][i][0]  # Move R to D
            self.faces['R'][i][0] = temp[i]  # Move U to R


    def _rotate_f_prime(self):
        self.rotate_face_counterclockwise('F')  # Rotate the front face itself counterclockwise
        temp = self.faces['U'][2][:]  # Save the bottom row of U
        self.faces['U'][2] = [self.faces['R'][i][0] for i in range(3)]  # Move R to U
        for i in range(3):
            self.faces['R'][i][0] = self.faces['D'][0][i]  # Move D to R
            self.faces['D'][0][i] = self.faces['L'][2 - i][2]  # Move L to D
            self.faces['L'][2 - i][2] = temp[i]  # Move U to L


        

    def _rotate_d(self):
        self.rotate_face('D')
        temp = self.faces['F'][2][:]
        self.faces['F'][2] = self.faces['L'][2][:]
        self.faces['L'][2] = self.faces['B'][2][:]
        self.faces['B'][2] = self.faces['R'][2][:]
        self.faces['R'][2] = temp

    def _rotate_d_prime(self):
        self.rotate_face_counterclockwise('D')
        temp = self.faces['F'][2][:]
        self.faces['F'][2] = self.faces['R'][2][:]
        self.faces['R'][2] = self.faces['B'][2][:]
        self.faces['B'][2] = self.faces['L'][2][:]
        self.faces['L'][2] = temp

    def y_move(self):
    # Rotate the U (top) face clockwise
        self.rotate_face('U')
        # Rotate the D (bottom) face counterclockwise
        self.rotate_face_counterclockwise('D')

        # Swap the front, right, back, and left faces
        temp = self.faces['F']
        self.faces['F'] = self.faces['R']
        self.faces['R'] = self.faces['B']
        self.faces['B'] = self.faces['L']
        self.faces['L'] = temp
    
    def y_prime(self):
    # Rotate the U (top) face counterclockwise
        self.rotate_face_counterclockwise('U')
        # Rotate the D (bottom) face clockwise
        self.rotate_face('D')

        # Swap the front, left, back, and right faces in reverse order
        temp = self.faces['F']
        self.faces['F'] = self.faces['L']
        self.faces['L'] = self.faces['B']
        self.faces['B'] = self.faces['R']
        self.faces['R'] = temp
    
    def x(self):
        # Perform a clockwise x-move (top becomes back, front becomes top, etc.)
        self.rotate_face('U')  # Rotate the top face clockwise
        self.rotate_face('D')  # Rotate the bottom face clockwise

        # Swap the faces in the correct order
        temp = self.faces['U']
        self.faces['U'] = self.faces['F']
        self.faces['F'] = self.faces['D']
        self.faces['D'] = self.faces['B']
        self.faces['B'] = temp

    def x_prime(self):
        # Perform a counterclockwise x-move (inverse of the x-move)
        self.rotate_face_counterclockwise('U')  # Rotate the top face counterclockwise
        self.rotate_face_counterclockwise('D')  # Rotate the bottom face counterclockwise

        # Swap the faces in the reverse order
        temp = self.faces['U']
        self.faces['U'] = self.faces['B']
        self.faces['B'] = self.faces['D']
        self.faces['D'] = self.faces['F']
        self.faces['F'] = temp


        
    def z(self):
        # Rotate the entire cube along the z-axis (front and back faces remain unchanged)
        self.rotate_face('U')
        self.rotate_face('D')
        temp = self.faces['L']
        self.faces['L'] = self.faces['R']
        self.faces['R'] = temp

    def z_prime(self):
        # Inverse of _rotate_z (rotation in the opposite direction)
        self.rotate_face_counterclockwise('U')
        self.rotate_face_counterclockwise('D')
        temp = self.faces['L']
        self.faces['L'] = self.faces['R']
        self.faces['R'] = temp



    def _rotate_b(self):
        # Simulate B move using 2 y-moves and F
        self.y_move()
        self.y_move()
        self._rotate_f()
        self.y_move()
        self.y_move()

    def _rotate_b_prime(self):
        # Simulate B' move using 2 y-moves and F'
        self.y_move()
        self.y_move()
        self._rotate_f_prime()
        self.y_move()
        self.y_move()


    def get_state_string(self):
        # Generate a string representing the current state of the cube
        order = ['L', 'F', 'R', 'B', 'U', 'D']
        state = []
        for face in order:
            face_array = []
            for row in self.faces[face]:
                for block in row:
                    face_array.append(block.lower())
            state.append(face_array)
        return state

class CubeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rubik's Cube Simulator")

        # Initialize Rubik's Cube
        self.cube = RubiksCube()

        # Create Canvas
        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.pack()

        # Draw initial state
        self.update_canvas()

        # Add buttons for moves
        self.add_buttons()

    def update_canvas(self):
        self.canvas.delete("all")  # Clear canvas
        self.draw_face('F')

    def draw_face(self, face):
        colors = {
            'W': "white",
            'Y': "yellow",
            'G': "green",
            'B': "blue",
            'O': "orange",
            'R': "red"
        }

        size = 50  # Size of each cell
        for i in range(3):
            for j in range(3):
                x1, y1 = j * size, i * size
                x2, y2 = x1 + size, y1 + size
                color = colors[self.cube.faces[face][i][j]]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def add_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack()

        moves = ['U', 'R', 'F', 'D' , 'B' , 'Y' , 'L' , 'X' , 'Z']
        for move in moves:
            btn = tk.Button(frame, text=move, command=lambda m=move: self.make_move(m))
            btn.pack(side=tk.LEFT, padx=5)

        reverse_moves = ["U'", "R'", "F'", "D'" , "B'" , "Y'", "L'", "X'", "Z'"]
        for move in reverse_moves:
            btn = tk.Button(frame, text=move, command=lambda m=move: self.make_move(m))
            btn.pack(side=tk.LEFT, padx=5)



        # Add exit button
        exit_btn = tk.Button(frame, text="Exit", command=self.show_state)
        exit_btn.pack(side=tk.LEFT, padx=5)

        solve_btn = tk.Button(frame, text="Solve", command=self.solve)
        solve_btn.pack(side=tk.LEFT, padx=5)


    def make_move(self, move):
        if "'" in move:
            base_move = move[0]
            if base_move == 'U':
                self.cube._rotate_u_prime()
            elif base_move == 'R':
                self.cube._rotate_r_prime()
            elif base_move == 'F':
                self.cube._rotate_f_prime()
            elif base_move == 'D':
                self.cube._rotate_d_prime()
            elif base_move == 'Y':
                self.cube.y_prime()
            elif base_move == 'B':
                self.cube._rotate_b_prime()
            elif base_move == 'L':
                self.cube._rotate_l_prime()
            elif base_move == 'X':
                self.cube.x_prime()
            elif base_move == 'Z':
                self.cube.z_prime()  # Perform the Z move on the cube
        else:
            if move == 'U':
                self.cube._rotate_u()
            elif move == 'R':
                self.cube._rotate_r()
            elif move == 'F':
                self.cube._rotate_f()
            elif move == 'D':
                self.cube._rotate_d()
            elif move == "Y":
                self.cube.y_move()  # Perform the Y move on the cube
            elif move == 'B':
                self.cube._rotate_b()  # Perform the B move on the cube
            elif move == 'L':
                self.cube._rotate_l()  # Perform the L move on the cube
            elif move == 'X':
                self.cube.x()  # Perform the X move on the cube
            elif move == 'Z':
                self.cube.z()  # Perform the Z move on the cube
        self.update_canvas()
    
    def y_move(self):
        self.cube.y_move()  # Perform the Y move on the cube
        self.update_canvas()

    def show_state(self):
        state_string = self.cube.get_state_string()
        print(state_string)

    def solver(self,solution):
        def execute_move(index):
            if index < len(solution):
                move = solution[index].replace("-", "'")
                print("Executing move:", move)
                self.make_move(move.upper())  # Make the move
                self.update_canvas()  # Update the canvas after making the move

                # Schedule the next move after a delay
                self.root.after(1000, execute_move, index + 1)  # Delay 1000ms (1 second)
        
        execute_move(0)

    def solve(self):
        cube_state = self.cube.get_state_string()
        solution = find_solution(cube_state)
        if solution is None:
            print("could not be solved")
            return
        self.solver(solution)
    

if __name__ == "__main__":
    root = tk.Tk()
    app = CubeApp(root)
    root.mainloop()

    # Retrieve the final cube state string after exiting the app
    final_state_string = app.cube.get_state_string()
    print(f"Final Cube State: {final_state_string}")
