import sys
import os
import urllib.parse
import vlc
import queue
# from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
# from PySide6.QtGui import QPalette, QColor

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *


from AppCode import *

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("IMP - Itchy Music Player Ver 0.1.0")
        placeholder_VerticalLayout = QVBoxLayout()
        centerVerticalAlignmentLayout = QVBoxLayout()
        rightplaceholder_verticalLayout = QVBoxLayout()
        flow_layout = FlowLayout()
        playlist_layout = FlowLayout()
        individualPlaylistViewerLayout = QVBoxLayout()
        # TagsLayout = QVBoxLayout()
        QueueLayout = QVBoxLayout()

        onStartHashCheck()
        # onStartPlaylistsCheck()

        #MainLayout
        MainLayout = QHBoxLayout()

        #Placeholder image
        placeholderimage = "placeholder.jpg"

        #Initialize Current Playlist and lastmediachange for playlist functionality
        CurrentPlaylist = [None]
        lastMediaChange = [None]

        #Initializes Current IPV for refresh functionality
        #It is in a list so that when assigning it in PlaylistTiles it updates the main IPV variable (mutables updates, but regular assignment doesn't)
        CurrentIPV = [None]

        QueueActive = [False]

        #Initialize PlaylistObjects for the PlayListTileCreationMainWindow function
        #Actually a dictionary lmao
        PlaylistObjectsList = {}

        #PlayerController initialization and listener activations
        #How this works: We initialize an instance of PlayerController as self.controller. We then assign the player created in the __init__ function to player.
        #After that we assign the player's event manager to events. We then attach listeners to events (the event manager), and when the listeners are triggered, we do
        #something according to the function of the same name in PlayerController.
        self.controller = PlayerController(CurrentPlaylist, lastMediaChange, PlaylistObjectsList, QueueActive)

        player = self.controller.player
        events = player.event_manager()

        events.event_attach(vlc.EventType.MediaPlayerPlaying, self.controller.on_playing)
        events.event_attach(vlc.EventType.MediaPlayerPaused, self.controller.on_paused)
        events.event_attach(vlc.EventType.MediaPlayerStopped, self.controller.on_stopped)
        events.event_attach(vlc.EventType.MediaPlayerEndReached, self.controller.on_end)
        events.event_attach(vlc.EventType.MediaPlayerMediaChanged, self.controller.on_media_changed)



        #ProgressBar
        #Scuffed BS Lmao (use the playercontroller to make the bar, then add the bar to the playercontroller)
        Bar = ProgressBar(self.controller)
        self.controller.bar = Bar

        Queue = MusicQueue(QueueActive, QueueLayout, self.controller)
        self.controller.Queue = Queue

        #Attached here so that controller.bar has a value
        events.event_attach(vlc.EventType.MediaPlayerMediaChanged, self.controller.bar.ProgressBarMediaChange)

        #Makes a variable that can be passed to functions that need access to self.controller
        passingcontroller = self.controller

        #Update flow layout with CompactMusicTiles
        updated_flow_layout = CompactTileCreationMainWindow(flow_layout, placeholderimage, passingcontroller)

        #Update playlist layout with PlaylistTiles
        updated_playlist_layout = PlayListTileCreationMainWindow(playlist_layout, placeholderimage, individualPlaylistViewerLayout, passingcontroller, CurrentPlaylist, PlaylistObjectsList, CurrentIPV)
        
        # updated_tags_layout = TagPageTileCreationMainWindow(TagsLayout, placeholderimage)
        # updated_tags_layout = TagsLayout
        # tagtiles = TagsPageTiles(TagsLayout)
        # updated_tags_layout = TagsLayout

        updated_queue_layout = QueueLayout

        OrganizeAlphabeticallyButton = QPushButton("Organize Library Alphabetically")
        OrganizeAlphabeticallyButton.clicked.connect(lambda: OrganizeMusicTagsAlphabetically())

        #RefreshFlowLayout
        RefreshButton = QPushButton("Refresh Library")
        RefreshButton.clicked.connect(lambda: RefreshFlowLayout(flow_layout, placeholderimage, passingcontroller))

        #RefreshPlaylistLayout
        RefreshPlaylist = QPushButton("Refresh Playlists")
        RefreshPlaylist.clicked.connect(lambda: RefreshPlaylistsLayout(playlist_layout, placeholderimage, individualPlaylistViewerLayout, passingcontroller, CurrentPlaylist, PlaylistObjectsList, CurrentIPV))


        # #RefreshTagsLayout
        # RefreshTags = QPushButton("Refresh Tags")


        #For adding a scrollbar to flowlayout
        centerwidget = QWidget()
        centerwidget.setLayout(updated_flow_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(centerwidget)

        #For adding a scrollbar to playlistLayout
        playlistCenterWidget = QWidget()
        playlistCenterWidget.setLayout(updated_playlist_layout)

        playlistScroll = QScrollArea()
        playlistScroll.setWidgetResizable(True)
        playlistScroll.setWidget(playlistCenterWidget)

        # #For adding a scrollbar to TagsLayout
        # tagsCenterWidget = QWidget()
        # tagsCenterWidget.setLayout(updated_tags_layout)

        # tagsScroll = QScrollArea()
        # tagsScroll.setWidgetResizable(True)
        # tagsScroll.setWidget(tagsCenterWidget)

        #For adding a scollbar to QueueLayout
        QueueCenterWidget = QWidget()
        QueueCenterWidget.setLayout(updated_queue_layout)

        QueueScroll = QScrollArea()
        QueueScroll.setWidgetResizable(True)
        QueueScroll.setWidget(QueueCenterWidget)


        #Buttons on the left
        libraryButton = QPushButton("Library")
        playListsButton = QPushButton("Playlists")
        # tagsButton = QPushButton("Tags")
        QueueButton = QPushButton("Queue")
        
        #Button Layout customization
        buttonLayout = QVBoxLayout()
        buttonLayout.setSpacing(40)
        buttonLayout.addWidget(libraryButton)
        buttonLayout.addWidget(playListsButton)
        # buttonLayout.addWidget(tagsButton)
        buttonLayout.addWidget(QueueButton)


        placeholder_VerticalLayout.addStretch(20)
        placeholder_VerticalLayout.addLayout(buttonLayout, 0)
        placeholder_VerticalLayout.addStretch(80)


        #Middle Stacked Layout
        middleStackedLayout = QStackedLayout()

        #The tabbed pages
        # libraryPage = scroll
        libraryPage = QVBoxLayout()
        libraryPage.addWidget(RefreshButton, 1)
        libraryPage.addWidget(OrganizeAlphabeticallyButton, 1)
        libraryPage.addWidget(scroll, 16)
        StackedLayoutlibraryPage = QWidget()
        StackedLayoutlibraryPage.setLayout(libraryPage)

        # playlistsPage = playlistScroll
        playlistsPage = QVBoxLayout()
        playlistsPage.addWidget(RefreshPlaylist)
        playlistsPage.addWidget(InputableButton("Create Playlist", CreatePlaylist, []))
        playlistsPage.addWidget(playlistScroll, 1)
        StackedLayoutplaylistsPage = QWidget()
        StackedLayoutplaylistsPage.setLayout(playlistsPage)

        # tagsPage = QVBoxLayout()
        # tagsPage.addWidget(RefreshTags, 1)
        # tagsPage.addWidget(tagsScroll, 8)
        # StackedLayoutTagsPage = QWidget()
        # StackedLayoutTagsPage.setLayout(tagsPage)

        QueuePage = QVBoxLayout()
        QueuePage.addWidget(QueueScroll, 8)
        StackedQueuePage = QWidget()
        StackedQueuePage.setLayout(QueuePage)


        #Add the pages to the stackedlayout
        middleStackedLayout.addWidget(StackedLayoutlibraryPage)
        middleStackedLayout.addWidget(StackedLayoutplaylistsPage)
        # middleStackedLayout.addWidget(StackedLayoutTagsPage)
        middleStackedLayout.addWidget(StackedQueuePage)

        #Connect the buttons to the pages (current implementation doesn't have the possibility for tags for playlists,
        #so some refactoring would need to be done if we wanted to do that)
        libraryButton.clicked.connect(lambda: middleStackedLayout.setCurrentWidget(StackedLayoutlibraryPage))
        playListsButton.clicked.connect(lambda: middleStackedLayout.setCurrentWidget(StackedLayoutplaylistsPage))
        # tagsButton.clicked.connect(lambda: middleStackedLayout.setCurrentWidget(StackedLayoutTagsPage))
        QueueButton.clicked.connect(lambda: middleStackedLayout.setCurrentWidget(StackedQueuePage))
        QueueButton.clicked.connect(lambda: Queue.Refresh())

        #Adds scrollablewindow and playback bar
        
        centerVerticalAlignmentLayout.addStretch(1)
        centerVerticalAlignmentLayout.addLayout(middleStackedLayout, 36)
        centerVerticalAlignmentLayout.addWidget(Bar, 6)
        Bar.hide()

        #Right Stacked Layout
        rightStackedLayout = QStackedLayout()


        tagsSearchPage = QLabel()
        # individualPlaylistViewerPage = QLabel("This is the IPV page")
        individualPlaylistViewerPage = QWidget()
        individualPlaylistViewerPage.setLayout(individualPlaylistViewerLayout)

        # tagsManagementPage = TagsPageSideView()
        QueueSidePage = QLabel()

        libraryButton.clicked.connect(lambda: rightStackedLayout.setCurrentWidget(tagsSearchPage))
        playListsButton.clicked.connect(lambda: rightStackedLayout.setCurrentWidget(individualPlaylistViewerPage))
        # tagsButton.clicked.connect(lambda: rightStackedLayout.setCurrentWidget(tagsManagementPage))
        QueueButton.clicked.connect(lambda: rightStackedLayout.setCurrentWidget(QueueSidePage))

        rightStackedLayout.addWidget(tagsSearchPage)
        rightStackedLayout.addWidget(individualPlaylistViewerPage)
        # rightStackedLayout.addWidget(tagsManagementPage)
        rightStackedLayout.addWidget(QueueSidePage)

        rightplaceholder_verticalLayout.addLayout(rightStackedLayout)

        MainLayout.addLayout(placeholder_VerticalLayout, 1)
        MainLayout.addLayout(centerVerticalAlignmentLayout, 6)
        MainLayout.addLayout(rightplaceholder_verticalLayout, 1)

        # print(PlaylistObjectsList[0].testvar)
        print(PlaylistObjectsList)

        dump_widget_stats(tag="Initial Widget Number")

        widget = QWidget()
        widget.setLayout(MainLayout)
        self.setCentralWidget(widget)

def CompactTileCreationMainWindow(flow_layout, placeholderimage, controller):
    Jsondata = fetchJson("MusicTags")

    for hash in Jsondata:
        titleName, ext = os.path.splitext(Jsondata[hash]["filepath"])
        joinedTags = ", ".join(Jsondata[hash]["tags"])
        newTile = CompactMusicTiles(placeholderimage, titleName, ext, joinedTags, controller, hash, flow_layout, ["Add to Playlist", "Add to Queue", "Rename", "Delete"])
        flow_layout.addWidget(newTile)

    return flow_layout

def ClearLayout(layout):

    #Stuff breaks if you don't verify it exists first
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                sub_layout = item.layout()
                if sub_layout is not None:
                    ClearLayout(sub_layout)
                    sub_layout.setParent(None)

def RefreshFlowLayout(flow_layout, placeholderimage, passingcontroller):
    
    ClearLayout(flow_layout)

    dump_widget_stats(tag="Before Refresh")

    onStartHashCheck()

    dump_widget_stats(tag="After Refresh")
    
    #Stops Everything from exploding if refreshed (active_tile would be a non-existant object and therefore throw an error when you try to play or stop anything after refreshing)
    passingcontroller.stop()
    passingcontroller.active_tile = None

    
    flow_layout = CompactTileCreationMainWindow(flow_layout, placeholderimage, passingcontroller)
    # flow_layout.addWidget(RefreshButton, 1)

def RefreshPlaylistsLayout(playlist_layout, placeholderimage, individualPlaylistViewerLayout, controller, CurrentPlaylist, PlaylistObjectsList, CurrentIPV):


    # onStartPlaylistsCheck()

    # print()
    # print("Current IPV")
    # print(CurrentIPV)
    # print()
    # if CurrentIPV[0] != None:
    #     CurrentIPV[0].Refresh()
    #     print()
    #     print("Refreshed IPV")
    #     print()

    
    #Plan
    #Get the activated button's playlist from CurrentIPV
    #Get the PlaylistTileObject from PlaylistTileObjectsDict
    #Trigger the on_toggle function with 


    dump_widget_stats(tag="Before Refresh")
    ClearLayout(playlist_layout)

    playlist_layout = PlayListTileCreationMainWindow(playlist_layout, placeholderimage, individualPlaylistViewerLayout, controller, CurrentPlaylist, PlaylistObjectsList, CurrentIPV)
    dump_widget_stats(tag="After Refresh")
    # print()
    # print("Current IPV")
    # print(CurrentIPV)
    # print()
    # if CurrentIPV[0] != None:
    #     CurrentIPV[0].Refresh()
    #     print()
    #     print("Refreshed IPV")
    #     print()
    if CurrentIPV[0] != None:
        ClearLayout(individualPlaylistViewerLayout)
        CurrentIPV[0] = None

    #Need this otherwise the exclusivity logic in PlaylistTiles throws a fit
    PlaylistTiles.active_button = None
    controller.stop()

    # playlist_layout.addWidget(RefreshButtonPlaylist, 1)

def PlayListTileCreationMainWindow(playlist_layout, placeholderimage, individualPlaylistViewerLayout, controller, CurrentPlaylist, PlaylistObjectsList, CurrentIPV):
    Jsondata = fetchJson("Playlists")


    for playlist in Jsondata:
        newPlaylistTile = PlaylistTiles(placeholderimage, playlist, individualPlaylistViewerLayout, CurrentPlaylist, PlaylistObjectsList, CurrentIPV, playlist_layout, controller, ["Rename", "Add to Queue", "Delete",])
        playlist_layout.addWidget(newPlaylistTile)

        newPlaylistObject = PlaylistIndexHolder(playlist)
        # PlaylistObjectsList.append(newPlaylistObject)

        #Assigning it to a dictionary
        PlaylistObjectsList[playlist] = newPlaylistObject

        print()
        print("PlayListTileCreationMainWindow log")
        print(playlist)
        print(newPlaylistObject)
        print()

        newPlaylistObject.valueChanged.connect(lambda val, object=newPlaylistObject: controller.PlaylistChangeHandler(object))

    return playlist_layout        


class PlaylistIndexHolder(QObject):
    valueChanged = Signal(int)

    def __init__(self, playlistName):

        #Very bigly important, so that we can properly initialize the QObject (or something)
        super().__init__()  

        self.name = playlistName

        # PlaylistData = fetchJson("Playlists")
        # currentPlayList = PlaylistData[playlistName]

        # self.currentsongplaying = None

        #CurrentSongPlaying
        self._value = None

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        print()
        print("PlaylistIndexHolderValues")
        print(self._value)
        print(new_value)
        print()

        if new_value != self._value:
            self._value = new_value
            self.valueChanged.emit(new_value)
            print()
            print("Emmited new value: " + str(new_value))
            print()

class PlaylistTiles(QWidget):
    active_button = None  

    def __init__(self, image_path, title, individualPlaylistViewerLayout, CurrentPlaylist, PlaylistObjectsList, CurrentIPV, playlist_layout, controller, dropdown_items=None, parent=None):
        super().__init__(parent)

        self.CurrentIPV = CurrentIPV

        self.title = title
        self.individualPlaylistViewerLayout = individualPlaylistViewerLayout
        self.CurrentPlaylist = CurrentPlaylist
        self.PlaylistObjectsList = PlaylistObjectsList
        self.dropdown_items = dropdown_items
        self.playlist_layout = playlist_layout
        self.image_path = image_path
        self.controller = controller

        #Taken mostly from CompactMusicTiles
        #Left to Right
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)


        #Image
        self.ImageIcon = QPushButton()
        pixmap = QPixmap(image_path).scaled(64, 64)
        self.ImageIcon.setIcon(QIcon(pixmap))   
        self.ImageIcon.setIconSize(QSize(64, 64))  
        layout.addWidget(self.ImageIcon)

        self.ImageIcon.setCheckable(True)
        self.ImageIcon.clicked.connect(lambda checked, button=self.ImageIcon, image_path=image_path, title=title, individualPlaylistViewerLayout=individualPlaylistViewerLayout, CurrentPlayList=CurrentPlaylist,
                                       PlaylistObjectsList=PlaylistObjectsList: self.on_toggle(checked, button, image_path, title, individualPlaylistViewerLayout, CurrentPlayList, PlaylistObjectsList) )


        #Center Text
        text_layout = QVBoxLayout()

        #Center Text - Title
        self.title_label = QLabel()
        self.title_label.setFixedWidth(150)
        ElideText(self.title_label, self.title)

        # title_fm = QFontMetrics(self.title_label.font())


        # title_elided_text = title_fm.elidedText(title, Qt.ElideRight, self.title_label.width())

        # self.title_label.setText(title_elided_text)

        # title_text_width = title_fm.horizontalAdvance(title)
        # title_label_width = self.title_label.width()

        # if title_text_width > title_label_width:
        #     self.title_label.setToolTip(title)
        # else:
        #     self.title_label.setToolTip("")

        #Center Text - Add to Main Widget
        text_layout.addWidget(self.title_label)
        layout.addLayout(text_layout)

        #Play Button (Have it call something called playplaylist, with a ui that appear on the right sidebar)

        #Menu
        self.menuButton = QPushButton("⋮")
        self.menu = QMenu(parent=self)
        self.menu.aboutToShow.connect(self.populateMenu)
        self.menu.aboutToHide.connect(self.clearMenu)


        self.menuButton.setMenu(self.menu)
        
        layout.addWidget(self.menuButton)

        layout.addStretch()

    def on_toggle(self, checked: bool, button, image_path: str, title: str, individualPlaylistViewerLayout, CurrentPlaylist, PlaylistObjectsList):

        if checked:

            # ClearLayout(individualPlaylistViewerLayout)
            # individualPlaylistViewerLayout = individualPlaylistViewer(image_path, title, individualPlaylistViewerLayout)
            # print("checked")
            if PlaylistTiles.active_button and PlaylistTiles.active_button is not button:
                PlaylistTiles.active_button.setChecked(False)

            PlaylistTiles.active_button = button

            ClearLayout(individualPlaylistViewerLayout)
            self.CurrentIPV[0] = individualPlaylistViewer(image_path, title, individualPlaylistViewerLayout, CurrentPlaylist, PlaylistObjectsList, self.controller)
            print()
            print("checked")
            print("Current IPV")
            print(self.CurrentIPV)
            print()

        else:

            # ClearLayout(individualPlaylistViewerLayout)

            if PlaylistTiles.active_button is button:
                PlaylistTiles.active_button = None

            self.CurrentIPV[0] = None
            ClearLayout(individualPlaylistViewerLayout)
            print("unchecked (no selection)")

    def populateMenu(self):
        self.clearMenu()

        for item in self.dropdown_items:
                
                # action = self.menu.addAction(item)
    
            if item == "Rename":
                RenameButton = InputableButton("Rename", RenamePlaylist, [self.title, self.playlist_layout, self.image_path, self.individualPlaylistViewerLayout, self.controller, self.CurrentPlaylist, self.PlaylistObjectsList, self.CurrentIPV])
                RenameAction = QWidgetAction(self.menu)
                RenameAction.setDefaultWidget(RenameButton)
                self.menu.addAction(RenameAction)

            if item == 'Add to Queue':
                AddtoQueueButton = QPushButton(item)
                AddtoQueueButton.clicked.connect(lambda checked=False, PlaylistName=self.title: AddtoQueueFromPlaylist(PlaylistName))
                AddtoQueueAction = QWidgetAction(self.menu)
                AddtoQueueAction.setDefaultWidget(AddtoQueueButton)
                self.menu.addAction(AddtoQueueAction)


            if item == 'Delete':
                DeleteMenu = QMenu(item, parent=self.menu)
                Deletebutton = QPushButton("Delete")
                Deletebutton.clicked.connect(lambda Checked=False, PlaylistName=self.title, playlist_layout=self.playlist_layout, placeholderimage=self.image_path, 
                                             individualPlaylistViewerLayout=self.individualPlaylistViewerLayout, controller=self.controller, CurrentPlaylist=self.CurrentPlaylist, PlaylistObjectsList=self.PlaylistObjectsList, CurrentIPV=self.CurrentIPV: 
                                             DeletePlaylist(PlaylistName, playlist_layout, placeholderimage, individualPlaylistViewerLayout, controller, CurrentPlaylist, PlaylistObjectsList, CurrentIPV))
                DeleteAction = QWidgetAction(DeleteMenu)
                DeleteAction.setDefaultWidget(Deletebutton)
                DeleteMenu.addAction(DeleteAction)
                self.menu.addMenu(DeleteMenu)

            

    def clearMenu(self):
        self.menu.clear()

