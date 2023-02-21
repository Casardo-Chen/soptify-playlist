#!/usr/bin/env python3

from unicodedata import name
from unittest import result
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import maxHeap
import pprint
import sys
import os

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

name = input("Your artist name: ")
uri = 'spotify:artist:' + spotify.search(q='artist:' + name, type='artist')['artists']['items'][0]['id']
results = spotify.artist_top_tracks(uri)

pprint.pprint(results)
# for track in results['tracks'][:10]:
#     print('track    : ' + track['name'])
#     print('audio    : ' + track['preview_url'])
#     print('cover art: ' + track['album']['images'][0]['url'])
#     print()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: