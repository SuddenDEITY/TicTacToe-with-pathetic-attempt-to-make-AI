import numpy as np
import random
import sys

class TTT:
 diff = ['user','easy', 'medium', 'hard']
 winning_indexes = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                    [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
 def __init__(self):
     self.grid = np.full((3,3), ' ')

 def start(self):
     while True:
        mode = input().split()
        if mode:
            if mode[0] == 'exit':
                sys.exit()
            if mode[0] == 'start' and len(mode[1:]) == 2 and all(el in self.diff for el in mode[1:]):
                return {'X':mode[1], 'O':mode[2]}
        print('Bad parameters!')

 def printer(self):
     print('---------')
     for i in range(3): print('|', *self.grid[i], '|')
     print('---------')

 def aiturn(self,let):
    flat = self.grid.flatten()
    if let[1] == 'easy':
     if ' ' in flat:
         s = random.choice([i for i in range(len(self.grid.flatten())) if self.grid.flatten()[i] == ' '])
         flat[s] = let[0]
         self.grid = flat.reshape(3, 3)
    if let[1] == 'medium':
        if ' ' in flat:
            s = self.medium(let[0])
            if s != None:
             flat[s] = let[0]
            else:
             s = random.choice([i for i in range(len(self.grid.flatten())) if self.grid.flatten()[i] == ' '])
             flat[s] = let[0]
            self.grid = flat.reshape(3, 3)
    if let[1] == 'hard':
        if 'X' not in flat and 'O' not in flat:
            s = random.choice([0,1,2,3,4,5,6,7,8])
        else:
            s = self.hard(flat,let[0])
        flat[s] = let[0]
        self.grid = flat.reshape(3, 3)
    print(f'Making move level {let[1]}')
    self.printer()

 def minimax(self, board, depth, is_maximazing):
     if self.wincheck(self.ai, board):
         return 100
     if self.wincheck(self.user, board):
         return -100
     if self.checkdraw(board):
         return 0

     if is_maximazing:
          best_score = -sys.maxsize
          for i in range(len(board)):
              if board[i] == ' ':
                  board[i] = self.ai
                  score = self.minimax(board, depth + 1, False)
                  board[i] = ' '
                  best_score = max(best_score, score)

     else:
         best_score = sys.maxsize
         for i in range(len(board)):
             if board[i] == ' ':
                 board[i] = self.user
                 score = self.minimax(board, depth + 1, True)
                 board[i] = ' '
                 best_score = min(best_score, score)

     return best_score

 def hard(self, flat, let):
     move = None
     if let == self.ai: best_score = -sys.maxsize
     else: best_score = sys.maxsize
     board = flat.copy()
     for i in range(len(board)):
         if board[i] == ' ':
             board[i] = let
             if let == self.ai: score = self.minimax(board, 0, False)
             else: score = self.minimax(board, 0, True)
             board[i] = ' '
             if let == self.ai:
              if score > best_score:
                 best_score = score
                 move = i
             else:
              if score < best_score:
                 best_score = score
                 move = i

     return move

 def medium(self,let):
     mark = []
     flat = self.grid.flatten()
     for el in self.winning_indexes:
         for j in el:
             mark.append(flat[j])
         if mark.count(let) == 2 and ' ' in mark:
             return el[mark.index(' ')]
         if (mark.count('X') == 2 or mark.count('O') == 2) and ' ' in mark:
             return el[mark.index(' ')]
         mark.clear()

 def userturn(self, let):
     coords = input('Enter the coordinates: ').split()
     if self.check(coords):
         self.grid[int(coords[0]) - 1][int(coords[1]) - 1] = let[0]
         self.printer()
     else:
         return self.userturn(let)

 def wincheck(self,let,flat):
     for el in self.winning_indexes:
         if flat[el[0]] == let and flat[el[0]] == flat[el[1]] == flat[el[2]]:
             return True
     return False

 def checkdraw(self,flat):
     if ' ' not in flat and not self.wincheck('X',flat) and not self.wincheck('O',flat):
         return True
     return False

 def check(self, coords):
     if coords[0].isdigit() and coords[1].isdigit():
         if (int(coords[0]) <= 3 and int(coords[0]) >= 1) and (int(coords[1]) <= 3 and int(coords[1]) >= 1):
             if self.grid[int(coords[0]) - 1][int(coords[1]) - 1] == ' ':
                 return True
             else: print('This cell is occupied! Choose another one!')
         else: print('Coordinates should be from 1 to 3!')
     else: print('You should enter numbers!')

 def game(self):
     d = self.start()
     if list(d.items())[0][1] != 'user' and list(d.items())[1][1] != 'user':
         self.ai = 'X'
         self.user = 'O'
         while True:
             self.aiturn(list(d.items())[0])
             if self.wincheck(list(d.items())[0][0], self.grid.flatten()):
                 print(f'{list(d.items())[0][0]} wins!')
                 break
             if self.checkdraw(self.grid.flatten()):
                 print('Draw!')
                 break
             self.aiturn(list(d.items())[1])
             if self.wincheck(list(d.items())[1][0], self.grid.flatten()):
                 print(f'{list(d.items())[1][0]} wins!')
                 break
             if self.checkdraw(self.grid.flatten()):
                 print('Draw!')
                 break
     elif list(d.items())[0][1] != 'user':
         self.ai = 'X'
         self.user = 'O'
         while True:
             self.aiturn(list(d.items())[0])
             if self.wincheck(list(d.items())[0][0], self.grid.flatten()):
                 print(f'{list(d.items())[0][0]} wins!')
                 break
             if self.checkdraw(self.grid.flatten()):
                 print('Draw!')
                 break
             self.userturn(list(d.items())[1])
             if self.wincheck(list(d.items())[1][0], self.grid.flatten()):
                 print(f'{list(d.items())[1][0]} wins!')
                 break
             if self.checkdraw(self.grid.flatten()):
                 print('Draw!')
                 break
     else:
         self.printer()
         self.user = 'X'
         self.ai = 'O'
         while True:
             self.userturn(list(d.items())[0])
             if self.wincheck(list(d.items())[0][0], self.grid.flatten()):
                 print(f'{list(d.items())[0][0]} wins!')
                 break
             if self.checkdraw(self.grid.flatten()):
                 print('Draw!')
                 break
             self.aiturn(list(d.items())[1])
             if self.wincheck(list(d.items())[1][0], self.grid.flatten()):
                 print(f'{list(d.items())[1][0]} wins!')
                 break
             if self.checkdraw(self.grid.flatten()):
                 print('Draw!')
                 break

n = TTT()
n.game()