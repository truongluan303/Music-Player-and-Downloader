'''
This file is responsible for scraping the data from youtube to look
for the desired song, and then download it to the playlist
'''
# import
import os
import re
import urllib.request
from tkinter import messagebox


def download_song(name: str, artist: str, path: str) -> None:
    '''
    Download a song as m4a file with the specific name and artist from Youtube
    '''
    if name == '' and artist == '':
        messagebox.showerror(title='Error',
            message='Please Enter The Song Name and Artist')
        return
    if not __check_input(name, artist):
        messagebox.showerror(title='Error',
            message='Invalid Input!')
        return
    url = __find_song(name, artist)
    # start with the song name and the folder where it will be stored
    filename = (artist + '-' + name).replace(' ', '_')
    download_to = path + '/' + filename + '.%(ext)s'
    print(download_to)
    # using youtube-dl, download the song as the filename and save it in the input path
    os.system('youtube-dl -f bestaudio[ext=m4a] ' + url + ' -o ' + download_to)
    messagebox.showinfo(title='Done', message='The song is successfully added!')


def __find_song(name: str, artist: str) -> str:
    '''
    Find a song from youtube and save the audio to the desired playlist
    @return: the url to the song on Youtube
    '''
    search_query = name.replace(' ', '+') + '+' + artist.replace(' ', '+')
    search_link = 'https://www.youtube.com/results?search_query=' + search_query
    html = urllib.request.urlopen(search_link)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = "https://www.youtube.com/watch?v=" + video_ids[0]
    return url


def __check_input(name: str, artist: str) -> bool:
    '''
    check if the input is valid
    '''
    return True