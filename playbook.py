#!/usr/bin/python

import Tkinter as tk
import ttk
import tkMessageBox as mBox

""" playbook.py is a basketball strategy playbook board."""

class MainFrame(tk.Frame):
    
    """Frame class that sets the menu with options for the playbook."""
    
    def __init__(self, parent):
        """A main frame to hold the canvas for the program. parent is the main
        window which is used to determine the title and size of the program.
        """
        
        self.frame = tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Play Book")
        self.width = self.parent.winfo_screenwidth()
        self.height = 720
        self.createMenuBar()
        self.side = ""
        self.mode = "Players Representation Mode"
        self.offenseOn = None
        self.playerRepOn = True
        self.status_bar = self.createStatusBar(self.side, self.mode)
        self.current_screen = PlaybookBoard(self)
        self.message= ["Welcome!", "Help!",
                       """Welcome!
Please choose the player representation you want put down by clicking 'Side'
on the menu bar. Then choose whether you want to place player reps on the
whiteboard or draw lines to show player motion by clicking 'Mode' on the menu
bar. The default mode is player representation which will draw circles on the
board. To see this message again click on help."""]

        # Initial message that helps the user get started with the playbook
        # program.
        self.initial_user_message = mBox.showinfo(self.message[0], self.message[2])
        self.newPlaybookBoard()                                             
              
    def createMenuBar(self):
        """Creates a menu bar with four options file, side, mode, and help."""

        menubar = tk.Menu(self.parent)
        fileMenu = tk.Menu(menubar)
        self.parent.config(menu=menubar)       
        fileMenu = tk.Menu(menubar, tearoff=0)
        sideMenu = tk.Menu(menubar, tearoff=0)
        modeMenu = tk.Menu(menubar, tearoff=0)
        helpMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="New", command=self.newPlaybookBoard,
                             accelerator="Ctrl+N")
        fileMenu.add_command(label="Quit", command=self.quit,
                             accelerator="Ctrl+Q")
        sideMenu.add_command(label="Offense", command=self.sideOffense,
                             accelerator="Ctrl+O")
        sideMenu.add_command(label="Defense", command=self.sideDefense,
                             accelerator="Ctrl+D")
        modeMenu.add_command(label="Player Representation",
                             command=self.modeCircles, accelerator="Ctrl+P")
        modeMenu.add_command(label="Line", command=self.modeLine,
                             accelerator="Ctrl+L")
        helpMenu.add_command(label="Help", command=self.playbookHelp,
                             accelerator="Ctrl+H")
        menubar.add_cascade(label="Menu", menu=fileMenu)
        menubar.add_cascade(label="Side", menu=sideMenu)
        menubar.add_cascade(label="Mode", menu=modeMenu)
        menubar.add_cascade(label="Help", menu=helpMenu)
        self.bind_all("<Control-q>", self.onQuit)
        self.bind_all("<Control-n>", self.onNewPlaybookBoard)
        self.bind_all("<Control-s>", self.onChooseSide)
        self.bind_all("<Control-m>", self.onChooseMode)

    def createStatusBar(self, side, mode):
        """Creates a status bar at the bottom of the frame showing which side
        is being represented and which mode is currently active.
        """
        
        if side == "" and self.playerRepOn:
            self.status_bar = tk.Label(self.parent,
                                       text= "Choose player representation. Default mode is 'Player Representation'.",
                                       width=self.width, relief=tk.SUNKEN,
                                       anchor=tk.W)
        else:
            self.status_bar = tk.Label(self.parent,
                                       text= "Current side: " + side + " , Current Mode: " + mode,
                                       width=self.width, relief=tk.SUNKEN,
                                       anchor=tk.W)
        self.status_bar.pack(side = tk.BOTTOM, fill = tk.BOTH)
        return self.status_bar

    def updateStatusBar(self, side, mode):
        """Updates the status bar with any changes to which side is being
        represented or the mode being used.
        """
        
        self.status_bar.destroy()
        self.status_bar  = self.createStatusBar(side, mode)
        return self.status_bar

    def newPlaybookBoard(self):
        """Sets a new playbook board with the global variables and status bar
        set to their default values.
        """
        self.side = ""
        self.mode = "Players Representation Mode"
        self.offenseOn = None
        self.playerRepOn = True
        self.updateStatusBar(self.side, self.mode)
        self.current_screen.destroy()           
        self.current_screen = PlaybookBoard(self)
        
    def onNewPlaybookBoard(self, key_event):
        """An event handler that calls the newPlaybookBoard method when the
        key_event occurs.
        """
        
        self.newPlaybookBoard()

    def toggleOffenseOn(self, active_side):
        """Toggles the global variable self.offenseOn depending on which side is
        active and updates the status bar.
        """
        
        if active_side.lower() == "offense":
            self.offenseOn = True
        else:
            self.offenseOn = False
        self.updateStatusBar(self.side, self.mode)
        self.current_screen.placeMarkings()

    def togglePlayerRepOn(self, switch):
        """Toggles the variable self.playerRepOn depending whether the switch is
        'on' or 'off'.
        """
        
        if switch.lower() == "on":
            self.playerRepOn = True
        else:
            self.playerRepOn = False
        self.updateStatusBar(self.side, self.mode)
        self.current_screen.placeMarkings()
                    
    def sideOffense(self):
        """Sets the self.side variable to the offense side."""
        
        self.side = "Offense"
        self.toggleOffenseOn(self.side)
             
    def sideDefense(self):
        """Sets the self.side variable to the defense side."""
        
        self.side = "Defense"
        self.toggleOffenseOn(self.side)


    def modeCircles(self):
        """Sets the self.mode variable to 'Players Representation Mode'."""
        
        self.mode = "Players Representation Mode"
        self.togglePlayerRepOn("on")

    def modeLine(self):
        """Sets the self.mode variable to 'Line Mode'."""
        
        self.mode = "Line Mode"
        self.togglePlayerRepOn("off")
        

    def onChooseSide(self, event):
        """An event handler that updates the side when the event occurs."""
        
        if self.offenseOn:
            self.sideDefense()
        else:
            self.sideOffense()

    def onChooseMode(self, event):
        """An event handler that updates the mode when the event occurs."""
        
        if self.playerRepOn:
            self.modeLine()
        else:
            self.modeCircles()
        
    def onQuit(self, event):
        """An event handler that closes the window when the event occurs."""

        self.quit()

    def playbookHelp(self):
        """Displays the message helping the user get started with the playbook
        program.
        """

        initial_user_message = mBox.showinfo(self.message[1], self.message[2])
        
