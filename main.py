import os
from tkinter import *
from tkinter.font import Font, BOLD
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
from threading import Timer
from install_lib.install_lib import install_required_libraries 
from music_player import MusicPlayer
from youtube_download import download_song


HIDDEN_DIR = '.playlists'   # the hidden folder where the playlists are stored
WIDTH = 700                 # the GUI height
HEIGHT = 400                # the GUI width
PLAY_OPTION = 1             # the indentifying code when user chooses to play song
DOWNLOAD_OPTION = 2         # the identifying code when user chooses to download song
playlist = ''               # the playlist that the user chooses
timer = None                # the timer to keep track of a song's duration



def create_mainscreen(root: Tk) -> None:
    '''
    create the main screen where the user chooses what to do.
    There will be 3 options: to start playing music from a playlist,
    to download music to a playlist, or to exit. If the user chooses
    any of the first 2 options, they will be taken to a screen where
    they must choose a playlist to take action on.
    '''
    clear_screen(root)
    canvas = Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    make_button(canvas, 'PLAY MUSIC', lambda: choose_playlist(root, PLAY_OPTION))
    add_space(canvas)
    make_button(canvas, 'ADD SONG', lambda: choose_playlist(root, DOWNLOAD_OPTION))
    add_space(canvas)
    make_button(canvas, 'EXIT', lambda: quit())



def choose_playlist(root, option: int) -> None:
    '''
    create a screen to let the user choose a playlist that they
    want to take action on. If the player is about to download music,
    there will be an extra option for them to create a new playlist.
    '''
    clear_screen(root)
    # create a canvas where inner components are centered
    canvas = Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    # display the correct message depends on the option chosen by the user
    if option == DOWNLOAD_OPTION:
        message = 'Please choose the playlist to download the song to'
    elif option == PLAY_OPTION:
        message = 'Please choose the playlist to play'
    make_label(canvas, message)
    add_space(canvas, 3)

    # show all the available playlists for the user to choose from
    for playlist in os.listdir(HIDDEN_DIR):
        name = os.path.basename(playlist)
        make_button(canvas, name.replace('-', ' '),
            lambda playlist=name: go_to_option(option, playlist))
    # if the user is about to download a song, then also add
    #   an option that allows them to create a new playlist
    if option == DOWNLOAD_OPTION:
        add_space(canvas)
        make_button(canvas, 'Create New Playlist', 
            lambda: create_playlist(option))
    add_space(canvas)
    # a button to go back to the main screen
    make_button(canvas, 'Go Back', lambda: create_mainscreen(root), 10)


    def create_playlist(option: int) -> None:
        '''
        create a new playlist (folder) in the hidden folder, and then
        choose that playlist
        '''
        new_playlist = simpledialog.askstring(
            title='Enter Playlist Name', 
            prompt='Please name your new playlist:'
        )
        # show error if the user did not enter a name for the new playlist
        if new_playlist is None or new_playlist == '':
            messagebox.showerror(title='Error', 
                message='Playlist name cannot be empty!')
            return
        # else, create the new playlist and go there
        new_playlist = new_playlist.replace(' ', '-')
        os.makedirs(HIDDEN_DIR + '/' + new_playlist)
        go_to_option(option, new_playlist)


    def go_to_option(option: int, playlist: str) -> None:
        '''
        take the user to the option that they chose
        '''
        if option == DOWNLOAD_OPTION:
            create_download_screen(root, playlist)
        elif option == PLAY_OPTION:
            create_play_screen(root, playlist)



def create_download_screen(root: Tk, playlist: str):
    '''
    create the screen where user downloads songs. The user must enter
    the name of the song they want to download and also the name of the 
    artist.
    '''
    path = HIDDEN_DIR + '/' + playlist
    clear_screen(root)
    add_space(root, 4)
    canvas = Canvas(root, width=WIDTH, height=HEIGHT)
    make_label(canvas, 'Enter the song and artist', False).grid(row=1, columnspan=2)
    make_label(canvas, 'Song Name: ', False).grid(row=2, column=0)
    song = make_entry(canvas, pack=False)
    song.grid(row=2, column=1)
    make_label(canvas, 'Artist Name: ', False).grid(row=3, column=0)
    artist = make_entry(canvas, pack=False)
    artist.grid(row=3, column=1)
    canvas.pack()
    add_space(root, 2)
    make_button(root, 'DOWNLOAD SONG', 
        lambda: download_song(song.get(), artist.get(), path))
    add_space(root)
    # a button to go back to the choose playlist screen
    make_button(root, 'Go Back', lambda: choose_playlist(root, DOWNLOAD_OPTION), 15)

    def start_downloading():
        if download_song(song.get(), artist.get(), path):
            messagebox.showinfo(title='Done', message='The song is successfully added!')
        else:
            messagebox.showerror(title='Error', message='Invalid Input!')
        song.delete(0, 'end')
        artist.delete(0, 'end')