class individualPlaylistViewer(QWidget):

    def __init__(self, image_path, title, individualPlaylistViewerLayout, CurrentPlaylist, PlaylistObjectsList, controller):
        super().__init__()
    

        self.image_path = image_path
        self.title = title
        self.individualPlaylistViewerLayout = individualPlaylistViewerLayout
        self.PlaylistObjectsList = PlaylistObjectsList
        self.CurrentPlaylist = CurrentPlaylist
        self.controller = controller

        # self.container = QVBoxLayout()
        # self.setLayout(self.container)
        # self.individualPlaylistViewerLayout.addWidget(self)

        self.container = QVBoxLayout()
        self.individualPlaylistViewerLayout.addLayout(self.container)
        # self.setLayout(self.container)

        self.build_ui()

    def build_ui(self):

        playlistJsondata = fetchJson("Playlists")
        MusicTagsJsondata = fetchJson("MusicTags")


        # self.container.addStretch(1)

        image_label = QLabel()
        pixmap = QPixmap(self.image_path)
        image_label.setPixmap(pixmap.scaled(64, 64))
        self.container.addWidget(image_label, alignment=Qt.AlignCenter)



        #Prevents adding a start button to an empty playlist
        if len(playlistJsondata[self.title]) > 0:
            StartPlaylistButton = QPushButton("Start Playlist")
            StartPlaylistButton.clicked.connect(lambda checked=False: setattr(self.PlaylistObjectsList[self.title], "value", 0))
            self.container.addWidget(StartPlaylistButton, alignment=Qt.AlignCenter)



        SideButtonsVBox = QVBoxLayout()

        for items in range(len(playlistJsondata[self.title])):
            
            TemporaryHBoxLayout = QHBoxLayout()
            print()
            print("items")
            print(items)
            print(playlistJsondata[self.title][items])
            print()


            if playlistJsondata[self.title][items] in MusicTagsJsondata:

                songname = QLabel()
                songname.setFixedWidth(300)

                ElideText(songname, MusicTagsJsondata[playlistJsondata[self.title][items]]["filepath"])
    
                SetPlaylistPositionButton = QPushButton(str(items + 1))

                # i = items so that i is forced to be different for each connection, otherwise it would just be the last made one
                # checked=False in order to make sure that checked isn't fed into the i arguement in setattr
                SetPlaylistPositionButton.clicked.connect(lambda checked=False, i=items: setattr(self.PlaylistObjectsList[self.title], "value", i))
                SetPlaylistPositionButton.clicked.connect(lambda checked=False: self.SetQueueToNone())
                TemporaryHBoxLayout.addWidget(SetPlaylistPositionButton)
                            
            else:
                songname = QLabel()
                songname.setText("Unknown Song")


            TemporaryHBoxLayout.addWidget(songname)


            RemoveSongButton = QPushButton("X")
            RemoveSongButton.clicked.connect(lambda checked=False, PlaylistName=self.title, Index=items:RemoveFromPlaylistIPV(PlaylistName, Index))
            RemoveSongButton.clicked.connect(lambda checked=False: self.Refresh())
            TemporaryHBoxLayout.addWidget(RemoveSongButton)

            ReOrderButton = InputableButton("Change Order", ChangePlaylistOrder, [self.title, items, self])
            TemporaryHBoxLayout.addWidget(ReOrderButton)

            SideButtonsVBox.addLayout(TemporaryHBoxLayout)

        SideButtonsVBox.addStretch(1)
        IPVWidget = QWidget()
        IPVWidget.setLayout(SideButtonsVBox)
        # IPVWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        IPVScroll = QScrollArea()
        IPVScroll.setWidgetResizable(True)
        IPVScroll.setMinimumWidth(IPVWidget.width())
        print()
        print("IPV Widget width")
        print(IPVWidget.width())
        print()
        IPVScroll.setWidget(IPVWidget)
        # IPVScroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # IPVScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # IPVScrollLayout = QVBoxLayout()
        # IPVScrollLayout.addWidget(IPVScroll)

        self.container.addWidget(IPVScroll)
        # self.container.addLayout(IPVScrollLayout)
        # self.container.addLayout(SideButtonsVBox)
        # self.container.addStretch(10)


    #Kind of Vestigial right now, not used for anything. Maybe something in the future
    def Refresh(self):

        ClearLayout(self.container)
        self.build_ui()

    def SetQueueToNone(self):

        self.controller.lastMediaChange[0] = 'PlaylistChangeHandler'
        self.controller.QueueActive[0] = False


