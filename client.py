#!/usr/bin/python

import sys
import json
import socket


def check_surroundings(board, row, col, opponent, score):
  #checking perimeter around piece
  
  best_move = None

  valid_moves = {}
  temp_max = 0

  for i in range(row - 1, row + 2):
    for j in range(col - 1, col + 2):
      if i >= 0 and i < 8 and j >= 0 and j < 8:
        if i == row and j == col:
          continue
        
        if board[i][j] == opponent:
          
          temp_max = line_check(board, i, j, row, col, opponent, valid_moves, score)

        #Check all the valid moves for best one
        for k in valid_moves:
          if k > temp_max:
            temp_max = k

        if temp_max > score:
          score = temp_max
          best_move = valid_moves[score]
    valid_moves.clear()

  return {score: best_move}

#check if there is a line of enemies 
#for each enemy you encounter in a given direction, increase the score. 
def line_check(board, next_row, next_col, row, col, opponent, valid_moves, total):

  total += 1

  if next_row >= 0 and next_row < 8 and next_col >= 0 and next_col < 8:
    if board[next_row][next_col] == opponent:
      
      #if next opponent piece is in the top row
      if next_row < row:
        if next_col < col:
          line_check(board, next_row - 1, next_col - 1, row, col, opponent, valid_moves, total)
        elif next_col > col:
          line_check(board, next_row - 1, next_col + 1, row, col, opponent, valid_moves, total)
        elif next_col == col:
          line_check(board, next_row - 1, next_col, row, col, opponent, valid_moves, total)
      
      #if next opponent piece is in the bottom row
      elif next_row > row:
        if next_col < col:
          line_check(board, next_row + 1, next_col - 1, row, col, opponent, valid_moves, total)
        elif next_col > col:
          line_check(board, next_row + 1, next_col + 1, row, col, opponent, valid_moves, total)
        elif next_col == col:
          line_check(board, next_row + 1, next_col, row, col, opponent, valid_moves, total)

      #if next opponent piece is in the same row
      elif next_row == row:
        if next_col < col:
          line_check(board, next_row, next_col - 1, row, col, opponent, valid_moves, total)
        elif next_col > col:
          line_check(board, next_row, next_col + 1, row, col, opponent, valid_moves, total)

    # if there is an available spot in a higher
    # tactical position
    if(board[next_row][next_col] == 0):

      augment = 0
      for i in range(next_row - 1, next_row + 2):
        for j in range(next_col - 1, next_col + 2):
          if i >= 0 and i < 8 and j >= 0 and j < 8:
            if(board[i][j] == opponent):
              augment += 2
      total += augment

      # if(next_row == 7) or (next_row == 0) or (next_col == 7) or (next_col == 0):
      #   total += 2
      if(next_row <= 2) or (next_col <= 2):
        total += 3
      if (next_row == next_col) or (abs(next_row - next_col) == 7):
        if next_row == 7 or next_col == 7:
          total += 100
        total += 2
      if abs(next_row - next_col) == 1 or abs(next_row - next_col) == 6:
        total = 1
      valid_moves.update({total: [next_row, next_col]})
      return total
    else:
      return

def get_move(player, board):
  #Finding out who's turn it is
  if player == 1:
    opponent = 2
  else:
    opponent = 1
 
  move = []
  temp_move = {}
  score = 0
  temp_max = 0

  #Checing the surrounding areas adjacent to each player piece
  for row in range(0, 8):
    for col in range(0, 8):

      if board[row][col] == player: 
        temp_move = check_surroundings(board, row, col, opponent, score)

        temp_max = next(iter(temp_move))

        for i in temp_move:
          if i > temp_max:
            temp_max = i
        
        if temp_move[temp_max] is not None:
          move = temp_move[temp_max]
        
  return move
  
def prepare_response(move):
  response = '{}\n'.format(move).encode()
  print('sending {!r}'.format(response))
  return response

if __name__ == "__main__":
  # board = [[0 for x in range(8)] for x in range(8)]
  # board =  [[0, 0, 0, 2, 1, 0, 0, 2], [0, 0, 0, 0, 1, 0, 2, 0], [0, 2, 2, 2, 1, 2, 0, 0], [0, 0, 2, 2, 1, 0, 0, 0], [1, 2, 1, 2, 2, 0, 0, 0], [2, 0, 2, 2, 2, 2, 0, 0], 
  # [0, 2, 1, 0, 1, 0, 0, 0], [0, 1, 1, 1, 0, 1, 0, 0]]



  
  # get_move(1, board)
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.connect((host, port))
    while True:
      data = sock.recv(1024)
      if not data:
        print('connection to server closed')
        break
      json_data = json.loads(str(data.decode('UTF-8')))
      board = json_data['board']
      maxTurnTime = json_data['maxTurnTime']
      player = json_data['player']
      print(player, maxTurnTime, board)

      move = get_move(player, board)
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()
