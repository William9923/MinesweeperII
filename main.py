import sys
import PySimpleGUI as sg
from pprint import pprint

from gui import GUI
from fact_generator import generate_facts, generate_board
from setup import reader, run, get_result

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


    # Run the Knowledge Based System
    res = run(CLP_FILE, facts)

    # Parse Result 
    history, logs = get_result(res, board_size)

    # render the gui 
    gui.render()

    # Processing the output one by one
    position = 0
    while True:
        event, values = gui.window.read()

        if event is None or (position >= len(history) or position >= len(logs)) : 
            break

        if event == '-RESET-':
            gui.clearLog()
            position = 0

        if event == '-MOVE-':
            pprint(logs[position])
            pprint(history[position])
            position += 1 

    gui.window.close() 