class CompactMusicTiles(QWidget):

    def __init__(self, image_path: str, title: str, extension: str, subtitle: str, controller, hash, flow_layout, dropdown_items=None, parent=None):
        super().__init__(parent)

        # #vlc
        # self.vlc_instance = vlc.Instance("--no-xlib --no-video")
        # self.player = None
        self.controller = controller
        self.PlaylistData = fetchJson("Playlists")

        self.title = title
        self.extension = extension
        self.flowlayout = flow_layout
        self.placeholderimage = image_path
        self.dropdown_items = dropdown_items

        #Left to Right
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        self.hash = hash

        #Image
        self.image_label = QLabel()
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(64, 64))
        layout.addWidget(self.image_label)

        #Center Text
        text_layout = QVBoxLayout()

        #Center Text - Title
        self.title_label = QLabel()
        self.title_label.setFixedWidth(150)
        
        ElideText(self.title_label, title)
        

        #Center Text - Subtitle
        self.subtitle_label = QLabel()
        self.subtitle_label.setFixedWidth(150)

        ElideText(self.subtitle_label, subtitle)
        # subtitle_fm = QFontMetrics(self.subtitle_label.font())
        # subtitle_elided_text = subtitle_fm.elidedText(subtitle, Qt.ElideRight, self.subtitle_label.width())

        # self.subtitle_label.setText(subtitle_elided_text)

        # subtitle_text_width = subtitle_fm.horizontalAdvance(subtitle)
        # subtitle_label_width = self.subtitle_label.width()

        # if subtitle_text_width > subtitle_label_width:
        #     self.subtitle_label.setToolTip(subtitle)
        # else:
        #     self.subtitle_label.setToolTip("")

        #Center Text - Add to Main Widget
        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.subtitle_label)
        layout.addLayout(text_layout)

        #Play Button
        self.play_button = QPushButton("Play")
        self.play_button.setCheckable(True)

            #toggled means it only updates on change, so its not always checking
        self.play_button.toggled.connect(lambda checked, songextension=extension, songtitle=title: self.on_toggle(checked, songextension, songtitle))
        layout.addWidget(self.play_button)

        #Menu
        self.menuButton = QPushButton("⋮")
        self.menu = QMenu(parent=self)
        self.menu.aboutToShow.connect(self.populateMenu)
        self.menu.aboutToHide.connect(self.clearMenu)

        # if dropdown_items:

            

                    # RenameFile(filename, extension, newname)
                    # RefreshFlowLayout(flow_layout, placeholderimage, passingcontroller)
        



        self.menuButton.setMenu(self.menu)
        
        layout.addWidget(self.menuButton)

        layout.addStretch()
    
    def on_toggle(self, checked: bool, songextension:str, songtitle: str):
        MusicDir = "MusicFiles\\" + songtitle + songextension
        if checked:

            self.controller.play(MusicDir, self)
            
            self.play_button.setText("Stop")
            # media = self.vlc_instance.media_new(MusicDir)
            # self.player = self.vlc_instance.media_player_new()
            # self.player.set_media(media)
            # self.player.play()

            # # playMusicFile(songtitle + songextension)

        else:
            self.controller.stop()
            self.play_button.setText("Play")
            # if self.player is not None:
            #     self.player.stop()
            #     self.player = None
            # # stopMusicFile(songtitle + songextension)

    def populateMenu(self):
        self.clearMenu()


        PlaylistData = fetchJson("Playlists")


        for item in self.dropdown_items:

                # action = self.menu.addAction(item)

                if item == 'Add to Playlist':
                    PlaylistsMenu = QMenu(item, parent=self.menu)
                    container = QWidget()
                    ATPlayout = QVBoxLayout(container)

                    for playlists in PlaylistData:
                        TempHboxLayout = QHBoxLayout()
                        PlaylistLabel = QLabel()
                        PlaylistLabel.setFixedWidth(120)
                        ElideText(PlaylistLabel, playlists)
                        TempHboxLayout.addWidget(PlaylistLabel)


                        RemoveButton = QPushButton("Remove")
                        RemoveButton.setFixedWidth(60)
                        RemoveButton.setEnabled(False)
                        if self.hash in PlaylistData[playlists]:
                            RemoveButton.setEnabled(True)
                        RemoveButton.clicked.connect(lambda Checked=False, PlaylistName=playlists, Hash=self.hash, RemoveButton=RemoveButton: RemoveFromPlaylist(PlaylistName, Hash, RemoveButton))

                        AddButton = QPushButton("Add")
                        AddButton.setFixedWidth(40)
                        AddButton.clicked.connect(lambda Checked=False, PlaylistName=playlists, Hash=self.hash, RemoveButton=RemoveButton: AddToPlaylist(PlaylistName, Hash, RemoveButton))
                        TempHboxLayout.addWidget(AddButton)
                        TempHboxLayout.addWidget(RemoveButton)


                        ATPlayout.addLayout(TempHboxLayout)

                    ATPlayout.addStretch(1)
                    scroll = QScrollArea()
                    scroll.setWidgetResizable(True)
                    scroll.setWidget(container)
                    scroll.setFixedSize(255, 400)

                    scroll_action = QWidgetAction(PlaylistsMenu)
                    scroll_action.setDefaultWidget(scroll)
                    PlaylistsMenu.addAction(scroll_action)
                    self.menu.addMenu(PlaylistsMenu)

                if item == 'Add to Queue':
                    AddtoQueueButton = QPushButton(item)
                    AddtoQueueButton.clicked.connect(lambda checked=False, hash=self.hash: AddtoQueueFromLibrary(hash))
                    AddtoQueueAction = QWidgetAction(self.menu)
                    AddtoQueueAction.setDefaultWidget(AddtoQueueButton)
                    self.menu.addAction(AddtoQueueAction)

                if item == "Rename":
                    RenameButton = InputableButton("Rename", RenameFile, [self.title, self.extension, self.flowlayout, self.placeholderimage, self.controller])
                    RenameAction = QWidgetAction(self.menu)
                    RenameAction.setDefaultWidget(RenameButton)
                    self.menu.addAction(RenameAction)


                if item == "Delete":
                    DeleteMenu = QMenu(item, parent=self.menu)
                    Deletebutton = QPushButton("Delete")
                    Deletebutton.clicked.connect(lambda Checked=False, FileName=self.title, FileExtension=self.extension, flow_layout=self.flowlayout, placeholderimage=self.placeholderimage, passingcontroller=self.controller: DeleteFile(FileName, FileExtension, flow_layout, placeholderimage, passingcontroller))
                    DeleteAction = QWidgetAction(DeleteMenu)
                    DeleteAction.setDefaultWidget(Deletebutton)
                    DeleteMenu.addAction(DeleteAction)
                    self.menu.addMenu(DeleteMenu)

    
    def clearMenu(self):
        self.menu.clear()

