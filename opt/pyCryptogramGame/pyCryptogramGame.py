"""
#TODOs

Game logic/code
  Quote data back-end
  Help/doc
  Configuration
  By author
  By topic
  Save state
  Trophy system

User interface
  Drag-and-drop
  Animation for win condition
  Monochrome icons
  *Maybe animations for letter boxes*
  
Code clean-up

Python cryptogram game.

Notes: separate init() and __init__() calls are because of programming style.

I like to be able to call other functions during initialization and pylint
likes to complain about that habit.

I think it makes the code more readable.

Code organization
  UI is the root user interface class.
    This is followed by custom widgets.
  
  Worker is the main worker class
    This is followed by custom classes to maintain state or add functionality
    This may be followed by custom widgets...I'm working on forcing it to be MVC...
  
  Handler is the callback handler for all Gtk callbacks

  Embedded files as strings are after this.

  Then there is the app declaration and main clause

Folder structure
  assets contains all binary files included in the application
    data contains templates for configuration files and the quote database
    icons contains the icon in various sizes for the application
    images contains any images needed
    sounds contains any sounds needed
    ui contains the glade file
"""

#gui imports
from gi.repository import Gtk

#parsing imports for configs and quotes
from bs4 import BeautifulSoup

#for mixing up letters
import string
from random import shuffle

#for relative path resolution for game assets
relative = '/'.join(__file__.split('/')[:-1])
if relative == '': relative = '.'

