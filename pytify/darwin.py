from __future__ import absolute_import, unicode_literals
import sys
import subprocess
from pytify.pytifylib import Pytifylib
import os
import spotipy
import spotipy.util as util


class Darwin(Pytifylib):
    def __init__(self):
        """
            Check if there is a Spotify process running and if not,
            run Spotify.
        """
        try:
            count = int(subprocess.check_output([
                    'osascript',
                    '-e', 'tell application "System Events"',
                    '-e', 'count (every process whose name is "Spotify")',
                    '-e', 'end tell'
                ]).strip())
            if count == 0:
                print('\n[OPENING SPOTIFY] The Spotify app was not open.\n')

                self._make_osascript_call(
                    'tell application "Spotify" to activate'
                )
        except Exception:
            sys.exit('You don\'t have Spotify installed. Please install it.')

    def _make_osascript_call(self, command):
        subprocess.call([
            'osascript',
            '-e',
            command
        ])

    def listen(self, index):
        uri = self._get_song_uri_at_index(index)
        self._make_osascript_call(
            'tell app "Spotify" to play track "%s"' % uri
        )

    def next(self):
        self._make_osascript_call('tell app "Spotify" to next track')

    def prev(self):
        self._make_osascript_call('tell app "Spotify" to previous track')

    def play_pause(self):
        self._make_osascript_call('tell app "Spotify" to playpause')

    def pause(self):
        self._make_osascript_call('tell app "Spotify" to pause')

    def get_current_playing(self):
        instruction = ('on getCurrentTrack()\n'
            ' tell application "Spotify"\n'
            '  set currentArtist to artist of current track as string\n'
            '  set currentTitle to name of current track as string\n'
            '  return currentArtist & " - " & currentTitle\n'
            ' end tell\n'
            'end getCurrentTrack\n'
            'getCurrentTrack()')
        proc = subprocess.Popen(
            ['osascript', '-e', instruction],
            stdout=subprocess.PIPE)
        out, err = proc.communicate()
        return out.decode(sys.getfilesystemencoding())
    def get_current_id(self):
        instruction = ('on getCurrentID()\n'
            ' tell application "Spotify"\n'
            '  set currentID to id of current track as string\n'
            '  return currentID\n'
            ' end tell\n'
            'end getCurrentID\n'
            'getCurrentID()')
        proc = subprocess.Popen(
            ['osascript', '-e', instruction],
            stdout=subprocess.PIPE)
        out, err = proc.communicate()
        return out.decode(sys.getfilesystemencoding())

    def _get_spotify(self):
        token = util.prompt_for_user_token('1234973619', self._scope, client_id=os.environ.get('SPOTIFY_CLIENT_ID'), client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET'), redirect_uri='http://localhost/')
        spotify = spotipy.Spotify(auth=token)
        return spotify

    def add_mellow(self):
        current_id = [self.get_current_id()[:-1]]
        playlist_id = 'spotify:playlist:6k93RmdQbCriD0H9HhR1ki'
        sp = self._get_spotify()
        new_offset = 0
        check_playlist = sp.user_playlist_tracks('1234973619', playlist_id,offset=0)
        total_songs=int(check_playlist['total'])
        while new_offset < total_songs:
            try:
                new_offset = int(check_playlist['next'].split('?')[1].split('&')[0].split('=')[1])
            except AttributeError:
                new_offset = total_songs
            for item in check_playlist['items']:
                if item['track']['uri'] == current_id[0]:
                    return print('found it, skipping duplicates')
            check_playlist = sp.user_playlist_tracks('1234973619', playlist_id,offset=new_offset)
            print('Checking {0}'.format(new_offset))
        result = sp.user_playlist_add_tracks('1234973619', playlist_id, current_id)
        return print(result)

    def add_favorite(self):
        current_id = [self.get_current_id()[:-1]]
        playlist_id = 'spotify:playlist:70Wde6Rr7M1WxwIqEy9kmO'
        sp = self._get_spotify()
        new_offset = 0
        check_playlist = sp.user_playlist_tracks('1234973619', playlist_id,offset=0)
        total_songs=int(check_playlist['total'])
        while new_offset < total_songs:
            try:
                new_offset = int(check_playlist['next'].split('?')[1].split('&')[0].split('=')[1])
            except AttributeError:
                new_offset = total_songs
            for item in check_playlist['items']:
                if item['track']['uri'] == current_id[0]:
                    return print('found it, skipping duplicates')
            check_playlist = sp.user_playlist_tracks('1234973619', playlist_id,offset=new_offset)
            print('Checking {0}'.format(new_offset))
        result = sp.user_playlist_add_tracks('1234973619', playlist_id, current_id)
        return print(result)
