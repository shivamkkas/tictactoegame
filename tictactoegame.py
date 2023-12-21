import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i:i+3] for i in range(0, 9, 3)]:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_blocks(self):
        return ' ' in self.board

    def num_empty_blocks(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            else:
                if self.num_empty_blocks()==0:
                    self.current_winner = "Tie"
            return True
        return False

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False

class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8): ')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val

class AI_agent(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = 4
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter  
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'position': None,
                    'score': 1 * (state.num_empty_blocks() + 1) if other_player == max_player else -1 * (
                                state.num_empty_blocks() + 1)}
        elif not state.empty_blocks():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -float('inf')}
        else:
            best = {'position': None, 'score': float('inf')}

        for possible_moves in state.available_moves():
            state.make_move(possible_moves, player)
            sim_score = self.minimax(state, other_player)

            state.board[possible_moves] = ' '  # reset board after try
            state.current_winner = None
            sim_score['position'] = possible_moves  # this represents the move optimal next move
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

class TicTacToe_Game:
    def __init__(self, root, x_player, o_player):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.game = TicTacToe()
        self.root.resizable(0,0)
        self.x_player = x_player
        self.o_player = o_player

        # Create buttons for each square
        self.buttons = [tk.Button(root, text='', font=('normal', 20), width=5,bg='#ADD8E6', height=2, command=lambda i=i: self.make_move(i)) for i in range(9)]

        # Grid layout for buttons
        for i, button in enumerate(self.buttons):
            row, col = divmod(i, 3)
            button.grid(row=row, column=col)

        # Status label
        self.status_label = tk.Label(root, text='', font=('normal', 14))
        self.status_label.grid(row=3, column=0, columnspan=3)

    def make_move(self, square):
        if self.game.make_move(square, self.x_player.letter):
            self.update_board()
            if self.game.current_winner:
                self.show_winner()
            else:
                self.o_player_move()

    def o_player_move(self):
        if self.game.empty_blocks():
            square = self.o_player.get_move(self.game)
            if self.game.make_move(square, self.o_player.letter):
                self.update_board()
                if self.game.current_winner:
                    self.show_winner()

    def update_board(self):
        for i, button in enumerate(self.buttons):
            button.config(text=self.game.board[i], state='disabled' if self.game.board[i] != ' ' else 'normal')

    def show_winner(self):
        winner = self.game.current_winner
        if winner == 'X':
            message = "You win!"
        elif winner == 'O':
            message = "Computer wins!"
        else:
            message = "It's a tie!"
        
        self.status_label.config(text=message)
        for button in self.buttons:
            button.config(state='disabled')

        # Ask if the player wants to play again
        play_again = messagebox.askyesno("Game Over", f"{message}\nDo you want to play again?")
        if play_again:
            self.reset_game()
        else:
            self.root.destroy()    

    def reset_game(self):
        self.game = TicTacToe()
        self.status_label.config(text='')
        for button in self.buttons:
            button.config(text='', state='normal')

#main program
if __name__ == "__main__":
    x_player = HumanPlayer('X')
    o_player = AI_agent('O')

    root = tk.Tk()
    app = TicTacToe_Game(root, x_player, o_player)
    root.mainloop()