class MusicQueue(QWidget):

    def __init__(self, QueueActive, QueueLayout, controller):

        self.QueueActive = QueueActive
        self.controller = controller
        self.controller.queueUpdated.connect(self.Refresh)
        self.QueueLayout = QueueLayout
        
        self.container = QVBoxLayout()
        self.QueueLayout.addLayout(self.container)

        self.buildUI()

    def buildUI(self):

        QueueData = fetchJson("Queue")
        MusicTagsData = fetchJson("MusicTags")

        QueueVBox = QVBoxLayout()

        TitleLabel = QLabel("Queue")
        QueueVBox.addWidget(TitleLabel, alignment=Qt.AlignCenter)

        ButtonsVBox = QVBoxLayout()
        
        #Add curently queue item and remove options here
        CurrentQueueItemLayout = QHBoxLayout()
        CurrentQueueItemLayout.addStretch(1)

        if QueueData["CurrentQueueItem"][0] == False and len(QueueData["Queue"]) > 0:

            popItemforQueue()

            #In order to grab the updated QueueData that popItemforQueue() updated
            QueueData = fetchJson("Queue")
            if QueueData["CurrentQueueItem"][0] != False:
                CurrentQueueItem = QLabel(MusicTagsData[QueueData["CurrentQueueItem"][0]]["filepath"])

            

        elif QueueData["CurrentQueueItem"][0] != False:
            CurrentQueueItem = QLabel()
            CurrentQueueItem.setMaximumWidth(500)
            NameOfCurrentQueueItem = MusicTagsData[QueueData["CurrentQueueItem"][0]]["filepath"]
            ElideText(CurrentQueueItem, NameOfCurrentQueueItem)
            # CurrentQueueItem.setText()

        else:
            CurrentQueueItem = QLabel("No Items in Queue")

        CurrentQueueItemLayout.addWidget(CurrentQueueItem)


        #Need Clear Queue Button

        StartButton = QPushButton("Start")
        StartButton.setMaximumWidth(200)
        StartButton.setEnabled(False)
        if QueueData["CurrentQueueItem"][0] != False:
            MusicPath = "MusicFiles\\"
            StartButton.clicked.connect(lambda checked=False: self.SetQueueActive())
            StartButton.clicked.connect(lambda checked=False, filename=(MusicPath + MusicTagsData[QueueData["CurrentQueueItem"][0]]["filepath"]): self.controller.playStartNonLib(filename))
            StartButton.setEnabled(True)
            
        CurrentQueueItemLayout.addWidget(StartButton)

        CurrentQueueItemRemoveButton = QPushButton("X")
        CurrentQueueItemRemoveButton.setMaximumWidth(200)
        CurrentQueueItemRemoveButton.clicked.connect(lambda checked=False: self.SetCurrentQueueItemToNothing())
        CurrentQueueItemRemoveButton.setEnabled(False)
        if QueueData["CurrentQueueItem"][0] != False:
            CurrentQueueItemRemoveButton.setEnabled(True)
        CurrentQueueItemLayout.addWidget(CurrentQueueItemRemoveButton)

        ClearQueueButton = QPushButton("Clear Queue")
        ClearQueueButton.setMaximumWidth(200)
        ClearQueueButton.clicked.connect(lambda checked: ClearQueue())
        ClearQueueButton.clicked.connect(lambda checked: self.Refresh())
        ClearQueueButton.clicked.connect(lambda checked: self.controller.stop())
        ClearQueueButton.setEnabled(False)
        if QueueData["CurrentQueueItem"][0] != False:
            ClearQueueButton.setEnabled(True)
        CurrentQueueItemLayout.addWidget(ClearQueueButton)
        CurrentQueueItemLayout.addStretch(1)

        QueueVBox.addLayout(CurrentQueueItemLayout)
        self.container.addLayout(QueueVBox)

        for items in range(len(QueueData["Queue"])):

            TemporaryHBoxLayout = QHBoxLayout()
            TemporaryHBoxLayout.addStretch(1)

            OrderNumber = QLabel()
            OrderNumber.setFixedWidth(100)
            ElideText(OrderNumber, str(items + 1))
            TemporaryHBoxLayout.addWidget(OrderNumber)

            if QueueData["Queue"][items] in MusicTagsData:

                songname = QLabel()
                songname.setFixedWidth(300)

                ElideText(songname, MusicTagsData[QueueData["Queue"][items]]["filepath"])

            else:
                songname = QLabel()
                songname.setText("Unknown Song")

            TemporaryHBoxLayout.addWidget(songname)

            RemoveSongButton = QPushButton("X")
            RemoveSongButton.setMaximumWidth(200)
            RemoveSongButton.clicked.connect(lambda checked=False, Index=items:RemovefromQueue(Index))
            RemoveSongButton.clicked.connect(lambda checked=False: self.Refresh())
            TemporaryHBoxLayout.addWidget(RemoveSongButton)

            ReOrderButton = InputableButton("Change Order", ChangeQueueOrder, [items, self])
            ReOrderButton.setMaximumWidth(200)
            TemporaryHBoxLayout.addWidget(ReOrderButton)
            TemporaryHBoxLayout.addStretch(1)

            ButtonsVBox.addLayout(TemporaryHBoxLayout)

        ButtonsVBox.addStretch(1)
        QueueWidget = QWidget()
        QueueWidget.setLayout(ButtonsVBox)
        # IPVWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        QueueScroll = QScrollArea()
        QueueScroll.setWidgetResizable(True)
        QueueScroll.setMinimumWidth(QueueWidget.width())
        print()
        print("IPV Widget width")
        print(QueueWidget.width())
        print()
        QueueScroll.setWidget(QueueWidget)

        self.container.addWidget(QueueScroll)

    def Refresh(self):

        ClearLayout(self.container)
        self.buildUI()

    def SetQueueActive(self):

        self.QueueActive[0] = True
        self.controller.lastMediaChange[0] = 'Queue'
        self.controller.CurrentPlaylist[0] = None
        print()
        print("QueueActive")
        print(self.QueueActive)
        print()
    
    def SetCurrentQueueItemToNothing(self):

        QueueData = fetchJson("Queue")
        QueueData["CurrentQueueItem"] = [False]

        writeJson("Queue", QueueData)
        QueueData = fetchJson("Queue")

        if len(QueueData["Queue"]) == 0:
            self.controller.stop()

        elif len(QueueData["Queue"]) > 0:
            self.controller.QueueChangeHandler()

        # writeJson("Queue", QueueData)
        self.Refresh()

