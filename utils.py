import re
from copy import deepcopy
from pprint import pprint

BOMBPATTERN=r"\(bomb\s\(row\s\d\)\s\(col\s\d\)\)"
NOTBOMBPATTERN=r"\(not_bomb\s\(row\s\d\)\s\(col\s\d\)\)"

def parse(fact:str, pattern:str):
  needed_string = re.findall(pattern, str(fact))[0]
  location = re.findall(r'[0-9]', str(needed_string))
  row, col = list(map(int, location)) 
  return row, col

def check(fact:str, pattern:str):
  return bool(re.search(str(pattern),str(fact)))

def generate_history_state(old, row, col, val):
  new = deepcopy(old)
  new[row][col] = val 
  return new

def generate_init_state(b_size):
  return [[-1 for i in range(b_size)] for i in range(b_size)]

if __name__ == "__main__":
  init = generate_init_state(4)
  history = [init]
  fact = "(checked 0 1 0)"

  if (check(fact)):
    row,col,val = parse(fact)
    # ganti append sementara, nanti ganti dengan kapan bom ditemukan
    history.append(generate_history_state(history[len(history)-1], row, col, val))
  pprint (history)
  # if (check(fact)):
  #   print(parser(fact))