class UI():
    """
    The class that holds UI update code
    """
    
    def __init__(self):
        """
        UI specific code
        """
        
        self.builder = Gtk.Builder()
        self.window_showing = 'the_content'
        self.help_showing = 'None'
        
    def init(self):
        """
        Additional init
        """
        
        #get the ui file
        self.builder.add_from_file(relative + "/assets/ui/cryptogram.glade")
        #main window initialization
        
        #fix title
        main_win = self.builder.get_object("cryptogram_main_win")
        main_win.set_title("CryptoG(r||...)am(...e)")
        
        #fix toolbar theme
        toolbar = self.builder.get_object("cryptogram_toolbar")
        context = toolbar.get_style_context()
        context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        #the text is freaking ugly...so no text
        
        #change toolbar icons to monochrome ones
        #self.__fix_toolbar_icons()
        
        #intialize ads
        self.update_ad_bar("empty")
        
        #hint to start the game
        self.update_status_bar("Click the plus to start a game")
        
        #set the icon so it's portable
        main_win.set_icon_from_file(relative + "/assets/icons/64x64.png")
        
        #show
        main_win.show_all()
        
    def __set_author(self):
        """
        """
        author_label = app.ui.builder.get_object("author_replace")
        author_label.set_text(app.worker.game_state.quote_data[2])
        
    def __set_topic(self):
        """
        """
        topics = ''
        for topic in app.worker.game_state.quote_data[0]:
            topics += topic + ', '
        topics = topics[:-2]
        topic_label = app.ui.builder.get_object("topic_replace")
        topic_label.set_text(topics)
        
    def __set_solved(self):
        """
        """
        solved_label = app.ui.builder.get_object("solved_replace")
        if app.worker.game_state.quote_data[3]:
            solved_label.set_text("Yes")
        else:
            solved_label.set_text("No")
            
        
    def set_header_state(self):
        """
        """
        self.__set_author()
        self.__set_topic()
        self.__set_solved()
        
    def set_selected(self, letter):
        """
        """
        selected = app.ui.builder.get_object("selected_letter_replace")
        selected.set_text(letter)

    def __fix_toolbar_icons(self):
        """
        Replace toolbar icons with non-stock ones
        #TODO populate icons and un-comment the call during init
        """
        
        new_icon_set = self.builder.get_object("new_toolbar_button")
        image = Gtk.Image()
        image.set_from_file(relative + "/assets/images/new.png")
        new_icon_set.set_icon_widget(image)
        
        save_icon_set = self.builder.get_object("save_toolbar_button")
        image = Gtk.Image()
        image.set_from_file(relative + "/assets/images/save.png")
        save_icon_set.set_icon_widget(image)
        
        discard_icon_set = self.builder.get_object("discard_toolbar_button")
        image = Gtk.Image()
        image.set_from_file(relative + "/assets/images/discard.png")
        discard_icon_set.set_icon_widget(image)
        
        trophy_icon_set = self.builder.get_object("trophy_toolbar_button")
        image = Gtk.Image()
        image.set_from_file(relative + "/assets/images/trophy.png")
        trophy_icon_set.set_icon_widget(image)
        
        config_icon_set = self.builder.get_object("configure_toolbar_button")
        image = Gtk.Image()
        image.set_from_file(relative + "/assets/images/config.png")
        config_icon_set.set_icon_widget(image)
        
        about_icon_set = self.builder.get_object("about_toolbar_button")
        image = Gtk.Image()
        image.set_from_file(relative + "/assets/images/about.png")
        about_icon_set.set_icon_widget(image)
        
        help_icon_set = self.builder.get_object("help_toolbar_button")
        image = Gtk.Image()
        image.set_from_file(relative + "/assets/images/help.png")
        help_icon_set.set_icon_widget(image)
        

    def update_status_bar(self, text):
        """
        Update status bar text
        """
        
        status = self.builder.get_object("cryptogram_statusbar")
        context = status.get_context_id('')
        status.pop(context)
        status.push(context, text.rstrip())

    def update_ad_bar(self, ad):
        """
        Update ad bar contents
        """
        
        if ad == "empty":
            ad_text = self.builder.get_object("ad_label")
            ad_text.set_text("")
        else:
            pass

    def update_trophy_win(self, category="overall"):
        """
        Update trophy contents
        """
        
    def __show_win(self, win_name):
        """
        Moving all the show window code to one place
        """
        self.__reset_win()
        #Move the main content to the storage window
        content_box = self.builder.get_object("the_content")
        storage_win = self.builder.get_object("storage_box")
        content_box.reparent(storage_win)
        
        #Move the trophy content to the main window
        content_box = self.builder.get_object(win_name)
        storage_win = self.builder.get_object("content_box")
        content_box.reparent(storage_win)
        
        #Set active
        self.window_showing = win_name
        
    def show_main_win(self):
        """
        bounce
        """
        self.__reset_win()
        
    def __reset_win(self):
        """
        Reset window attachments
        """
        if self.window_showing == 'the_content':
            pass
        else:
            reparent_to = self.window_showing.split('_')[0]+'_win'
            
            content_box = self.builder.get_object(self.window_showing)
            storage_win = self.builder.get_object(reparent_to)
            content_box.reparent(storage_win)
            
            content_box = self.builder.get_object('the_content')
            storage_win = self.builder.get_object('content_box')
            content_box.reparent(storage_win)
            
            #reset showing window
            self.window_showing = 'the_content'

    def swap_main_win(self, win_name):
        """
        Swap window contents
        """
        self.__show_win(win_name)

    def show_trophy_win(self):
        """
        Show the trophy contents
        """
        #TODO move all these back to the button callbacks as swap_main_win("accomplishments_pane")
        self.__show_win("accomplishments_pane")
        

    def hide_trophy_win(self):
        """
        Show the main window contents
        """
        self.__reset_win()
        

    def show_config_win(self):
        """
        Show the trophy contents
        """
        self.__show_win("configuration_pane")
        

    def hide_config_win(self):
        """
        Show the main window contents
        """
        self.__reset_win()
        

    def show_about_win(self):
        """
        Show the trophy contents
        """
        self.__show_win("about_pane")
        

    def hide_about_win(self):
        """
        Show the main window contents
        """
        self.__reset_win()
        

    def show_help_win(self):
        """
        Show the trophy contents
        """
        self.__show_win("help_pane")
        

    def hide_help_win(self):
        """
        Show the main window contents
        """
        self.__reset_win()
        
    def swap_help_win(self, win_name):
        """
        Swap the help section
        """
        self.__reset_help_win()
        reparent = 'help_'+win_name+'_box'
        
        content_box = self.builder.get_object('help_topic_box')
        storage_win = self.builder.get_object('storage_box')
        content_box.reparent(storage_win)
        
        content_box = self.builder.get_object(reparent)
        storage_win = self.builder.get_object('help_topic_root_box')
        content_box.reparent(storage_win)
        self.help_showing = win_name
        

    def __reset_help_win(self):
        """
        Reset window attachments
        """
        
        reparent = 'help_'+self.help_showing+'_box'
        reparent_to = 'help_'+self.help_showing+'_win'
        if self.help_showing == 'None':
            pass
        else:
            content_box = self.builder.get_object(reparent)
            storage_win = self.builder.get_object(reparent_to)
            content_box.reparent(storage_win)
            
            content_box = self.builder.get_object('help_topic_box')
            storage_win = self.builder.get_object('help_topic_root_box')
            content_box.reparent(storage_win)
            
            #reset showing window
            self.help_showing = 'None'
            
    def swap_trophy_win(self, win_name):
        """
        Swaps the trophy title and data
        #TODO
        """
        pass

