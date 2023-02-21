#!/usr/bin/env python3

from unicodedata import name
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import random
import playlistFunc as pl
import pprint
import sys
import os


# Usage
def usage(status=0):
    print('''Usage: {} [options] 
    -p              PLAYLIST     Generate a new playlist (By Default)
    -q              QUEUE        Add the songs to the back of the queue 
    -f              FAVOURITE    Rank by popularity
    -a [artist]     ARTIST       Get top 10 songs of a given [artist]
    -l [album]      ALBUM        Get all songs in a given [album]
    -r              RANDOM       Shuffle the order of songs
    -h              HELP         Usage
    '''.format(os.path.basename(sys.argv[0])))
    sys.exit(status)



# Main function
def main():
    # Parse Command Lines
    arguments = sys.argv[1:]
    playlist = True
    queue = False
    popularity = False
    artist = False
    album = False
    rdm = False
    artist_name = ""
    album_name = ""

    while arguments and arguments[0].startswith('-'):
        argument = arguments.pop(0)
        if argument == '-p':
            playlist = True
        elif argument == '-q':
            queue = True
            playlist = False
        elif argument == '-f':
            popularity = True
        elif argument == '-a':
            artist = True
            artist_name = arguments.pop(0)
        elif argument == '-l':
            album = True
            album_name = arguments.pop(0)
        elif argument == '-r':
            rdm = True        
        elif argument == '-h':
            usage(0)
        else:
            usage(1)
    
    # Get username
    username = pl.getUserId()

    # Get total time length
    requested_time = pl.getTimeReq()

    # Get Songs
    if artist:
        songs = pl.getSongsFromArtist(artist_name, popularity=popularity)
    elif album:
        songs = pl.getSongsFromAlbum(album_name, popularity=popularity)
    else:
        songs = pl.getSongsFromPlaylist(username, popularity=popularity)

    # Generate final list
    songHeap = pl.loadMaxheap(songs)
    finalList = pl.generateFinalList(songs, songHeap, requested_time, popularity=popularity)

    # Shuffle the list
    if rdm:
        random.shuffle(finalList,random=random.random)

    # Display the final playlist
    pl.displayTrackInfo(finalList, queue=queue)

    # Add to the queue or generate a new playlist
    if playlist:
        pl.generateNewPlaylist(finalList, username, artist=artist, artist_name=artist_name, album=album, album_name=album_name, desire_time=requested_time//60)
    if queue:
        pl.addToQueue(finalList,username)



# Main execution
if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: