So, here's the deal. I'm a fan of the [Rubinius open commit policy](http://www.programblings.com/2008/04/15/rubinius-for-the-layman-part-2-how-rubinius-is-friendly/), so like all Self-Appointed-Benevolent-Dicators, this is my only major decree.

What does this mean?

> Anyone who submits a patch which is accepted is granted commit access.


Let me repeat that.

> Anyone who submits a patch which is accepted is granted commit access.

Ok, so anyone, and pretty much anyway. I'd prefer this to be via github, but you can email me a git patch and I'll accept that.




External Requires:
`gi.repository.Gtk`
`bs4`

Standard Requires:
`string`
`random`

Tested on python 2.7.3 and python 3.2.3 on Ubuntu 12.04 LTS.

Works as a portable application just launch the script in ./opt/pyCryptoGame/.

Other directories are just placeholders for packaging/visualization before packaging.

##TODOs


This is the biggest thing:

# Get our existing code under unit tests.

Now, James doesn't know Python, so he's lost when it comes to Python unit testing. If someone can help get the whole testing thing *started*, that'd be great. Otherwise, the following to-dos might get messy.

###Game logic/code
  Quote data back-end
  Help/doc
  Configuration
  By author
  By topic
  Save state
  Trophy system

###User interface
  Drag-and-drop
  Animation for win condition
  Monochrome icons
  *Maybe animations for letter boxes*
  
###Code clean-up

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


Written by Andrew King. James Gifford `<james@jamesrgifford.com>` appointed as maintainer [here](http://chat.stackexchange.com/transcript/message/5783681#5783681), and is released under the BSD license for the world to use, as Andrew wished.