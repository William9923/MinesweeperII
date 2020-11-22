# row,col
# 0,0 0,1
# 1,0 1,1
def generate_board(board_size, list_bomb):
    result = [[0 for i in range(board_size)] for i in range(board_size)]
    for el in list_bomb:
        result[el[0]][el[1]] = 100 ## sementara bomb ditandain >= 100
        for i in range(-1, 2):
            for j in range(-1, 2):
                row = el[0] + i
                col = el[1] + j 
                if ((row >= 0) and (col>=0) and (row < board_size) and (col < board_size)):
                    result[row][col] += 1
    return result

def generate_facts(board_size, list_bomb):
    board = generate_board(board_size, list_bomb)
    list_facts = []
    for i in range(len(board)):
      for j in range(len(board)):
        facts = "(assert (value_cell (row " + str(i) + ") (col " + str(j) + ") (val " + str(board[i][j]) + ")))"
        list_facts.append(facts)
    return list_facts

if __name__ == "__main__":
    list_bomb = [(1,0), (2,1)]
    # print(generate_board(4, list_bomb))
    list_facts = generate_facts(4, list_bomb)
    # for el in list_facts:
    #   print(el)