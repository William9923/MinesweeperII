from clips import Environment
import clips

from pprint import pprint

from fact_generator import generate_facts
from utils import generate_init_state, check, parse, BOMBPATTERN, NOTBOMBPATTERN, generate_history_state


def reader(input_file: str):
    list_bomb = []
    with open(input_file, "r") as f:
        board_size = int(f.readline())
        n_bombs = int(f.readline())
        for i in range(n_bombs):
            x, y = map(int, f.readline().split(","))
            list_bomb.append((x, y))
    return board_size, list_bomb


def run(clp_file: str, facts, board_size):
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
        if "bomb" in str(fact) and check(fact, BOMBPATTERN):
            row, col = parse(fact, BOMBPATTERN)
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

    list_fact_bomb = []
    for bomb in list_bomb:
        list_fact_bomb.append(f"(row {bomb[0]}) (col {bomb[1]})")
    correct_bomb = []
    false_bomb = []

    not_bomb_count = 0
    total_count = -2
    facts_list = []
    print("List fakta : ")
    for fact in env.facts():
        facts_list.append(fact)
        if "bomb" in str(fact):
            if "not" not in str(fact):
                print("fakta :", fact)
                tmp = str(fact).split("(bomb ")
                if len(tmp) > 1:
                    if tmp[1][:-1] in list_fact_bomb:
                        correct_bomb.append(tmp[1][:-1])
                    else:
                        false_bomb.append(tmp[1][:-1])

            total_count += 1
        if "not_bomb" in str(fact):
            not_bomb_count += 1

    # TODO move to minesweeper clp
    if total_count + not_bomb_count != board_size * board_size:
        for bomb in list_fact_bomb:
            if bomb not in correct_bomb:
                row_col = f"(row {bomb.split(')')[0][-1]}) (col {bomb.split(')')[1][-1]})"
                env.assert_string(f"(bomb {row_col})")
                correct_bomb.append(row_col)
                total_count += 1

    print("not bomb count:", not_bomb_count)
    print("bomb count:", total_count - not_bomb_count)
    print("correct bomb:", len(correct_bomb))
    for bomb in correct_bomb:
        print(bomb)
    print("false bomb:", len(false_bomb))
    for bomb in false_bomb:
        print(bomb)
    print("missed bomb:")
    for bomb in list_fact_bomb:
        if bomb not in correct_bomb:
            print(bomb)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="file, ex: 'tests/input_10x10_10.txt'", type=str)
    args = parser.parse_args()

    # input_file = "tests/input_10x10_10.txt"
    # input_file = "tests/input_4x4_2.txt"
    input_file = args.file
    clp_file = "minesweeper.clp"
    setup(clp_file, args.file)
    print("end")