class Worker():
    """
    The class that holds all worker code
    """
    

    def __init__(self):
        """
        Worker code
        """
        self.game_state = GameState()
        self.game_state.init()
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
        app.ui.swap_main_win('selectquote_pane')
        print("Implement new cryptogram")
        

    def save_cryptogram(self):
        """
        Save progress
        """
        app.ui.swap_main_win('savestate_pane')
        

    def discard_cryptogram(self):
        """
        Discard progress
        """
        #At this point it just goes towards select new
        #It should at some point actually clear game-state
        app.ui.swap_main_win('selectquote_pane')
        

    def configure(self):
        """
        Configure the game
        """

class Substitution():
    def __init__(self, puzzle_text='', solver=False):
        """
        """
        self.solver = solver
        self.puzzle_text = puzzle_text
        self.mixed_alphabet = []
        self.alphabet = []
        self.cipher_text = ''
        for letter in string.ascii_lowercase:
            self.mixed_alphabet.append(letter)
        for letter in string.ascii_lowercase:
            self.alphabet.append(letter)
        shuffle(self.mixed_alphabet)
        for letter in puzzle_text:
            try:
                if letter in string.ascii_lowercase:
                    self.cipher_text += self.mixed_alphabet[self.alphabet.index(letter.lower())]
                else:
                    self.cipher_text += self.mixed_alphabet[self.alphabet.index(letter.lower())].upper()
            except:
                self.cipher_text += letter
        self.puzzle_win = SubstPuzzleWin(self.cipher_text)
        self.solver_win = SubstSolverWin()
        
    def update(self, solver = False):
        """
        Substitution cipher
        
        Provide cipher_text and letter_map
        letter_map is the possibly solved letter list
        """
        self.solver.solve(self.puzzle_text)
        

class SubstSolver():
    def __init__(self):
        self.the_dict = {}
    
    def add_item(self, cipher_text, new_text):
        if cipher_text in string.ascii_letters:
            self.the_dict[cipher_text.lower()] = new_text.lower()
        
    def solve(self, cipher_text):
        solved = ''
        for letter in cipher_text:
            try:
                if letter in string.ascii_lowercase:
                    solved += self.the_dict[letter]
                else:
                    solved += self.the_dict[letter.lower()].upper()
                
            except:
                if letter in string.ascii_letters:
                    solved += '_'
                else:
                    solved += letter
        return solved
    
    def check(self):
        check_text = self.solve(app.worker.game_state.puzzle_data.cipher_text)
        if app.worker.game_state.puzzle_data.puzzle_text == check_text:
            app.worker.game_state.update_solved()
            app.ui.update_status_bar("You win!!!")
            label = app.ui.builder.get_object('solved_text_replace')
            label.set_text("The quote was:\n" + app.worker.game_state.puzzle_data.puzzle_text)
            app.ui.swap_main_win('winanimation_pane')
                