class PlayerController(QObject):

    #This is to play it in the main thread
    playRequestedQueue = Signal(str)

    #This is to stagger the refresh, so that QueueChangeHandler doesn't delete every gui queue item
    queueUpdated = Signal()

    def __init__(self, CurrentPlaylist, lastMediaChange, PlaylistObjectsList, QueueActive):

        super().__init__()
        self.playRequestedQueue.connect(self.playStartNonLib)

        self.Playlistsdata = fetchJson("Playlists")

        self.vlc_instance = vlc.Instance("--no-xlib --no-video")
        self.player = self.vlc_instance.media_player_new()

        #Probably not needed, remove later
        self.current_file = None

        #Speaks for themselves
        self.CurrentPlaylist = CurrentPlaylist
        self.lastMediaChange = lastMediaChange
        self.PlaylistObjectsList = PlaylistObjectsList
        self.QueueActive = QueueActive

        #Linked to the Playback Bar
        self.bar = None    

        #Linked to the Queue
        self.Queue = None   

        #The Active Tile
        self.active_tile = None


    #May need to add another play function for playlists
    def play(self, filepath, tile):

        #Fixes a bug in which start a playlist and leaving the index on 0, then plaing a library song,
        #and then going back to that playlist wouldn't let you start (because startbutton places you on index0,
        #but index0 is still the current index)

        if self.CurrentPlaylist[0] != None:
            self.PlaylistObjectsList[self.CurrentPlaylist[0]].value = None
        
        self.CurrentPlaylist[0] = None
        self.QueueActive[0] = False

        if self.active_tile and self.active_tile != tile:
            self.active_tile.play_button.setChecked(False)
            self.active_tile.play_button.setText("Play")

        if self.player.is_playing():
            self.player.stop()

        
        media = self.vlc_instance.media_new(filepath)
        self.player.set_media(media)
        self.player.play()
        self.current_file = filepath
        self.active_tile = tile

        if self.bar:
            self.bar.PauseButton.setChecked(False)
            self.bar.PauseButton.setText("Pause")

        if self.CurrentPlaylist[0] == None and self.QueueActive[0] == False and self.lastMediaChange[0] != "Library":
            self.lastMediaChange[0] = "Library"

        print()
        print(self.CurrentPlaylist)
        print(self.lastMediaChange)
        print()

        # if self.bar:
        #     self.bar.set_file(filepath)

    def playStartNonLib(self, filename):
        
        print()
        print("playStartNonLib")
        print(filename)
        print("playStartNonLib called from thread:", QThread.currentThread())
        print()

        media = self.vlc_instance.media_new(filename)

        print(media)

        # self.player.set_media(media)
        # result = self.player.play()

        # print()
        # print("VLC play() result:", result)
        # print()

        try:
            self.player.set_media(media)
            result = self.player.play()
            print("VLC play() result:", result)
        except Exception as e:
            import traceback
            print("Error while starting playback:", e)
            traceback.print_exc()


        self.current_file = filename


        if self.bar:
            self.bar.PauseButton.setChecked(False)
            self.bar.PauseButton.setText("Pause")

    def SafeplayStartNonLib(self, filename):

        self.playRequestedQueue.emit(filename)

    def playNonLib(self):

        self.player.play()

        if self.bar:
            self.bar.PauseButton.setChecked(False)
            self.bar.PauseButton.setText("Pause")


    def pause(self):
        self.player.pause()

        if self.bar:
            self.bar.PauseButton.setChecked(True)
            self.bar.PauseButton.setText("Resume")
    
    def stop(self):
        
        #Prevents crashes if the program tries to get the player to stop if it is already stopped
        if self.player.get_state() != vlc.State.Stopped:
            self.player.stop()
            self.current_file = None


        # if self.active_tile:
        #     self.active_tile.play_button.setChecked(False)
        #     self.active_tile.play_button.setText("Play")
        #     self.active_tile = None

        # if self.bar:
        #     self.bar.clear()

    def on_playing(self, event):
        print("playing")

        if self.bar:
            self.bar.show()

        # pass

    def on_paused(self, event):
        print("paused")

        if self.bar:
            self.bar.show()
        # pass

    def on_stopped(self, event):
        print("stopped")
        if self.bar:
            self.bar.hide()

    def on_end(self, event):
        
        print()
        print("ended")
        print(self.CurrentPlaylist)
        
        if self.active_tile != None:
            self.active_tile.play_button.setChecked(False)
            self.active_tile.play_button.setText("Play")
            self.active_tile = None

        if self.CurrentPlaylist[0] != None:

            #This is required in order for self.Playlistsdata to update if new playlist items are added
            self.Playlistsdata = fetchJson("Playlists")

            print("Playlist isn't none")

            PlaylistObject = self.PlaylistObjectsList[self.CurrentPlaylist[0]]
            
            currentPlaylistLenght = len(self.Playlistsdata[self.CurrentPlaylist[0]])

            #If the next playlistItem Exists, go to it
            print()
            print("currentPlaylistLength")
            print(currentPlaylistLenght)
            print(PlaylistObject.value)
            print()

            if currentPlaylistLenght > PlaylistObject.value:

                print("Playlist isn't at the end")



                PlaylistObject.value += 1

        print()
        print("On_end QueueActive")
        print(self.QueueActive)
        print()

        if self.QueueActive[0] != False:

            print()
            print("On_end QueueChangeHandler")
            print(self.QueueActive[0])
            print()


            self.QueueChangeHandler()


    def on_media_changed(self, event):

        print(self.CurrentPlaylist)
        print(self.lastMediaChange)

        # if self.bar:
        #     song = self.player.get_media()

        #     if song:
        #         mrl = song.get_mrl()

        #         print()
        #         print('mrl')
        #         print(mrl)
        #         print()

        #         self.bar.musicName.setText(mrl)
        
        if self.CurrentPlaylist[0] != None or self.QueueActive[0] != False:

            if self.lastMediaChange[0] == "PlaylistChangeHandler":

                self.QueueActive[0] = False

            elif self.lastMediaChange[0] == "Library":

                self.CurrentPlaylist[0] = None
                self.QueueActive[0] = False
            
            elif self.lastMediaChange[0] == 'Queue':

                self.CurrentPlaylist[0] = None

            else:

                pass

    

    def PlaylistChangeHandler(self, newPlaylistObject):

        MusicDir = "MusicFiles\\"

        playlistsData = fetchJson("Playlists")
        musicTagsData = fetchJson("MusicTags")

        if newPlaylistObject.name != self.CurrentPlaylist[0]:
            
            #Fixes a bug in which start a playlist and leaving the index on 0, then starting another playlist,
            #and then going back to that playlist wouldn't let you start (because startbutton places you on index0,
            #but index0 is still the current index)
            if self.CurrentPlaylist[0] != None:
                self.PlaylistObjectsList[self.CurrentPlaylist[0]].value = None

            self.CurrentPlaylist[0] = newPlaylistObject.name
        
        #Grabs the hash associated with the index of the playlist (specified by name)
        #Not ._value, so that the emitter works properly
        print()
        print("PlaylistChangeHandler log")
        print(self.CurrentPlaylist)
        print(playlistsData[newPlaylistObject.name])
        print(newPlaylistObject.value)
        hash = playlistsData[newPlaylistObject.name][newPlaylistObject.value]
        print()

        if hash in musicTagsData:
            filetoplay = musicTagsData[hash]["filepath"]

            self.playStartNonLib(MusicDir + filetoplay)

        #If the hash is unknown, skip it by incrementing the value, calling PlaylistChangeHandler again
        else:
            newPlaylistObject.value += 1

        self.lastMediaChange[0] = "PlaylistChangeHandler"
        
    
        print("Playlist Index Changed")

    def QueueChangeHandler(self):

        MusicDir = "MusicFiles\\"

        QueueData = fetchJson("Queue")
        musicTagsData = fetchJson("MusicTags")

        
        if len(QueueData["Queue"]) > 0:
            NewCurrentQueue = QueueData["Queue"].pop(0)
            QueueData["CurrentQueueItem"][0] = NewCurrentQueue

            writeJson("Queue", QueueData)

            self.QueueActive[0] = True
            self.lastMediaChange[0] = 'Queue'

            hash = QueueData["CurrentQueueItem"][0]

            print()
            print("QueueChangeHandler")
            print(hash)
            print()

            if hash in musicTagsData:

                print()
                print("Hash in musicTagsData")
                print(musicTagsData[hash]["filepath"])
                print()

                fileToPlay = musicTagsData[hash]["filepath"]
                print(MusicDir + fileToPlay)
                self.SafeplayStartNonLib(MusicDir + fileToPlay)

            

        else:
            print()
            print("QueueChangeHandler - Else Triggered")

            QueueData["CurrentQueueItem"] = [False]
            writeJson("Queue", QueueData)

        #For good measure
        # writeJson("Queue", QueueData)

        if not self.Queue:
            print()
            print("self.Queue Doesn't exist")
            print()


        if self.Queue:
            print()
            print("QueueChangeHandler - self.Queue = True")
            print()
            self.queueUpdated.emit()

