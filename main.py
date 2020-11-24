import sys
import PySimpleGUI as sg
from pprint import pprint

from gui import GUI
from fact_generator import generate_facts, generate_board
from setup import reader, run

CLP_FILE = "minesweeper.clp"

if __name__ == "__main__" :
    
    # Init the loading screen / get test case data
    gui = GUI()

    fname = gui.initInputFile()

    # Processing and get setting
    board_size, list_bomb = reader(fname) 
    board = generate_board(board_size, list_bomb)
    facts = generate_facts(board_size, list_bomb)
    gui.set_size(board_size)
    gui.set_board(board)


    # Run the Knowledge Based System
    # Parse Result 
    history , logs = run(CLP_FILE, facts, board_size)
    for log in logs:
        pprint(log)
    init = [[-1 for i in range(board_size)] for i in range(board_size)]
    init[0][0] = 0
    history.insert(0, init)
    logs.insert(0,["START"])

    # render the gui 
    gui.render()
    history.append([[0 for i in range(board_size)] for i in range(board_size)])
    logs.append(["DONE"])

    position = 0
    gui.update(history[position], logs[position])
    while True:
        event, values = gui.window.read()

        if event is None or (position > len(history)-1) : 
            break

        if event == '-RESET-':
            gui.clearLog()
            gui.resetBoard()
            position = 0

        if event == '-MOVE-':
            position += 1 
            gui.update(history[position+1], logs[position])
            

    gui.window.close() 