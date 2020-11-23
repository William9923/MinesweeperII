from clips import Environment
import clips

from pprint import pprint

from fact_generator import generate_facts
from parser import generate_init_state, check, parser

def setup(clp_file, input_file):

  list_bomb = []
  with open(input_file, "r") as f:
      board_size = int(f.readline())
      n_bombs = int(f.readline())
      for i in range(n_bombs):
          x, y = map(int, f.readline().split(","))
          list_bomb.append((x, y))

  list_facts = generate_facts(board_size, list_bomb)
  print("board size:", board_size)
  print("total bombs:", n_bombs)
  print()
  
  env = Environment()
  env.batch_star(clp_file)
  for fact in list_facts:
    env.assert_string(fact)

  env.run()
  print("Run clips done")
  print()
  

  print("List fakta : ")
  not_bomb_count = 0
  total_count = -2
  facts_list = []
  for fact in env.facts():
    facts_list.append(fact)
    if "bomb" in str(fact):
      print("fakta :" ,fact)
      total_count += 1
    if "not_bomb" in str(fact):
      not_bomb_count += 1
  print("not bomb count:", not_bomb_count)
  print("bomb count:", total_count - not_bomb_count)

  # print("Testing GUI")
  # board = generate_init_state(board_size)
  # for fact in facts_list:
  #   if check(fact):
  #     print(fact)
  #     row, col, val = parser(fact)
  #     board[row][col] = val
  #     pprint(board)
  
if __name__ == '__main__' :
  input_file = "input_10x10_8.txt"
  clp_file = "minesweeper.clp"
  setup(clp_file, input_file)
  print("end")