class ProgressBar(QWidget):

    #What might be needed: 
    def __init__(self, controller):
        super().__init__()

        superlayout = QVBoxLayout()

        self.controller = controller

        

        self.musicName = QLabel()
        self.musicName.setMinimumWidth(300)
        self.musicName.setMaximumWidth(1000)
        superlayout.addWidget(self.musicName, alignment=Qt.AlignCenter)


        self.PauseButton = QPushButton("Pause")
        self.PauseButton.setCheckable(True)

        self.PauseButton.toggled.connect(lambda checked, : self.PauseButtonToggle(checked))
        superlayout.addWidget(self.PauseButton)

        self.controller = controller

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(1000)

        self.elapsed_label = QLabel("0:00")
        self.total_label = QLabel("0:00")

        layout = QHBoxLayout()
        layout.addWidget(self.elapsed_label)
        layout.addWidget(self.slider)
        layout.addWidget(self.total_label)
        superlayout.addLayout(layout)

        self.setLayout(superlayout)

        self.slider.sliderPressed.connect(self.on_slider_pressed)
        self.slider.sliderReleased.connect(self.on_slider_released)
        self.slider.sliderMoved.connect(self.on_slider_moved)


        self.timer = QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start()

    def PauseButtonToggle(self, checked):

        if checked:

            self.controller.pause()
            self.PauseButton.setText("Resume")

        else:

            #Directly plays, instead of engaging the play function in playercontroller
            self.controller.player.play()
            self.PauseButton.setText("Pause")
            
            

    
    def update_progress(self):
        player = self.controller.player

        if player is not None and player.is_playing():
            length = player.get_length()
            position = player.get_time()
            if length > 0:
                self.slider.setValue(int(position / length * 1000))
                self.elapsed_label.setText(self.ms_to_time(position))
                self.total_label.setText(self.ms_to_time(length))

    def on_slider_pressed(self):

        self.timer.stop()
        # self.controller.pause()

        #Pauses the player directly, instead of engaging with the pause function in playercontroller, making
        #sure that PauseButton displays the correct text (as the pause function resets the Pausebutton, in anticipation
        #of multiple pause buttons)

        if self.controller.player.get_state() != vlc.State.Paused:
            self.controller.player.pause()

    def on_slider_released(self):

        new_slider_position = self.slider.value()
        player = self.controller.player
        length = player.get_length()
        new_time_position = int((new_slider_position / 1000) * length)

        player.set_time(new_time_position)

        player.play()

        #We can do this here because the other pause buttons (if there are more) will only be click style buttons, instead of
        #toggling buttons
        if self.PauseButton.isChecked:
            self.PauseButton.setChecked(False)
            self.PauseButton.setText("Pause")

        self.timer.start()

    def on_slider_moved(self, value):

        player = self.controller.player
        length = player.get_length()
        new_time_position = int((value / 1000) * length)
        self.elapsed_label.setText(self.ms_to_time(new_time_position))

    def ProgressBarMediaChange(self, event):
        
        song = self.controller.player.get_media()

        if song:
            mrl = song.get_mrl()

            path = urllib.parse.unquote(mrl[7:])

            basepath = os.path.splitext(os.path.basename(path))[0]

            #Really should make a function for this shit
            ElideText(self.musicName, basepath)

            #Keeps it center aligned even with a minimum width
            self.musicName.setAlignment(Qt.AlignCenter)


            # self.musicName.setText(os.path.splitext(os.path.basename(path))[0])

    


    @staticmethod
    def ms_to_time(ms):
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02}"

