import random
import copy

base_layout = {
        1: " []", 2: "[]", 3: "[]\n",
        4: "[]", 5: "[]", 6: "[]\n",
        7: "[]", 8: "[]", 9: "[]", 
        }

commands = """ 
    Available commands you can type:
        -q -> Exits the game.
        -h -> Shows this list of commands.
        -i -> Shows instructions and how to play guide.
        -s -> Choose single player mode.
        -m -> Choose multiplayer mode.
 """

game_guide = r"""
    
    _   _      _             _             
    | | (_)    | |           | |            
    | |_ _  ___| |_ __ _  ___| |_ ___   ___ 
    | __| |/ __| __/ _` |/ __| __/ _ \ / _ |
    | |_| | (__| || (_| | (__| || (_) |  __/
    \__|_|\___|\__\__,_|\___|\__\___/ \___|

    
    GAMEPLAY:
    The layout of the game is a 3x3 grid, as usual.
    Each cell corresponds to a number.
                                    [1] [2] [3]
                                    [4] [5] [6]
                                    [7] [8] [9]
    To place your mark simply type the number of the cell you wish to fill.
    For example if you type "6" this is what you'd get:
                                    [] [] []
                                    [] [] [X]
                                    [] [] []
    RULES:                                
    You are X , your friend (or the computer if you chose single player mode) is O. 
    Players take turns putting their marks in empty squares. The first player to 
    get 3 marks in a row (up, down, across, or diagonally) is the winner. 
    When all 9 squares are full, the game is over.

    To see all available commands type "-h"

 """

start_message = """ 
    To play in SINGLE PLAYER MODE type "-s" 
    To play in MULTIPLAYER MODE type "-m"
    """

################ FUNCTIONS #################
def random_choice(cells_taken:list[int]):
    """ 
    Generates a random number that'll be used to place a [0] mark by the computer in single player mode.
    
    If the random number matches a cell that is already taken, it'll trigger a while loop to keep generating a number until it matches an empty cell.
    
    Args:
        cells_taken(list): A list of the cells that are already filled.
    
    Returns:
        Random_number(int): A valid number to be used as a position in game's grid.
         
    """
    choice = random.randint(1,9)
    while choice in cells_taken:
        choice = random.randint(1,9)

    return choice

def check_win(layout:dict, mark:str):
    """ 
    Analyses the game's grid to determine if the current player has won.

    Creates a list of the cells the current player has filled and compares it to every combination of cells that count as a win.

    Args:
        layout(dict): Game's current grid
        mark(str): Current player's mark (X or O)
    
    Returns:
        Boolean: Weather user has won this time or not.   
    """
    possible_wins = [
                        # Diagonal wins
                        [1, 5, 9], [3, 5, 7],
                        # Vertical wins
                        [1, 4, 7], [2, 5, 8], [3, 6, 9], 
                        # Horizontal wins
                        [1, 2, 3], [4, 5, 6], [7, 8, 9]
                    ]
    cells_filled = []

    for num in layout: # this ensures numbers will always be ordered correctly
        if layout[num].rstrip("\n") == mark:
            cells_filled.append(num)

    for win in possible_wins:
        if all(num in cells_filled for num in win): # This will check if all numbers necessary to win can be found in the cells_field list, regardles of how many items it has
            return True
   
    return False

def place_mark(position:int, layout:dict[int, str], mark:str):
    """ 
    Puts user's mark in the corresponding chosen cell.
    It will append a line break if user chose 3 or 6, for formating reasons.

    Args:
        position(int): The cell chosen by the user.
        layout(dict): The current grid of the game.
        mark(str): Current player's mark (X or O).
    Returns:
        layout(dict): Updated game grid
    """
    
    if position == 3 or position == 6:
        layout[position] = f"{mark}\n"
    else:
        layout[position] = mark
    
    return layout

