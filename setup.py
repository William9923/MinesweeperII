from clips import Environment
import clips

from fact_generator import generate_facts

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

  print("List fakta : ")
  not_bomb_count = -2
  total_count = -4
  for fact in env.facts():
    print("fakta :" ,fact)
    if "bomb" in str(fact):
      total_count += 1
      if "not" in str(fact):
        not_bomb_count += 1
      # else:
        # print("fakta :" ,fact)
  print("not bomb count:", not_bomb_count)
  print("bomb count:", total_count - not_bomb_count)

if __name__ == '__main__' :
  input_file = "input_4x4_2.txt"
  clp_file = "minesweeper.clp"
  setup(clp_file, input_file)
  print("end")
