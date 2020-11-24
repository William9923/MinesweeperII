from clips import Environment
import clips

from pprint import pprint

from fact_generator import generate_facts
from utils import generate_init_state, check, parse, BOMBPATTERN, NOTBOMBPATTERN, generate_history_state

def reader(input_file:str):
  list_bomb = []
  with open(input_file, "r") as f:
      board_size = int(f.readline())
      n_bombs = int(f.readline())
      for i in range(n_bombs):
          x, y = map(int, f.readline().split(","))
          list_bomb.append((x, y))
  return board_size, list_bomb

def run(clp_file:str, facts, board_size):
  env = Environment()
  env.batch_star(clp_file)
  for fact in facts:
    env.assert_string(fact)
  
  env.run()
  print("Run clips done")

  history = [generate_init_state(board_size)]
  logs = []

  log = []
  state = generate_init_state(board_size)
  for fact in env.facts():
    log.append(str(fact))
    if "bomb" in str(fact) and check(fact,BOMBPATTERN):
      row, col = parse(fact,BOMBPATTERN)
      state = generate_history_state(state, row, col, 1)
      logs.append(log)
      history.append(state)
      log = []

    if "not_bomb" in str(fact) and check(fact, NOTBOMBPATTERN):
      row, col = parse(fact, NOTBOMBPATTERN)
      state = generate_history_state(state, row, col, 0)
  
  return history, logs

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

if __name__ == '__main__' :
  input_file = "input_10x10_8.txt"
  clp_file = "minesweeper.clp"
  setup(clp_file, input_file)
  print("end")