class SubstPuzzleWin(Gtk.Box):
    """
    The puzzle area
    """
    def __init__(self, crypt_text):
        """
        Nothing going on here...move along
        """
        super(Gtk.Box, self).__init__()
        self.crypt_text = crypt_text.split()
        self.set_orientation(Gtk.Orientation.VERTICAL)
        
        self.update_labels()
        
    def update_labels(self):
        """
        It would be faster to update the labels instead of reallocate
        all of them every time, but I wanted to belt out a working demo
        """
        children = self.get_children()
        for child in children:
            self.remove(child)
            
        line_length = 0
        rows_lists = []
        temp_row = []
        for word in self.crypt_text:
            line_length += len(word)+1
            if line_length > 35:
                line_length = 0
                rows_lists.append(temp_row)
                temp_row = []
            else:
                temp_row.append(word)
        rows_lists.append(temp_row)
        
        for row in rows_lists:
            sep = Gtk.Separator.new(True)
            sep.set_orientation(Gtk.Orientation.HORIZONTAL)
            self.pack_start(sep , False, False, 0)
        
            #This should be in PuzzleRow
            temp_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
            for word in row:
                a_word = SubstPuzzleWord(word)
                temp_box.pack_start(a_word, False, False, 0)
                space = SubstPuzzleWord(' ')
                temp_box.pack_start(space, False, False, 0)
            self.pack_start(temp_box , False, False, 0)
            
        sep = Gtk.Separator.new(True)
        sep.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.pack_start(sep , False, False, 0)
        self.show_all()
        app.worker.game_state.puzzle_data.solver.check()
            
class SubstPuzzleRow(Gtk.Box):
    """
    """
    
class SubstPuzzleWord(Gtk.Box):
    def __init__(self, word):
        """
        Nothing going on here...move along
        """
        super(Gtk.Box, self).__init__()
        self.word = word
        for letter in self.word:
            a_letter = SubstPuzzleLetterPair(letter)
            self.pack_start(a_letter, False, False, 0)

class SubstPuzzleLetterPair(Gtk.Button):
    """
    The widget for puzzle letters
    """
    def __init__(self, letter):
        """
        Nothing going on here...move along
        """
        super(Gtk.Button, self).__init__()
        self.unsolved = letter
        self.box = Gtk.Box()
        self.box.set_orientation(Gtk.Orientation.VERTICAL)
        if letter in string.ascii_letters:
            #TODO insert shim to check for letter is solved
            self.solved = app.worker.game_state.puzzle_data.solver.solve(letter)
        else:
            self.solved = letter     
        label = Gtk.Label.new(self.unsolved)
        self.box.pack_start(label, False, False, 0)
        label_a = Gtk.Label.new(self.solved)
        self.box.pack_start(label_a, False, False, 0)
        self.add_child(app.ui.builder, self.box, None)
        self.set_relief(Gtk.ReliefStyle.NONE)
        self.connect('clicked', self.on_clicked)
        

    def on_clicked(self, *args, **kwds):
        """
        """
        letter_label = app.ui.builder.get_object("selected_letter_replace")
        letter = letter_label.get_text()
        cipher_text = args[0].get_children()[0].get_children()[0].get_text()
        app.worker.game_state.puzzle_data.algo_work.solver.add_item(cipher_text, letter)
        app.worker.game_state.puzzle_data.algo_work.puzzle_win.update_labels()
        
        
        

