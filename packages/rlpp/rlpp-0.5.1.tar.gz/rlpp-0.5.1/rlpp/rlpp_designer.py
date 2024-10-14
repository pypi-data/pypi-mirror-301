from rlpp.constants import *
from rlpp.mainUI import Ui_MainWindow
class PygameEmbed(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainUI = Ui_MainWindow() #Create the UI components
        self.mainUI.setupUi(self) #initialize the UI components
        # self.objectManager = DesignerObjectManager() #Create the main object that will contain the information on the game objects
        # Set a timer to update the Pygame display in the QLabel
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: objectManager.update_pygame(self.mainUI.label))
        self.timer.start(30)  # Update at approximately 30 FPS
        self.setFixedSize(937, 559)  # Width: 400, Height: 300
        # connect buttons
        self.mainUI.pushButton_21.clicked.connect(lambda: objectManager.create_new_gameObject(self.mainUI.pushButton_21.img_path_name,"agent", reset_mode=True))
        self.mainUI.pushButton_18.clicked.connect(lambda: objectManager.create_new_gameObject(self.mainUI.pushButton_18.img_path_name,"wall", reset_mode=True))
        self.mainUI.pushButton_17.clicked.connect(lambda: objectManager.create_new_gameObject(self.mainUI.pushButton_17.img_path_name,"enemy", reset_mode=True))
        self.mainUI.pushButton_24.clicked.connect(lambda: objectManager.create_new_gameObject(self.mainUI.pushButton_24.img_path_name,"food", reset_mode=True))
        
        self.mainUI.pushButton_20.clicked.connect(lambda: self.importNewGameObject(self.mainUI.scrollArea_8, "agent"))
        self.mainUI.pushButton_11.clicked.connect(lambda: self.importNewGameObject(self.mainUI.scrollArea_5, "wall"))
        self.mainUI.pushButton_16.clicked.connect(lambda: self.importNewGameObject(self.mainUI.scrollArea_7, "enemy"))
        self.mainUI.pushButton_23.clicked.connect(lambda: self.importNewGameObject(self.mainUI.scrollArea_9, "food"))
        
        # buttons related to current_gameObject select from the ObjectManager
        self.mainUI.pushButton.clicked.connect(lambda: self.set_cursor_mode("SELECT"))
        self.mainUI.pushButton_2.clicked.connect(lambda: self.set_cursor_mode("STAMP"))
        self.mainUI.pushButton_5.clicked.connect(lambda: self.set_cursor_mode("MOVE"))
        self.mainUI.pushButton_3.clicked.connect(lambda: self.set_cursor_mode("TRASH"))
        self.mainUI.pushButton_4.clicked.connect(lambda: self.set_cursor_mode("TURN"))
        
        # Key shortcut behaviors
        # Create a shortcut for Escape and connect it to a custom function
        self.shortcut_undo = QShortcut(QKeySequence("Escape"), self)
        self.shortcut_undo.activated.connect(lambda: self.set_cursor_mode("SELECT"))
        
        # keep track of the last location where the user is working
        self.last_directory = RESOURCES_PATH
    
    def set_cursor_mode(self,mode):
        if mode == "SELECT":
            objectManager.current_go = None
            cursor_settings["MODE"] = mode
        elif mode == "STAMP":
            cursor_settings["MODE"] = mode
        elif mode == "MOVE":
            cursor_settings["MODE"] = mode
        elif mode == "TRASH" and objectManager.current_go != None:
            objectManager.remove_current_gameObject()
        elif mode == "TURN" and objectManager.current_go != None:
            objectManager.current_go.turnClockwise()
        
        
    # Create a new button for a given menu and category: agents, walls, enemies or foods
    def importNewGameObject(self, scrollArea, game_object_type):
        # Open a file dialog to select an image
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", self.last_directory, 
                                                    "Images (*.png *.jpg *.jpeg);;All Files (*)", 
                                                    options=options)
        if file_name:
            self.last_directory = os.path.dirname(file_name)
            self.mainUI.createNewButton(file_name,scrollArea, game_object_type)
        
    def mousePressEvent(self, event):
        """Start drawing when the mouse is pressed."""
        # if cursor is in widget display, and left button and there's a game object to place, append it to its corresponding list and reset
        if cursor_settings["INDISPLAY"] and event.button() == Qt.LeftButton:
            if (cursor_settings["MODE"] == "" or cursor_settings["MODE"] == "STAMP") and objectManager.current_go is not None:
                objectManager.processCurrentObject()
            elif cursor_settings["MODE"] == "SELECT":
                objectManager.getObjectClicked()
            elif cursor_settings["MODE"] == "MOVE" and objectManager.current_go is not None:
                objectManager.current_go.placed = not objectManager.current_go.placed
            # elif cursor_settings["MODE"] == "TURN" and objectManager.current_go is not None:
                # objectManager.current_go.turnClockwise()
    
    def wheelEvent(self, event):
        """Handle mouse scroll events."""
        if cursor_settings["INDISPLAY"] and objectManager.current_go is not None:
            delta = event.angleDelta().y()  # Get the vertical scroll amount
            if delta > 0:
                objectManager.current_go.scale(abs( cursor_settings["RESIZESENS"]))
            elif delta < 0:
                objectManager.current_go.scale(-abs( cursor_settings["RESIZESENS"]))

    
def main():
    # Enable High DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # Use the high-resolution icons and fonts
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    window = PygameEmbed()
    window.show()
    sys.exit(app.exec_())
        
if __name__ == "__main__":
    main()
