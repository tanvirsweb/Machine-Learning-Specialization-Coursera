import random
from collections import defaultdict

class MENACE:
    def __init__(self):
        # Dictionary to store state-action weights (equivalent to matchboxes and beads)
        self.states = defaultdict(lambda: defaultdict(int))  
        self.epsilon = 0.1  # Exploration probability

    def choose_action(self, state):
        # MENACE selects an action based on epsilon-greedy policy
        actions = self.states[state]
        valid_actions = self.get_valid_actions(state)
        if random.random() < self.epsilon or not actions:
            return random.choice(valid_actions)  # Exploration
        return max(valid_actions, key=lambda action: actions[action])  # Exploitation

    def update_weights(self, history, result):
        # Reinforce the moves based on the game result
        for state, action in history:
            if result == "win":
                self.states[state][action] += 1  # Reward for winning moves
            elif result == "loss":
                self.states[state][action] -= 1  # Penalize losing moves

    @staticmethod
    def get_valid_actions(state):
        # Return a list of empty cells (valid moves)
        return [i for i, cell in enumerate(state) if cell == 0]

    @staticmethod
    def check_winner(state):
        # Check if there's a winner
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6],  # Diagonals
        ]
        for combo in winning_combinations:
            line = [state[i] for i in combo]
            if all(x == 1 for x in line):  # MENACE wins
                return "MENACE"
            if all(x == -1 for x in line):  # User wins
                return "User"
        return None

    @staticmethod
    def print_board(state):
        # Print the Tic-Tac-Toe board
        symbols = [" " if x == 0 else "X" if x == 1 else "O" for x in state]
        board = f"""
         {symbols[0]} | {symbols[1]} | {symbols[2]} 
        ---+---+---
         {symbols[3]} | {symbols[4]} | {symbols[5]} 
        ---+---+---
         {symbols[6]} | {symbols[7]} | {symbols[8]} 
        """
        print(board)

    def play_game(self):
        # Initialize the game state
        state = [0] * 9  # Empty board
        history = []  # Store MENACE's moves for reinforcement
        while True:
            # MENACE's turn
            action = self.choose_action(tuple(state))
            history.append((tuple(state), action))
            state[action] = 1  # MENACE plays as "X"
            self.print_board(state)

            # Check if MENACE wins or if the board is full
            winner = self.check_winner(state)
            if winner:
                print(f"{winner} wins!")
                self.update_weights(history, "win" if winner == "MENACE" else "loss")
                break
            if not self.get_valid_actions(state):
                print("It's a draw!")
                break

            # User's turn
            while True:
                try:
                    user_action = int(input("Enter your move (0-8): "))
                    if user_action in self.get_valid_actions(state):
                        state[user_action] = -1  # User plays as "O"
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Please enter a number between 0 and 8.")

            # Check if the user wins
            winner = self.check_winner(state)
            if winner:
                self.print_board(state)
                print(f"{winner} wins!")
                self.update_weights(history, "win" if winner == "User" else "loss")
                break
            if not self.get_valid_actions(state):
                print("It's a draw!")
                break

# Main loop
if __name__ == "__main__":
    menace = MENACE()
    print("Welcome to MENACE Tic-Tac-Toe!")
    print("You are 'O'. MENACE is 'X'. Enter a number (0-8) to make your move:")
    print("""
     0 | 1 | 2 
    ---+---+---
     3 | 4 | 5 
    ---+---+---
     6 | 7 | 8 
    """)
    while True:
        menace.play_game()
        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != "y":
            print("Thanks for playing!")
            break
