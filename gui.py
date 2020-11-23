import PySimpleGUI as sg

BOARDCOLOR="#bbbbbb"
BOARDBORDER="#f2dcbb"

DARKBUTTON="#39311d"
LIGHTBUTTON="#ffdd93"

GREEN="#28df99"
BLUE="#0f3057"
RED="#ec0101"

BOMBICON="💣"
FLAGICON="🚩"

class GUI():
    def __init__(self, b_size=4):
      self.b_size = b_size
      self.window = None
      sg.ChangeLookAndFeel('Reddit')

    def set_size(b_size):
      self.b_size = b_size

    def init_loading_screen(self):
        layout = [
            [sg.T('MINESWEEPER', font='Any 20', justification='center')],
            [sg.T(BOMBICON, font='Any 20', justification='center')],
            [sg.ProgressBar(150, orientation='h', size=(25, 3), key='progbar')]
        ]
        self.loading_window = sg.Window(
            'Loading Screen',
            layout,
            element_justification='center',
            no_titlebar=True,
            keep_on_top=True,
            grab_anywhere=False, 
            alpha_channel=0.85)
        
        for i in range(150):
            event, values = self.loading_window.read(timeout=10)          
            self.loading_window['progbar'].update_bar(i + 1)
        self.loading_window.close()

    def init_game_board(self):
        button_size = (6,3) if self.b_size <= 6 else (4,2)

        board=[[(i, j) for j in range(self.b_size)] for i in range(self.b_size)]
        board_layout=[[sg.B('', size=button_size, key=(i,j), pad=(0,0),disabled=True, focus=False,border_width=2, button_color=(BOARDCOLOR, BOARDBORDER))
              for j in range(self.b_size)] for i in range(self.b_size)]

        return board_layout

    def init_game_status(self):
        layout = [
            [sg.Column([
                [sg.MLine(key='-MLOutput-' + sg.WRITE_ONLY_KEY, size=(60,16))]
            ], element_justification="center")],
            [sg.Column([[
                self.init_game_button("-MOVE-", "Move"),
                self.init_game_button("-RESET-", "Reset")
            ]], justification='center', element_justification="center")]
        ]
        return layout 

    def init_game_button(self, event, text):
        return sg.B(text, size=(20,3), key=event, pad=(2,2), button_color=(BOARDBORDER, DARKBUTTON))

    def init_layout(self):
        return [[
            sg.Column(self.init_game_board()),
            sg.VerticalSeparator(pad=(3,2)),
            sg.Column(self.init_game_status())
        ]]

    def generate_color_theme(self, item):
      return {
        1:BLUE,
        2:GREEN,
        3:RED,
      }.get(item)
      
  
    def render(self):
        if self.window is None :
            self.window = sg.Window("Minesweeper", self.init_layout(), keep_on_top=True, resizable=False)

    def update(self, board, facts):
      if self.window is None:
          self.render()
      self.updateBoard(board)
      self.flushLog(facts)
  
    def updateBoard(self, board):
      for i in range(self.b_size):
        for j in range(self.b_size):
          if board[i][j] != -1:
            item = board[i][j]
            self.window[(i, j)].update(item, disabled_button_color=(self.generate_color_theme(item), disabled=True))

    def flushLog(self, logs):
      for log in logs:
        self.addLog(log)


    def initInputFile(self):
        event, values = sg.Window('My Script',
                    [[sg.Text('Testcase to open')],
                    [sg.In(), sg.FileBrowse()],
                    [sg.Open(), sg.Cancel()]]).read(close=True)
        fname = values[0]
        return fname

    def addLog(self, log):
        self.window['-MLOutput-' + sg.WRITE_ONLY_KEY].print(log) 

    def clearLog(self):
        self.window['-MLOutput-' + sg.WRITE_ONLY_KEY].update('')

    def input(self):
        return None