class PlaybookBoard(tk.Canvas):

    """ A blank basketball court playbook board template."""

    def __init__(self, frame):
        """ A playbook board made to fit in the frame."""
        
        self.canvas = tk.Canvas.__init__(self, bg="white")
        self.frame = frame
        self.width = self.frame.width
        self.height = self.frame.height
        self.offense_count = 0
        self.defense_count = 0
        self.offense = StrategyPiece(self, "red")
        self.defense = StrategyPiece(self, "blue")
        self.createCourt(self.width, self.height)
        self.pack(fill=tk.BOTH, expand=1)
        
    def createCourt(self, screen_width, screen_height):
        """Creates a 2-dimensional black and white basketball court bounded by
        the screen_width and screen height.
        """

        # variables used to facilitate the drawing of the court
        
        half_screen = screen_width/2.0
        quarter_screen = screen_width/4.0
        third_of_height = screen_height/3.0
        free_throw_b = screen_height - third_of_height
        free_throw_R = screen_width - quarter_screen
        bounds_L = screen_width/40.0
        bounds_R = screen_width - bounds_L
        bounds_U = screen_height/12.0
        bounds_D = screen_height - bounds_U
        mid_circ_L = screen_width/2.3
        mid_circ_R = screen_width - screen_width/2.3
        three_pt_U = bounds_U + 40
        three_pt_D = bounds_D - 40
        three_pt_start = -screen_width/2.9

        # draws the bounds of the court
        
        out_of_bounds = self.create_rectangle(bounds_L, bounds_U, bounds_R,
                                              bounds_D)

        # draws the half court line and circle
        
        half_court = self.create_line(half_screen, 0, half_screen,
                                      screen_height)
        half_court_circle = self.create_oval(mid_circ_L, third_of_height,
                                             mid_circ_R, free_throw_b)

        # draws the paint for the free throw area on the left side of the
        # screen
        
        paint_L = self.create_rectangle(bounds_L, third_of_height,
                                        quarter_screen, free_throw_b)
        free_throw_aL = self.create_arc(quarter_screen - 100, third_of_height,
                                        mid_circ_L - 150, free_throw_b, extent=180,
                                        start=270, style=tk.ARC)

        # draws the paint for the free throw area on the right side of the
        # screen
        
        paint_R = self.create_rectangle(bounds_R, third_of_height,
                                        free_throw_R, free_throw_b)
        free_throw_aR = self.create_arc(free_throw_R + 100, third_of_height,
                                        mid_circ_R + 150, free_throw_b, extent=180,
                                        start=90, style=tk.ARC)

        # draws the three point arc on the left side of the screen
        
        three_pt_aL = self.create_arc(three_pt_start, three_pt_U , mid_circ_L - 40,
                                      three_pt_D, extent=180, start=270,
                                      style=tk.ARC)

        # draws the three point arc on the right side of the screen
        
        three_pt_aR = self.create_arc(mid_circ_R + 50, three_pt_U ,
                                      screen_width - three_pt_start, three_pt_D,
                                      extent=180, start=90, style=tk.ARC)

    def onCreateMarkers(self, event):
        """ Event handler that calls the createMarkers method from the instance
        of the StrategyPiece class when the event occurs.
        """
        
        if self.frame.offenseOn and self.offense_count < 5:
            self.offense.updatePos(event)
            self.offense.createMarkers()
            self.offense_count += 1
        else:
            if not self.frame.offenseOn and self.defense_count < 5:
                self.defense.updatePos(event)
                self.defense.createMarkers()
                self.defense_count += 1
            else:
                over = mBox.showinfo("Too Many!", "Only 5 players can be represented per side")

        # create a new court so that it seems as if the circles are always
        # above the court lines.
        
        self.createCourt(self.width, self.height)   

    def onErase(self, event):
        """ Event handler that calls the erase method from the instance of
        the StrategyPiece class when the event occurs.
        """
        
        self.offense.updatePos(event)
        self.offense.erase()

        # creates a new court so that it appears as if court lines are not
        # erased

        self.createCourt(self.width, self.height)

    def onDeleteMarking(self, event):
        """ Event handler that calls the deleteMarking method from the instance
        of the StrategyPiece class when the event occurs.
        """
        
        if self.frame.offenseOn and self.offense_count > 0:
            self.offense.deleteMarking()
            self.offense_count -= 1
        elif self.defense_count > 0 and not self.frame.offenseOn:
            self.defense.deleteMarking()
            self.defense_count -= 1
        
    def onCreateLine(self, event):
        """ Event handler that calls the createLine method from the instance
        of the StrategyPiece class when the event occurs.
        """

        # a continuous line is created only when the event is a mouse click
        # motion event
        
        if self.frame.side != "":
            if self.frame.offenseOn:
                self.offense.updatePos(event)
                self.offense.createLine()
            else:
                self.defense.updatePos(event)
                self.defense.createLine()

    def placeMarkings(self):
        """ Creates the markings on the court depending on the key event."""
        
        if self.frame.playerRepOn and self.frame.offenseOn != None:
            self.bind("<Button-1>", self.onCreateMarkers)
            self.bind("<B3-Motion>", self.onErase)
            self.bind_all("<Control-z>", self.onDeleteMarking)
        elif self.frame.playerRepOn == False:
            self.bind("<Button-1>", self.onCreateLine)
            self.bind("<B3-Motion>", self.onErase)
            self.bind("<B1-Motion>", self.onCreateLine)
            self.bind_all("<Control-z>", self.onDeleteMarking)            
        