class InputableButton(QWidget):

    def __init__(self, ButtonText, functionToDo, additionalarguemments: list):
        super().__init__()

        layout = QVBoxLayout()

        self.functionToDo = functionToDo
        self.arguemments = additionalarguemments

        self.button = QPushButton(ButtonText)
        self.button.clicked.connect(self.show_input)
        layout.addWidget(self.button)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Hit Enter once done typing")
        self.input.returnPressed.connect(self.on_enter_pressed)
        self.input.hide()
        layout.addWidget(self.input)

        self.setLayout(layout)

    def show_input(self):
        self.input.show()
        self.input.setFocus()

    def on_enter_pressed(self):
        text = self.input.text()
        self.functionToDo(self.arguemments, text)
        self.input.clear()
        self.input.hide()


def CreatePlaylist(AddtionalArguements, playlistName):

    playlistData = fetchJson("Playlists")

    if playlistName not in playlistData:
        playlistData[playlistName] = []
        print("Created Playlist Successfully!")

    writeJson("Playlists", playlistData)

def AddToPlaylist(PlaylistName, Hash, RemoveButton):
    PlaylistData = fetchJson("Playlists")

    PlaylistData[PlaylistName].append(Hash)

    if not RemoveButton.isEnabled():
        RemoveButton.setEnabled(True)

    writeJson("Playlists", PlaylistData)

def RemoveFromPlaylist(PlaylistName, Hash, RemoveButton):
    PlaylistData = fetchJson("Playlists")

    playlistWithHashRemoved = []
    for hashs in PlaylistData[PlaylistName]:
        if hashs != Hash:
            playlistWithHashRemoved.append(hashs)
    
    if RemoveButton.isEnabled():
        RemoveButton.setEnabled(False)

    PlaylistData[PlaylistName] = playlistWithHashRemoved

    writeJson("Playlists", PlaylistData)
        
def RenameFile(Arguements, text):

    filename = Arguements[0]
    extension = Arguements[1]
    newname = text

    MusicPath = "MusicFiles\\"

    Filepath = MusicPath + filename + extension
    Newpath = MusicPath + newname + extension

    print()
    print(os.listdir(MusicPath))
    print()
    print(Newpath + extension)
    print()

    #Protects against duplicate names
    if newname + extension not in os.listdir(MusicPath):
        os.rename(Filepath, Newpath)

        RefreshFlowLayout(Arguements[2], Arguements[3], Arguements[4])
        #RefreshFlowLayout(flow_layout, placeholderimage, passingcontroller)