class SubstSolverWin(Gtk.Box):
    """
    The puzzle area
    """
    def __init__(self):
        """
        Nothing going on here...move along
        """
        super(Gtk.Box, self).__init__()
        #TODO shim in the row logic...
        self.set_orientation(Gtk.Orientation.VERTICAL)
        """
        sep = Gtk.Separator.new(True)
        sep.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.pack_start(sep , False, False, 0)
        """
        
        #This should be in PuzzleRow
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        for letter in string.ascii_uppercase:
            letter = SubstSolverLetter(letter)
            self.pack_start(letter, False, False, 0)

class SubstSolverRow(Gtk.Box):
    """
    """

class SubstSolverLetter(Gtk.Button):
    """
    The widget for puzzle letters
    """
    def __init__(self, letter):
        """
        Nothing going on here...move along
        """
        super(Gtk.Button, self).__init__()
        self.unsolved = letter
        self.set_label(self.unsolved)
        self.set_relief(Gtk.ReliefStyle.NONE)
        self.set_focus_on_click(False)
        self.connect("clicked", app.handler.on_set_letter_selected)
        
        '''
        self.connect("drag-begin", app.handler.on_set_opposite_background_solver)
        self.connect("drag-end", app.handler.on_set_normal_background_solver)
        '''
        
class PuzzleData():
    """
    The class that handles translation to and
    from ciphertext
    """
    def __init__(self, puzzle_text='', algo='substitution'):
        """
        Setup class attributes
        """
        self.puzzle_text = puzzle_text
        self.algo = algo
        self.cipherlist = {
                           "substitution" : self.__subst
                           }
        self.cipher_text = ''
        self.algo_work = ''
        self.solver = {}
        
    def init(self):
        """
        More initialization
        """
        self.cipherlist[self.algo]()
        
    def update(self):
        """
        """
        self.algo_work.update()

    def __subst(self):
        """
        Substitution cipher
        """
        self.solver = SubstSolver()
        self.algo_work = Substitution(self.puzzle_text, self.solver)
        self.cipher_text = self.algo_work.cipher_text

class GameState():
    """
    The class that holds all the data about game state
    """
    def __init__(self):
        """
        Initial game-state declarations
        """
        
        self.puzzle_open = False
        self.trophy_state = {}
        self.configuration = {}
        self.quote_data=()
        self.puzzle_data = PuzzleData()
        
    def init(self):
        """
        More initialization
        """
        

    def get_quote(self, topic=False, author=False, solved=False):
        """
        Method to set a quote
        Sets a tuple ([category, another category, ...], 'the quote', 'the author')
        """
        self.quote_data = (['testing', 'more testing'], 'This is a test.?!"\' aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa', 'A Tester', False)
        self.puzzle_data = PuzzleData(self.quote_data[1])
        self.puzzle_data.init()
        
        
        

    def load_config(self):
        """
        Load the config from XML
        """
        

    def save_config(self):
        """
        Save the config to XML
        """
        
    def update_solved(self):
        """
        Update solved puzzle data
        """

