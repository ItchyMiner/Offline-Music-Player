Hi! This is my first ever Pyside6 program. It is a Local Music Player. Hope you like it!

Features:
A library page for all of your Music
Automatic duplicate detection
Playlists (you can add multiple of the same song if you want)
A Queue

All of the features present inside work (to the extent of my testing). However there is some extra/unused
code for features not yet implemented (I haven't gotten around to doing so, and I want to ship a mvp). More features
are planned!

How to use:
(If not using the exe version) Create a Folder called MusicFiles in the folder with the rest of the files. Drag all of your music files into the MusicFiles folder. Then start the program. 
Depending on how many files you have, the first startup might take a bit (~10-20 seconds per 7.5 gigabytes of music), 
as the program is hashing all the files (if it doesn't work the first time, try it again, it should work then).
On future startups, it will be much faster (~2 seconds). Once it is done hashing, the program will start.

In the program, there are buttons for the library, playlists, and the queue. You can add music to playlists or the queue from the library. 
You can also add entire playlists to the queue (from the playlists page), if you want.

You can create playlists by using the Create Playlist button in the playlists page. You have to click the Refresh Playlists button for them to show up.

It is possible to rename or delete music in the library from inside the program, however this can be somewhat laggy, so I suggest deleting them in your file manager.

When changing the position of music in Playlists or in the Queue, click on the change order button, and input the position (the number) you want it to move to

The the rest of the program should be mostly self-explanatory, so have fun!


Extra Information:
DO NOT rename the MusicTags folder, it will break everything
DO NOT Rename any of the Json files either for the same reason

If you want a new placeholder image, just replace the one in the folder with another placeholder.jpg (it has to be a jpg)

Don't spam the refresh library button, it will make things lag for a bit (once is fine)

The performance is decent, but it isn't great for renaming/deleting files from the library (it may take a few seconds), due to
some architectural problems
