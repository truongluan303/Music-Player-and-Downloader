# Music-Player-and-Downloader

This python program is a music player that allows the users to download a song from youtube and then play all the songs that have been downloaded.
The user can choose a playlist to download songs to. To download a song, the user only needs to enter the song's name and the artist's name, and then
hit download. After downloading all the songs that they want, the user can then choose a playlist to start playing music.

The music player is implemented using a circular doubly linked list to easily move from one song to another in both forward and backward direction.

The two main libraries that this program use are youtube-dl (to download song from youtube), and pyglet (to play sound). These libraries will automatically
be installed at the very first time the program is run so the user does not need to install anything. 

## Demo Run:

* turn the sound on to hear the song in the demo run *

https://user-images.githubusercontent.com/83048295/130008623-724463a6-57b2-409a-919c-6ef4463ae9f1.mp4


## Screen Shots:

![Music Player 8_18_2021 9_39_42 PM](https://user-images.githubusercontent.com/83048295/130008738-74829540-7792-4f89-baf0-b407d35894ef.png)
![Music Player 8_18_2021 9_39_20 PM](https://user-images.githubusercontent.com/83048295/130008743-2bcb0829-09ff-4b51-8bdf-a9e1509d51ed.png)


## How did I implement this program?

This program can be seperated into two main parts, the song downloader and the song player.

For the song downloader, the program simply use the user's input of the song's name and artist as the search query for youtube searching. Then the program will download the very first result found since it will most likely be the best match for the song that the user wants to download.

For the music player, as mentioned above, it is implemented using a circular doubly linked list. This data structure will allow us to move in both forward and backward directions. And when we encounter the end of the songs list, it will continue at the beginning of the song list. The music player is a class inherited from the circular doubly lined list class and will have all basic features of a music player such as play/pause, to next song, to previous song, delete a song from playlist, etc. 