class Handler():
    """
    The class that holds all callback handlers
    """
    

    def __init__(self):
        """
        Callback handlers
        """
        

    def init(self):
        """
        Additional init
        """
        

    def on_help_toolbar_button_clicked(self, *args, **kwds):
        """
        Help clicked callback
        """
        
        app.ui.show_help_win()
        

    def on_about_toolbar_button_clicked(self, *args, **kwds):
        """
        About clicked callback
        """
        
        app.ui.show_about_win()
        

    def on_configure_toolbar_button_clicked(self, *args, **kwds):
        """
        Configure clicked callback
        """
        
        app.ui.show_config_win()
        

    def on_trophy_toolbar_button_clicked(self, *args, **kwds):
        """
        Trophy button clicked callback
        """
        
        app.ui.swap_main_win("accomplishments_pane")
        

    def on_close_trohpy_button_clicked(self, *args, **kwds):
        """
        Close trophy window button callback
        """
        
        app.ui.hide_trophy_win()
        

    def on_discard_toolbar_button_clicked(self, *args, **kwds):
        """
        Discard clicked callback
        """
        
        app.worker.discard_cryptogram()
        

    def on_save_toolbar_button_clicked(self, *args, **kwds):
        """
        Save clicked callback
        """
        
        app.worker.save_cryptogram()
        

    def on_new_toolbar_button_clicked(self, *args, **kwds):
        """
        New clicked callback
        """
        
        app.worker.new_cryptogram()
        

    def on_home_toolbar_button_clicked(self, *args, **kwds):
        """
        New clicked callback
        """
        
        app.ui.show_main_win()
        

    def on_cryptogram_main_win_delete_event(self, *args, **kwds):
        """
        Kill the app
        """
        
        Gtk.main_quit()
        
    def on_close_about_button_clicked(self, *args, **kwds):
        """
        Reset the window
        """
        app.ui.show_main_win()
        

    def on_close_help_button_clicked(self, *args, **kwds):
        """
        Reset the window
        """
        app.ui.show_main_win()

    def on_help_button_nav_clicked(self, *args, **kwds):
        """
        Open Navigation Help
        """
        app.ui.swap_help_win('nav')

    def on_help_button_play_clicked(self, *args, **kwds):
        """
        Open Gameplay Help
        """
        app.ui.swap_help_win('play')

    def on_help_button_conf_clicked(self, *args, **kwds):
        """
        Open Configuration Help
        """
        app.ui.swap_help_win('config')

    def on_help_button_trophy_clicked(self, *args, **kwds):
        """
        Open Trophy Help
        """
        app.ui.swap_help_win('trophy')

    def on_help_button_man_clicked(self, *args, **kwds):
        """
        Open Full Manual
        """
        app.ui.swap_help_win('man')

    def on_select_by_random_button_clicked(self, *args, **kwds):
        """
        Select a quote at random
        """
        app.worker.game_state.get_quote()
        app.ui.show_main_win()
        self.quote_data = (['testing', 'more testing'], 'This is a test.?!"\'', 'A Tester', False)
        app.ui.set_header_state()
        puzzle_box = app.ui.builder.get_object("puzzle_box")
        children = puzzle_box.get_children()
        #This would be cleaner if there were a .purge() method...
        for child in children:
            puzzle_box.remove(child)
        puzzle_box.pack_start(app.worker.game_state.puzzle_data.algo_work.puzzle_win, False, False, 0)
        puzzle_box.show_all()
        
        solver_box = app.ui.builder.get_object("solver_box")
        children = solver_box.get_children()
        #This would be cleaner if there were a .purge() method...
        for child in children:
            solver_box.remove(child)
        solver_box.pack_start(app.worker.game_state.puzzle_data.algo_work.solver_win, False, False, 0)
        solver_box.show_all()
        
        app.ui.update_status_bar('Thanks for playing...')
        

    def on_select_by_author_button_clicked(self, *args, **kwds):
        """
        Select a quote at random
        """
        print("implement select by author")
        app.worker.game_state.get_quote()
        
    def on_select_by_topic_button_clicked(self, *args, **kwds):
        """
        Select a quote at random
        """
        print("implement select by topic")
        app.worker.game_state.get_quote()
        
    def on_set_letter_selected(self, *args, **kwds):
        """
        """
        app.ui.set_selected(args[0].get_label())
        

class App():
    """
    The class to rule them all
    """
    

    def __init__(self):
        """
        Application code not covered elsewhere
        Extra init routines added to satisfy pylint
        """
        
        self.ui = UI()
        self.ui.init()
        
        self.worker = Worker()
        self.worker.init()

        self.handler = Handler()
        self.handler.init()
        
        self.ui.builder.connect_signals(self.handler)

app = App()

if __name__ == '__main__':
        Gtk.main()
