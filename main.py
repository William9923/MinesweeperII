import sys
from gui import GUI
import PySimpleGUI as sg


if __name__ == "__main__" :
    
    # Init the loading screen / get test case data
    gui = GUI()
    gui.init_loading_screen()


    fname = gui.initInputFile()
    # Processing and get setting 
    # run the env, get result

    # render the gui 
    gui.render()

    # Processing the output one by one
    position = 0
    while True:
        event, values = gui.window.read()

        if event is None : # or position >= len(history)
            break

        if event == '-RESET-':
            gui.clearLog()
            position = 0

        if event == '-MOVE-':
            # add data from the history 
            position += 1 

    gui.window.close() 