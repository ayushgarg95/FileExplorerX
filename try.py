import gtk
import os

#for running any linux command(Ayudh)
import subprocess
from subprocess import call
#ends here

COL_PATH = 0
COL_PIXBUF = 1
COL_IS_DIRECTORY = 2
back_stack = []
forward_stack = []
class PyApp(gtk.Window):
    def __init__(self):
        super(PyApp, self).__init__()

        self.set_size_request(650, 400)
        self.set_position(gtk.WIN_POS_CENTER)

        self.connect("destroy", gtk.main_quit)
        self.set_title("ProjectX")

        self.current_directory = '/'
        

        vbox = gtk.VBox(False, 0);

        #Toolbars for bifurcation
        title_toolbar=gtk.Toolbar()
        vbox.pack_start(title_toolbar, False, False, 0)

        menu_toolbar=gtk.Toolbar()
        vbox.pack_start(menu_toolbar, False, False, 0)
         

        #ends here

        toolbar = gtk.Toolbar()
        vbox.pack_start(toolbar, False, False, 0)

        self.upButton = gtk.ToolButton(gtk.STOCK_GO_UP);
        self.upButton.set_is_important(True)
        self.upButton.set_sensitive(False)
        toolbar.insert(self.upButton, -1)

        homeButton = gtk.ToolButton(gtk.STOCK_HOME)
        homeButton.set_is_important(True)
        toolbar.insert(homeButton, -1)

        # Back and Forward buttons
        self.backButton = gtk.ToolButton(gtk.STOCK_GO_BACK)
        self.backButton.set_is_important(True)
        self.backButton.set_sensitive(False)
        toolbar.insert(self.backButton, -1)

        self.forwardButton = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        self.forwardButton.set_is_important(True)
        self.forwardButton.set_sensitive(False)
        toolbar.insert(self.forwardButton, -1)


        #ends here



        #search bar(Ayudh)
        
        self.searchfile=gtk.Entry()
        self.searchfile.set_text("Search")
        item = gtk.ToolItem()
        item.add(self.searchfile)
        toolbar.insert(item, -1)
        

        searchButton = gtk.ToolButton(gtk.STOCK_FIND)
        searchButton.set_is_important(True)
        toolbar.insert(searchButton, -1)



        #ends here

        self.fileIcon = self.get_icon(gtk.STOCK_FILE)
        self.dirIcon = self.get_icon(gtk.STOCK_DIRECTORY)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw, True, True, 0)

        self.store = self.create_store()
        self.fill_store()

        # Right Click Popup menu

        rightClickMenu = gtk.Menu()
        item1 = gtk.MenuItem("ITEM 1")
        rightClickMenu.append(item1)

        item2 = gtk.MenuItem("ITEM 2")
        rightClickMenu.append(item2)
        item1.show()
        item2.show()

        rightClickMenu.show()
        eventbox = gtk.EventBox()
        eventbox.connect_object("button-press-event", self.on_button_press_event,rightClickMenu)
        
        
        # RIght Click ends


        iconView = gtk.IconView(self.store)
        iconView.set_selection_mode(gtk.SELECTION_MULTIPLE)

        self.upButton.connect("clicked", self.on_up_clicked)
        homeButton.connect("clicked", self.on_home_clicked)
        self.backButton.connect("clicked", self.on_back_clicked)
        self.forwardButton.connect("clicked", self.on_forward_clicked)

        iconView.set_text_column(COL_PATH)
        iconView.set_pixbuf_column(COL_PIXBUF)

        iconView.connect("item-activated", self.on_item_activated)
        # extra 
        eventbox.add(iconView)
        sw.add_with_viewport(eventbox)

        # extra ends
        iconView.grab_focus()

        self.add(vbox)
        self.show_all()

    def get_icon(self, name):
        theme = gtk.icon_theme_get_default()
        return theme.load_icon(name, 48, 0)


    def create_store(self):
        store = gtk.ListStore(str, gtk.gdk.Pixbuf, bool)
        store.set_sort_column_id(COL_PATH, gtk.SORT_ASCENDING)
        return store


    def fill_store(self):
        self.store.clear()

        if self.current_directory == None:
            return

        for fl in os.listdir(self.current_directory):

            if not fl[0] == '.':
                if os.path.isdir(os.path.join(self.current_directory, fl)):
                    self.store.append([fl, self.dirIcon, True])
                else:
                    self.store.append([fl, self.fileIcon, False])



    def on_home_clicked(self, widget):
        self.current_directory = os.path.realpath(os.path.expanduser('~'))
        self.fill_store()
        self.upButton.set_sensitive(True)

# back and fwd functions
    def on_back_clicked(self, widget):
        
        forward_stack.append(self.current_directory)
        self.current_directory = back_stack.pop()
        if not back_stack:
            self.backButton.set_sensitive(False) 
        self.forwardButton.set_sensitive(True)
        self.fill_store()
        self.upButton.set_sensitive(True)  

    def on_forward_clicked(self, widget):
        
        back_stack.append(self.current_directory)
        self.current_directory = forward_stack.pop()
        if not forward_stack:
            self.forwardButton.set_sensitive(False) 
        self.backButton.set_sensitive(True)
        self.fill_store()
        self.upButton.set_sensitive(True)         
#end here

    def on_item_activated(self, widget, item):

        model = widget.get_model()
        path = model[item][COL_PATH]
        isDir = model[item][COL_IS_DIRECTORY] 

        # opens a file withs its default preferred application(Ayudh)
        if not isDir:
            subprocess.call(["xdg-open",self.current_directory +"/"+path])  
            return
        #ends here   
 
        # back and forward implementation
        back_stack.append(self.current_directory)
        forward_stack[:]= []
        self.forwardButton.set_sensitive(False)
        self.backButton.set_sensitive(True)
        self.current_directory = self.current_directory + os.path.sep + path
        self.fill_store()
        self.upButton.set_sensitive(True)
        #ends

    def on_up_clicked(self, widget):
        self.current_directory = os.path.dirname(self.current_directory)
        self.fill_store()
        sensitive = True
        if self.current_directory == "/": sensitive = False
        self.upButton.set_sensitive(sensitive)

    def on_button_press_event(self, widget, event):
            # Check if right mouse button was preseed
            if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
                print "HI"
                widget.popup(None, None, None, event.button, event.time)
                widget.grab_focus()
                return True # event has been handled

PyApp()


PyApp()
gtk.main()
