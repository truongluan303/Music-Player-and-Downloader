'''
This file is responsible for scraping the data from youtube to look
for the desired song, and then download it to the playlist
'''

import sys
import re
import urllib.request
from subprocess import check_call


def download_song(name: str, artist: str, path: str) -> bool:
    '''
    Download a song as m4a file with the specific name and artist from Youtube
    @return: whether the download was successful
    '''
    if name == '' and artist == '':
        return False
    if not __check_input(name, artist):
        return False
    url = __find_song(name, artist)
    # start with the song name and the folder where it will be stored
    filename = (artist + '-' + name).replace(' ', '_')
    download_to = path + '/' + filename + '.%(ext)s'
    print(download_to)
    # using youtube-dl, download the song as the filename and save it in the input path
    check_call([sys.executable, "-m", "youtube_dl", "-f", 
        'bestaudio[ext=m4a]', url, '-o', download_to])
    return True


def __find_song(name: str, artist: str) -> str:
    '''
    Find the song from youtube and save the audio to the desired playlist.
    The song downloaded will be the first result found.
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
    The input string must only contain letters and numbers. If it does
    contain punctuation marks, then only commas, periods, question marks,
    quotation marks, and exclamation marks are allowed.
    '''
    allowed_punc = {',', '.', '!', '?', '"'}
    for char1, char2 in zip(name, artist):
        if not char1.isalnum() and not char1.isspace():
            if char1 not in allowed_punc:
                return False
        if not char2.isalnum() and not char2.isspace():
            if char2 not in allowed_punc:
                return False
    return True