def create_play_screen(root: Tk, playlist: str) -> None:
    '''
    create the screen where user plays music. This is the most important
    GUI in the application where the songs are played and the information
    about the songs is displayed
    '''

    def start_timing():
        '''
        start counting down the song duration to know when the song
        is finished. When it is, go to the next song in the list
        '''
        global timer
        timer = Timer(player.get_song_duration(), lambda: end_of_song())
        timer.start()

    def close_window():
        '''
        When the user closes the window, if timer is still counting, 
        it won't response. So, we need to cancel the timer for the 
        window to close
        '''
        timer.cancel()
        quit()
 
    root.protocol("WM_DELETE_WINDOW", close_window)
    clear_screen(root)
    repeat = False
    # create the music player and start timing since a song will be played right away
    player = MusicPlayer(HIDDEN_DIR + '/' + playlist)
    start_timing()

    # make the GUI
    add_space(root, 1)
    make_label(root, 'Now Playing:')
    add_space(root, 2)
    song_label = make_label(root, player.get_song_name())
    artist_label = make_label(root, player.get_artist_name())
    add_space(root)

    buttons = Canvas(root)
    repeat_button = Button(buttons, text='🔁', font=('Arial', 30), bd=0,
        command=lambda: repeat_song())
    repeat_button.grid(row=0, column=0)
    Button(buttons, text='⏮', font=('Arial', 30), bd=0,
        command=lambda: previous_song()).grid(row=0, column=1)
    play_pause_button = Button(buttons, text='⏸', font=('Arial', 30), bd=0,
        command=lambda: play_pause())
    play_pause_button.grid(row=0, column=2)
    Button(buttons, text='⏭', font=('Arial', 30), bd= 0,
        command=lambda: next_song()).grid(row=0, column=3)
    Button(buttons, text='🗑', font=('Arial', 30), bd= 0,
        command=lambda: delete_song()).grid(row=0, column=4)
    buttons.pack()

    add_space(root, 2)
    make_button(root, 'Go Back', lambda: go_back(), 15)

    def play_pause():
        '''
        play or pause the song
        '''
        if player.is_playing():
            play_pause_button.config(text='▶')
        else:
            play_pause_button.config(text='⏸')
        player.play_pause()

    def next_song():
        '''
        go to the next song in the list
        '''
        player.to_next_song()
        change_song()

    def previous_song():
        '''
        go to the previous song in the list
        '''
        player.to_previous_song()
        change_song()

    def change_song():
        '''
        change the song and update the GUI
        '''
        global timer  
        # reset the timer
        timer.cancel()
        # update the GUI
        song_label.config(text=player.get_song_name())
        artist_label.config(text=player.get_artist_name())
        start_timing()

    def end_of_song():
        '''
        move on to the next song when a song ends. If repeat is
        on, then keep replaying the song
        '''
        if not repeat:
            next_song()
        else:
            player.replay()
            change_song()

    def delete_song():
        '''
        permanently delete the song from the playlist
        '''
        if messagebox.askokcancel('Please confirm', 
            'You are about to permanently delete this song!'):
            if not player.delete_song():
                messagebox.showerror(title='Error',
                    message='An Error occurred while deleting the song ' + 
                    player.get_song_name() + player.get_artist_name())
            next_song()

    def repeat_song():
        '''
        repeat the song until the user change song
        '''
        nonlocal repeat
        if not repeat:
            repeat = True
            repeat_button.config(fg='blue')
        else:
            repeat = False
            repeat_button.config(fg='black')


    def go_back():
        '''
        cancel the timer, destroy the music player,
        and go back to choose playlist screen
        '''
        timer.cancel()
        player.destroy()
        choose_playlist(root, PLAY_OPTION)



def make_button(master, text: str, command, width:int=25, 
                pack:bool=True) -> Button:
    '''
    create a button
    @return: the button created
    '''
    button = Button(master, width=width, height=1, command=command)
    button.config(fg='white', bg='brown', padx=5, text=text, 
        font=Font(family='Helvetica', weight=BOLD))
    if pack:
        button.pack()
    return button



def make_label(master, text: str, pack:bool=True) -> Label:
    '''
    create a text label
    @return: the label created
    '''
    label = Label(master, text=text)
    label.config(fg='brown', font=Font(family='Helvetica', weight=BOLD))
    if pack:
        label.pack()
    return label



def make_entry(master, placeholder:str='', pack:bool=True) -> Entry:
    '''
    create an entry portion
    @return: the entry created
    '''
    entry = Entry(master)
    entry.config(width=30, font=Font(family='Helvetica'), fg='brown')
    entry.insert(0, placeholder)
    if pack:
        entry.pack()
    return entry



def add_space(canvas: Canvas, height:int=1) -> None:
    '''
    add a gap between components using an empty label
    '''
    Label(canvas, height=height).pack()



def clear_screen(root: Tk) -> None:
    '''
    clear all the components in the master component
    '''
    for component in root.winfo_children():
        component.destroy()



def init_playlists() -> None:
    '''
    create the hidden playlist folder if it does not already exist.
    And also install the required libraries since the if the hidden 
    folder does not exist then it means program was never run before.
    '''
    if not os.path.exists(HIDDEN_DIR) or not os.path.isdir(HIDDEN_DIR):
        # create the hidden folder '.playlists'
        os.makedirs(HIDDEN_DIR)
        if os.name == 'nt':
            os.system('attrib +h ' + HIDDEN_DIR)
        # install required libraries
        install_required_libraries()
        


###################################################
###################### M A I N ####################
def main():
    init_playlists()
    root = Tk()
    root.title('Music Player')
    root.geometry(str(WIDTH) + 'x' + str(HEIGHT))
    create_mainscreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
