#!/usr/bin/env python3

from unicodedata import name
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import maxHeap
import pprint
import sys
import os

# Functions
def getUserId():
    username = input('Please type your Spotify username: ')
    return username



def getTimeReq():
    input_time = input('Please enter the requested time (min): ')
    requested_time = 60 * int(input_time)
    return requested_time



def convertTime(millis):
    seconds=(millis/1000)%60
    strs = "%02d" % seconds 
    minutes=(millis/(1000*60))%60
    strm = "%02d" % minutes 
    print(strm,":",strs, end='      ')



def loadMaxheap(songs):
    songHeap = maxHeap.MaxHeap(capacity=1000)
    for song in songs:
        songHeap.insert(song, songs[song])
    return songHeap



def generateFinalList(songs, songHeap, desire_time, popularity=False):
    auth_manager = SpotifyClientCredentials()
    sp=spotipy.Spotify(auth_manager=auth_manager)
    final_list = []
    while (desire_time >= -30 and (not songHeap.isEmpty())):
        song_uri = songHeap.popMax()
        if song_uri != '' and song_uri != 'init':
            if popularity:
                song_duration = sp.track(song_uri)['duration_ms']/1000
                if desire_time + 30 >= song_duration:
                    desire_time -= song_duration
                    final_list.append(song_uri)
            else:
                song_duration = songs[song_uri]
                if desire_time + 30 >= song_duration:
                    desire_time -= song_duration
                    final_list.append(song_uri)
    return final_list



def getSongsFromPlaylist(username, popularity=False):
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    # Get User Playlists
    playlists = sp.user_playlists(username)
    playlist_dict = {}

    # Display all playlists
    print('We find these playlists:')
    while playlists:
        for i, playlist in enumerate(playlists['items']):
                playlist_dict[i+1] = playlist_dict.get(i+1,playlist['name'])
                print("%d  %s" % (i+1, playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
        
    # Ask User to choose a playlist
    playlist_name = playlist_dict[int(input('Please enter the index of the desired playlist: '))]
    playlist_uri = 0
    playlists2 = sp.user_playlists(username)
    while playlists2:
        for i, playlist in enumerate(playlists2['items']):
                if playlist['name'] == playlist_name:
                    playlist_uri = playlist['uri']
        if playlists2['next']:
            playlists2 = sp.next(playlists2)
        else:
            playlists2 = None
    # Get songs
    tracks = sp.user_playlist_tracks(username, playlist_uri)
    total_songs = tracks['total']
    songs = {}
    for i in range(0, total_songs):
        uri = tracks['items'][i]['track']['uri']
        if popularity:
            popularity = tracks['items'][i]['track']['popularity']
            songs[uri] = songs.get(uri,popularity)
        else:
            time = tracks['items'][i]['track']['duration_ms']/1000
            songs[uri] = songs.get(uri,time)
    # return the list of songs
    return songs



def getSongsFromArtist(artist, popularity=False):
    songs = {}
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    uri = 'spotify:artist:' + spotify.search(q='artist:' + artist, type='artist')['artists']['items'][0]['id']
    results = spotify.artist_top_tracks(uri)
    for track in results['tracks']:
        uri = track['uri']
        if popularity:
            popularity = track['popularity']
            songs[uri] = songs.get(uri,popularity)
        else:
            time = track['duration_ms']/1000
            songs[uri] = songs.get(uri,time)
    # return the list of songs
    return songs



def getSongsFromAlbum(album, popularity=False):
    songs = {}
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    album_uri = spotify.search(q='album:' + album, type='album')['albums']['items'][0]['uri']
    results = spotify.album_tracks(album_uri)['items']
    for track in results:
        uri = track['uri']
        if popularity:
            popularity = spotify.track(uri)['popularity']
            songs[uri] = songs.get(uri,popularity)
        else:
            time = track['duration_ms']/1000
            songs[uri] = songs.get(uri,time)
    # return the list of songs
    return songs



def displayTrackInfo(final_list, queue=False):
    auth_manager = SpotifyClientCredentials()
    sp=spotipy.Spotify(auth_manager=auth_manager)
    if queue:
        print("We've added these songs to your queue")
    else:
        print("We've created a new playlist containing these songs")
    print('No.'.ljust(3), end='      ')
    print('Time'.ljust(7), end='      ')
    print('Popularity'.ljust(10), end='      ')
    print('Title'.ljust(6))
    for i, song in enumerate(final_list):
        result =sp.track(song)
        print(f'{i+1:<3}', end='      ')
        # song time
        convertTime(result['duration_ms'])
        # popularity
        popularity = result['popularity']
        print(f'{popularity:<10}', end='      ')
        # song name
        print("%s" % result['name'])



def addToQueue(final_list,username):
    auth_manager = SpotifyOAuth(scope='user-modify-playback-state', username=username)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    for song in final_list:
        sp.add_to_queue(song)



def generateNewPlaylist(songlist, username, artist=False, artist_name="", album=False, album_name="", desire_time=0):
    scope = 'playlist-modify-public'
    token = SpotifyOAuth(scope=scope,username=username)
    spotifyObject = spotipy.Spotify(auth_manager = token)
    #create the playlist
    if artist:
        playlist_name = "New Playlist of " + artist_name +" " + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    elif album:
        playlist_name = "New Playlist of " + album_name +" " + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    else:
        playlist_name = "New Playlist " + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    play_description = "A ~" + str(desire_time) + "min playlist generated by Spotify Playlist Optimizer. Enjoy!"
    spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True, description=play_description)
    # find the new playlist
    prePlaylist = spotifyObject.user_playlists(user=username)
    playlist = prePlaylist['items'][0]['id']
    # add songs 
    spotifyObject.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=songlist)

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: