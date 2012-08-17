import kivy

#all the kivy stuff
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color
from kivy.graphics import Rectangle

#TODO to be cross platform this as to use shutil or something
relative = '/'.join(__file__.split('/')[:-1])
if relative == '': relative = '.'

import string


class Worker():
    """
    The class that holds all worker code
    """
    

    def __init__(self):
        """
        Worker code
        """
        #self.game_state = GameState()
        #self.game_state.init()
        self.quotes_file = 'assets/data/quotes.xml'
        self.config_file = '~/.cryptograme/conf/config.xml'
        self.data = {}
        

    def init(self):
        """
        Additional init
        """
        self.data = {
                     'categories' : ['testing', 'more testing'],
                     'authors' : ['A Tester']
                     }
        

    def new_cryptogram(self):
        """
        Start a new puzzle
        """

    def save_cryptogram(self):
        """
        Save progress
        """

    def discard_cryptogram(self):
        """
        Discard progress
        """

    def configure(self):
        """
        Configure the game
        """

class SolverLetter(Button):
    def __init__(self, letter):
        super(SolverLetter, self).__init__(text=letter, size_hint_x=None, width=60)
        

class SolverBox(BoxLayout):
    def __init__(self):
        super(SolverBox, self).__init__(spacing=5, size_hint_x=None, width=((65*26)))
        self.letter_pool = {}
        self.re_init()
    
    def add_letter(self, letter):
        temp = SolverLetter(letter)
        self.letter_pool[letter.lower()]=temp
        self.add_widget(temp)

    def pop_letter(self, letter):
        '''
        '''

    def re_init(self):
        for letter in string.ascii_uppercase:
            self.add_letter(letter)

class SolverWin(ScrollView):
    def __init__(self, size):
        super(SolverWin, self).__init__(size_hint=(None,None), scroll_view_y=False, size=(800, 40))
        #scroll_view_x=False, 

class SolverWinBox(BoxLayout):
    def __init__(self):
        super(SolverWinBox, self).__init__(size_hint_x=1, size_hint_y=.1)
        solve_box = SolverBox()
        self.solve_win = SolverWin(None)
        self.add_widget(self.solve_win)
        self.solve_win.add_widget(solve_box)


class PuzzleLetter(BoxLayout):
    def __init__(self):
        super(PuzzleLetter, self).__init__()

class PuzzleWord(BoxLayout):
    def __init__(self):
        super(PuzzleWord, self).__init__()

class PuzzleRow(BoxLayout):
    def __init__(self):
        super(PuzzleRow, self).__init__()

class PuzzleWin(BoxLayout):
    def __init__(self):
        super(PuzzleWin, self).__init__( size_hint=(1, .8))

class HeaderBarLabel(BoxLayout):
    def __init__(self, title='Author: ', label='Unknown'):
        super(HeaderBarLabel, self).__init__( size_hint=(1, .3))
        the_label = Label(text=title, size_hint=(.25, 1))
        self.add_widget(the_label)
        space = Label(text='', size_hint=(.25, 1))
        self.add_widget(space)
        self.label = Label(text=label, size_hint=(.25, 1))
        self.add_widget(self.label)
        space = Label(text='', size_hint=(.25, 1))
        self.add_widget(space)

class HeaderBarSection(BoxLayout):
    def __init__(self, one, two, three):
        super(HeaderBarSection, self).__init__( size_hint=(.3, 1), orientation='vertical')
        self.one = HeaderBarLabel(one[0], one[1])
        self.add_widget(self.one)
        self.two = HeaderBarLabel(two[0], two[1])
        self.add_widget(self.two)
        self.three = HeaderBarLabel(three[0], three[1])
        self.add_widget(self.three)

class HeaderBar(BoxLayout):
    def __init__(self):
        super(HeaderBar, self).__init__( size_hint=(1.0, .1))
        self.leftbar = HeaderBarSection(('Author: ', 'Unknown'),
                                        ('Topic: ', 'Unknown'),
                                        ('Solve: ', 'False')
                                        )
        self.add_widget(self.leftbar)
        self.centerbar = HeaderBarSection(('Selected: ',''),
                                         ('',''),
                                         ('','')
                                         )
        self.add_widget(self.centerbar)
        self.rightbar = HeaderBarSection(('',''),
                                       ('',''),
                                       ('','')
                                       )
        self.add_widget(self.rightbar)
        
class PaneTemplate(BoxLayout):
    def __init__(self):
        super(PaneTemplate, self).__init__( size_hint=(1.0, .8), orientation='vertical')
        
class MainPane(PaneTemplate):
    def __init__(self):
        super(MainPane, self).__init__()
        self.header_bar = HeaderBar()
        self.add_widget(self.header_bar)
        self.puzzle_win = PuzzleWin()
        self.add_widget(self.puzzle_win)
        self.solver_win = SolverWinBox()
        self.add_widget(self.solver_win)
        
        
class ToolBar(BoxLayout):
    def __init__(self):
        super(ToolBar, self).__init__( size_hint=(1.0, .05) )
        new = Button(text='New')
        self.add_widget(new)
        home = Button(text='Home')
        self.add_widget(home)
        configure = Button(text='Options')
        self.add_widget(configure)
        about = Button(text='About')
        self.add_widget(about)
        help_button = Button(text='Help')
        self.add_widget(help_button)

class WindowBox(BoxLayout):
    def __init__(self):
        super(WindowBox, self).__init__(orientation='vertical')
        self.tool_bar = ToolBar()
        self.add_widget(self.tool_bar)
        self.main_pane = MainPane()
        self.add_widget(self.main_pane)

        
        #Insert the other panes but don't attach them
        #i like how kivy has a way to carte blanche detach all children

class KivyCryptoGrame(App):
    def __init__(self):
        super(KivyCryptoGrame, self).__init__()
        self.cryptogram_main_win = WindowBox()
        self.worker = Worker()

    
    def build(self):
        '''
        self.cryptogram_main_win.main_pane.header_bar.leftbar.one.label.text = 'Test'
        ??
        self.cryptogram_main_win.main_pane.header_bar.leftbar.one.label.texture_update()
        ???
        need a post-start event to resize the scrollable, most easily done with not rendering it
        immediately and using a welcome button...
        '''
        return self.cryptogram_main_win

app = KivyCryptoGrame()

if __name__ == '__main__':
    app.run()