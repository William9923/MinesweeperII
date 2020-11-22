from clips import Environment

from fact_generator import generate_facts

def load_file(filename: str):
  with open(filename, "r") as f:
    return "".join(f.readlines())

def assert_all(env, filename: str):
  with open(filename, "r") as f:
    for line in f.readline():
      env.build(line)

if __name__ == '__main__' :
  list_bomb = [(1,0), (2,1)]
  list_facts = generate_facts(4, list_bomb)
  # for el in list_facts:
  #   print(el)
  # arr = findFact(list_facts)

  env = Environment()

  rule = """
  (defrule my-rule
    (my-fact first-slot)
    =>
    (printout t "My Rule fired!" crlf))
  """
  env.build(rule)

  for rule in env.rules():
      print(rule)
  # insert templates
  # template_str = load_file("minesweeper.clp")
  # with open("scripts/deftemplate.clp", "r") as f:
  #   for line in f.readline():
  #     env.build(line)
  # print(template_str)
  # env.load(template_str)
  # env.run()
  # print("t")
  # print(len(list(env.rules())))
  # for rule in env.rules():
  #   print(rule)

  

  # insert facts
  # for fact in list_facts:
  #       env.assert_string(fact)
  # facts_str = load_file("scripts/a")