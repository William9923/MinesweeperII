import sys
from gui import GUI
import PySimpleGUI as sg


if __name__ == "__main__" :
    
    gui = GUI(4)
    gui.init_loading_screen()
    gui.render()
    fname = gui.initInputFile()

    while True:
        event, values = gui.window.read()

        if event is None:
            break

        if event == '-RESET-':
            gui.clearLog()

        if event == '-MOVE-':
            gui.addLog("MOVE") 

    gui.window.close() 