def DeleteFile(FileName, FileExtension, flow_layout, placeholderimage, passingcontroller):

    MusicPath = "MusicFiles\\"

    FilePath = MusicPath + FileName + FileExtension

    os.remove(FilePath)

    RefreshFlowLayout(flow_layout, placeholderimage, passingcontroller)

def DeletePlaylist(PlaylistName, playlist_layout, placeholderimage, individualPlaylistViewerLayout, controller, CurrentPlaylist, PlaylistObjectsList, CurrentIPV):

    PlaylistsData = fetchJson("Playlists")

    if PlaylistName in PlaylistsData:
        del PlaylistsData[PlaylistName]

    writeJson("Playlists", PlaylistsData)
    RefreshPlaylistsLayout(playlist_layout, placeholderimage, individualPlaylistViewerLayout, controller, CurrentPlaylist, PlaylistObjectsList, CurrentIPV)

def RenamePlaylist(Arguements, text):
    
    PlaylistsData = fetchJson("Playlists")

    PlaylistName=Arguements[0]

    playlist_layout=Arguements[1]
    placeholderimage=Arguements[2]
    individualPlaylistViewerLayout=Arguements[3]
    controller=Arguements[4]
    CurrentPlaylist=Arguements[5]
    PlaylistObjectsList=Arguements[6]
    CurrentIPV=Arguements[7]

    if PlaylistName in PlaylistsData:
        CopiedPlaylist = list(PlaylistsData[PlaylistName])

        del PlaylistsData[PlaylistName]

        PlaylistsData[text] = CopiedPlaylist

    writeJson("Playlists", PlaylistsData)

    RefreshPlaylistsLayout(playlist_layout, placeholderimage, individualPlaylistViewerLayout, controller, CurrentPlaylist, PlaylistObjectsList, CurrentIPV)
    
def RemoveFromPlaylistIPV(PlaylistName, Index):
    playlistJsondata = fetchJson("Playlists")

    del playlistJsondata[PlaylistName][Index]

    writeJson("Playlists", playlistJsondata)

def ChangePlaylistOrder(Arguements, text):

    playlistJsondata = fetchJson("Playlists")

    PlaylistName = Arguements[0]
    CurrentIndex = Arguements[1]
    PlaylistTileInstance = Arguements[2]
    NewIndex = int(text)


    element = playlistJsondata[PlaylistName].pop(CurrentIndex)

    if CurrentIndex > NewIndex:

        playlistJsondata[PlaylistName].insert(NewIndex - 1, element)
        print()
        print("NewIndex - CurrentIndex > NewIndex")
        print(NewIndex)
        print()
    
    elif CurrentIndex < NewIndex:

        playlistJsondata[PlaylistName].insert(NewIndex - 1, element)
        print()
        print("NewIndex - CurrentIndex < NewIndex")
        print(NewIndex)
        print()


    else:
        playlistJsondata[PlaylistName].insert(CurrentIndex - 1, element)
        print()
        print("NewIndex - CurrentIndex = NewIndex")
        print(NewIndex)
        print()

    writeJson("Playlists", playlistJsondata)
    PlaylistTileInstance.Refresh()

def RemovefromQueue(Index):
    QueueData = fetchJson("Queue")

    del QueueData["Queue"][Index]

    writeJson("Queue", QueueData)

def ChangeQueueOrder(Arguements, text):

    QueueData = fetchJson("Queue")

    CurrentIndex = Arguements[0]
    QueueInstance = Arguements[1]
    NewIndex = int(text)


    element = QueueData["Queue"].pop(CurrentIndex)

    if CurrentIndex > NewIndex:

        QueueData["Queue"].insert(NewIndex - 1, element)
        print()
        print("NewIndex - CurrentIndex > NewIndex")
        print(NewIndex)
        print()
    
    elif CurrentIndex < NewIndex:

        QueueData["Queue"].insert(NewIndex - 1, element)
        print()
        print("NewIndex - CurrentIndex < NewIndex")
        print(NewIndex)
        print()


    else:
        QueueData["Queue"].insert(CurrentIndex - 1, element)
        print()
        print("NewIndex - CurrentIndex = NewIndex")
        print(NewIndex)
        print()

    writeJson("Queue", QueueData)
    QueueInstance.Refresh()

def ClearQueue():

    QueueData = fetchJson("Queue")

    QueueData["Queue"] = []
    QueueData["CurrentQueueItem"] = [False]
    writeJson("Queue", QueueData)

def AddtoQueueFromLibrary(hash):

    QueueData = fetchJson("Queue")
    QueueData["Queue"].append(hash)
    writeJson("Queue", QueueData)

def AddtoQueueFromPlaylist(PlaylistName):

    QueueData = fetchJson("Queue")
    PlaylistsData = fetchJson("Playlists")

    if PlaylistName in PlaylistsData:

        for items in PlaylistsData[PlaylistName]:
            QueueData["Queue"].append(items)

    writeJson("Queue", QueueData)
    
def popItemforQueue():
    QueueData = fetchJson("Queue")

    if len(QueueData["Queue"]) > 0:
        NewCurrentQueue = QueueData["Queue"].pop(0)
        QueueData["CurrentQueueItem"][0] = NewCurrentQueue

        writeJson("Queue", QueueData)

def OrganizeMusicTagsAlphabetically():
    MusicTagsData = fetchJson("MusicTags")
    NewJson = {}

    DictOfFilePathsAndHashs = {}
    ListOfFilePaths = []
    for items in MusicTagsData:
        print(MusicTagsData[items]["filepath"])
        DictOfFilePathsAndHashs[MusicTagsData[items]["filepath"]] = items
        ListOfFilePaths.append(MusicTagsData[items]["filepath"])

    print()

    ListOfFilePaths.sort()
    for filepaths in ListOfFilePaths:
        NewJson[DictOfFilePathsAndHashs[filepaths]] = MusicTagsData[DictOfFilePathsAndHashs[filepaths]]

    writeJson("MusicTags", NewJson)
    onStartHashCheck()

def ElideText(Label, text):
    Label_fm = QFontMetrics(Label.font())


    Label_elided_text = Label_fm.elidedText(text, Qt.ElideRight, Label.width())

    Label.setText(Label_elided_text)

    Label_text_width = Label_fm.horizontalAdvance(text)
    Label_label_width = Label.width()

    if Label_text_width > Label_label_width:
        Label.setToolTip(text)
    else:
        Label.setToolTip("")

class FlowLayout(QLayout):
    def __init__(self, parent=None):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(QMargins(0, 0, 0, 0))

        self._item_list = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self._item_list.append(item)

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list[index]

        return None

    def takeAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self._do_layout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())

        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def _do_layout(self, rect, test_only):
        x = rect.x()
        y = rect.y()
        line_height = 0
        spacing = self.spacing()

        for item in self._item_list:
            style = item.widget().style()
            layout_spacing_x = style.layoutSpacing(
                QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton,
                Qt.Orientation.Horizontal
            )
            layout_spacing_y = style.layoutSpacing(
                QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton,
                Qt.Orientation.Vertical
            )
            space_x = spacing + layout_spacing_x
            space_y = spacing + layout_spacing_y
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y()

def dump_widget_stats(tag=""):
    total = len(QApplication.instance().allWidgets())
    tops = len(QApplication.instance().topLevelWidgets())
    print()
    print(f"[{tag}] widgets={total}, topLevel={tops}")
    print()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

