import re
from copy import deepcopy
from pprint import pprint

FACTPATTERN=r"checked\s\d\s\d\s\d"

def parser(fact:str):
  needed_string = re.findall(FACTPATTERN, str(fact))[0]
  location = re.findall(r'[0-9]', str(needed_string))
  print(location)
  row, col, val = list(map(int, location)) 
  return row, col, val

def check(fact:str):
  return bool(re.search(str(FACTPATTERN),str(fact)))

def generate_history_state(old, row, col, val):
  new = deepcopy(old)
  new[row][col] = val 
  return new

def generate_init_state(b_size):
  return [[-1 for i in range(b_size)] for i in range(b_size)]

def validate(history, fact):
  pass  


if __name__ == "__main__":
  init = generate_init_state(4)
  history = [init]
  fact = "(checked 0 1 0)"

  if (check(fact)):
    row,col,val = parser(fact)
    # ganti append sementara, nanti ganti dengan kapan bom ditemukan
    history.append(generate_history_state(history[len(history)-1], row, col, val))
  pprint (history)
  # if (check(fact)):
  #   print(parser(fact))