def handle_input(user_input:str, cells_taken:list[int]):
    """
    Validates and processes the user's input for selecting a cell in the game.

    This function ensures that the input is a valid integer, within the range of 
    available cells (1-9), and not already taken. If the input is invalid, the 
    user is prompted to re-enter their choice until a valid input is provided.

    Args:
        user_input (str): The raw input provided by the user.
        cells_taken (list): A list of integers representing the cells that are 
            already filled.

    Returns:
        int: The validated cell number chosen by the user.
    """
    
    while True:
        try:
            new_input = int(user_input)  # Try converting the passed argument
        except ValueError:
            user_input = input("Invalid input. Please only type numbers while playing: ")  
            continue  # Restart loop with the new input
        else:
            if new_input < 1 or new_input > 9:
                user_input = input("Invalid input. Only numbers from 1 to 9 are allowed: ")  
            elif new_input in cells_taken:
                user_input = input("That cell is already filled. Choose another one: ")  
            else:
                break  # Valid input, exit loop

    return new_input  # Successfully validated input
 
def single_game():    
    current_grid = base_layout.copy()  # Create copy of base_layout so the grid resets every game
    cells_taken = []
    while len(cells_taken) < 9:
        # User turn
        user = handle_input(user_input=input("\nYour turn: "),
                            cells_taken=cells_taken)
        current_grid = place_mark(position=user,
                                  layout=current_grid,
                                  mark="[X]")
        print(" ".join(current_grid.values()))
        cells_taken.append(user)

        if check_win(current_grid, mark="[X]"):
            return "user"
        
        # Check if all cells are taken before the computer's turn
        if len(cells_taken) == 9:
            break  # Exit the loop if the grid is full

        # Computer turn
        ai_choice = random_choice(cells_taken)        
        current_grid = place_mark(position=ai_choice, 
                                  layout=current_grid, 
                                  mark="[O]")
        print("\nComputer's turn:")
        print(" ".join(current_grid.values()))
        cells_taken.append(ai_choice)
        
        if check_win(current_grid, mark="[O]"):
            return "ai"
    
    return "tie"
   
def multi_game():
    print("\nPlayer 1 is X\nPlayer 2 is O\n")
    
    current_grid = base_layout.copy()  # Create a copy of base_layout so the grid resets every game
    cells_taken = []
    while len(cells_taken) < 9:
        # Player 1's turn
        player1 = handle_input(
                           user_input=input("\nPlayer 1's turn: "),
                            cells_taken=cells_taken)
        current_grid = place_mark(
                                player1, 
                                layout=current_grid, 
                                mark="[X]")
        print( " ".join(current_grid.values()) )
        cells_taken.append(player1)

        if check_win(current_grid, mark="[X]"):
            return "player1"

        # Check if all cells are taken before next person's turn
        if len(cells_taken) == 9:
            break  # Exit the loop if the grid is full                    
            
        # Player 2's turn
        player2 = handle_input(
                            input("\nPlayer 2's turn: "),
                            cells_taken=cells_taken)
        current_grid = place_mark(
                                player2, 
                                layout=current_grid, 
                                mark="[O]")
        print(" ".join(current_grid.values()))
        cells_taken.append(player2)
        
        if check_win(current_grid, mark="[O]"):                
            return "player2"        

    return "tie"

################ GAME LOOP ################# 
print(game_guide)
print(start_message)
user = input("👉 ").lower()
while True:
    match user:
        case "-s":
            match single_game():
                case "user":
                    print("You won! Congrats 🎉")
                case "ai":
                    print("Computer won, too bad 😔")
                case "tie":
                    print("Looks like it's a tie this time 🤷")
                    

        case "-m":
                match multi_game():
                    case "player1":
                        print("Player 1 won, Congrats 🎉")
                    case "player2":
                        print("Player 2 won, Great game! 💪")
                    case "tie":
                        print("Looks like it's a tie this time 🤷")

        case "-h":
            print(commands)
        case "-i":
            print(game_guide)
        case "-q":
            print("Thanks for playing 👋")
            break
        case _:
            print("That is not a valid command.")
    
    user = input('\nType anything: ')
