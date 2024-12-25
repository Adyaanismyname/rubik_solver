from solver_utils.functions import *
from solver_utils.data import *
from change_wd import change_wd

def find_solution(cube_state):

    change_wd()

    print("                 _____________________________")
    print("     ______    /_____________________________/")
    print("    |   _  \            _            _       _")
    print("    |  |_|  |  _    _  | | __    _  | |  _  /_/  ______")
    print("    |    __/  | |  | | | |/  \  | | | | / /     /  __  \ ") 
    print("    | |\ \    | |  | | |   /| | | | | |/ /     | /   |_|")
    print("    | | \ \_  | |__| | |  |_/ | | | |    \     \ \ ")
    print("    |_|  \__| \_____ / \_____/  |_| |_| \_\     \ \ ")
    print("                                                 \ \ ")
    print("     ________________________________________   _ \ \ ")
    print("    /_______________________________________/  / / \ \ ")
    print("                                              | |_ /  | ")
    print("    Welcome to the rubik solver!              \______/ ")
    print("")
    print("------------------------------------------------------------------------")
    print("       Order of faces:")
    print("          _________")
    print("         |__|__|__|                      Order of facettes in each face:")
    print("         |_FACE 4_|                          ____________")
    print("_________|__|__|__|_________________        |_0_|_1_|_2_|")
    print("|__|__|__|__|__|__|__|__|__|__|__|__|       |_3_|_4_|_5_|")
    print("|_FACE 0_|_FACE 1_|_FACE 2_|_FACE 3_|       |_6_|_7_|_8_|")
    print("|__|__|__|__|__|__|__|__|__|__|__|__|")
    print("         |__|__|__|  ")
    print("         |_FACE 5_|")
    print("         |__|__|__|")
    print("")
    print("-----------------------------------------------------------------------")
    print("Enter the colors of each face.")
    print("white: w, yellow: y, green: g, blue: b, orange: o, red: r")
    state_string = "OOWOOOOOOYRRGGWGGGBRRGRRGRRWBBBBBBBBWWRWWGWWGYYOYYYYYY"
    cube_map = input_map(cube_state)
    # white - 0 , yellow - 1 , red - 2 , orange - 3 , blue - 4 , green -5 

    try:
        print("")
        moves = []
        moves, cube_map = solve_first_cross(cube_map, moves, centers_map, edges_map)
        moves, cube_map = solve_f2l(cube_map, moves, centers_map, edges_map, corners_map)
        moves, cube_map = solve_last_cross(cube_map, moves, 4, 1, "y")
        moves, cube_map = solve_oll(1, centers_map, cube_map, moves)  
        moves, cube_map = solve_pll(cube_map, moves, "y", plls)
        moves = simplify(moves)



        print("")
        print("moves:", end = " ")
        for i in moves:
            print(i, end=" ")
        print("")
        return moves
    except:
        print("")
        print("ERROR: WRONG INPUT: the cube is not solvable") 
        print("")
    