class StrategyPiece(object):

    """ Object class of the playbook board strategy pieces."""

    def __init__(self, board, piece_color):
        """ A strategy piece set to the color of piece_color and drawn onto the
        playbook board.
        """
        
        self.board = board
        self.piece_color = piece_color
        self.mouse_pos = [0, 0]
        self.clicked_circ = []

    def updatePos(self, event):
        """ Returns the updated position of the click event."""
        
        self.mouse_pos = [int(event.x), int(event.y)]
        return self.mouse_pos
        

    def createMarkers(self):
        """ Draws a circle used to create a marker on the board."""
        
        self.marker_placement = [self.mouse_pos[0] + 20, self.mouse_pos[1] + 20,
                                 self.mouse_pos[0] - 20, self.mouse_pos[1] - 20]
        self.circles = self.board.create_oval(self.marker_placement[0],
                                              self.marker_placement[1],
                                              self.marker_placement[2],
                                              self.marker_placement[3],
                                              fill=self.piece_color)

        # adds the clicked circle to a list to be used later for undoing circles

        self.clicked_circ.append(self.circles)
                 
                

    def createLine(self):
        """ Draws a square used to create a line on the board."""
        
        self.line_placement = [self.mouse_pos[0], self.mouse_pos[1],
                               self.mouse_pos[0] + 10, self.mouse_pos[1] + 10]
        self.line = self.board.create_rectangle(self.line_placement[0],
                                                self.line_placement[1],
                                                self.line_placement[2],
                                                self.line_placement[3],
                                                fill=self.piece_color,
                                                outline=self.piece_color)
    def erase(self):
        """ Draws a square used to erase a mark on the board."""
        
        self.line = self.board.create_rectangle(self.line_placement[0],
                                                self.line_placement[1],
                                                self.line_placement[2],
                                                self.line_placement[3],
                                                fill="white",
                                                outline="white")
    def deleteMarking(self):
        """ Deletes a circle from the board."""
        
        if len(self.clicked_circ) > 0:
            undone_circ = self.clicked_circ.pop()
            self.board.delete(undone_circ)
                                          
def main():

    root = tk.Tk()
    root.geometry("%dx%d" % (root.winfo_screenwidth()-10, 720))

    # sets the maximum size of the window when maximized or resized
    
    root.maxsize(root.winfo_screenwidth(), 720)

    # sets the minimum size of the window when resized
    
    root.minsize(root.winfo_screenwidth()-10, 720)
    app = MainFrame(root)
    root.mainloop()

if __name__ == '__main__':
    main()
    
