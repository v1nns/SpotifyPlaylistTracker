import spotipy
import sys, time
from spotipy.oauth2 import SpotifyClientCredentials

"""
download_playlist_tracks.py
    Searches for playlists according to a given string and saves it to a file

    Created in 21/07/2017
    by Vinicius Moura Longaray 
"""

# ############### BEGIN CLASS ############### #
class SpotifyPlaylist:
    seq = 0
    objects = []
    
    def __init__(self, index, playlistName, playlistId, playlistUsername, playlistSize):
        self.index = index
        self.playlistName = playlistName    
        self.playlistId = playlistId
        self.playlistUsername = playlistUsername
        self.playlistSize = playlistSize
        
        self.__class__.seq += 1
        self.id = self.__class__.seq
        self.__class__.objects.append(self)
        
    def __str__(self):
        return self.name
   
    def __repr__(self):
        return '<{}: {} - {} - Size:{} - {} - {}>\n'.format(self.__class__.__name__, self.index, self.playlistName, self.playlistSize, self.playlistUsername, self.playlistId)
   
    # < necessary to iterate through object
    def __iter__(self):
        return iter(self.objects)
        
    def __len__(self):
        return len(self.objects)

    def __getitem__(self, item):
        return self.objects[item]
    # necessary to iterate through object />
    
    @classmethod
    def reset(cls):
        cls.objects = []

    @classmethod
    def all(cls):
        return cls.objects
# ############### END CLASS ############### #
        
def log(str):
    sys.stdout.buffer.write('[{}] {}\n'.format(time.strftime('%H:%M:%S'), str).encode(sys.stdout.encoding, errors='replace'))
    sys.stdout.flush()

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %.02d %32.32s %s" % (i+1, track['artists'][0]['name'],track['name']))

def main():
    SpotifyPlaylist.reset()

    # Client Credentials Flow
    client_credentials_manager = SpotifyClientCredentials('*INSERT YOUR CREDENTIALS*', '*INSERT YOUR CREDENTIALS*')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    log('testando isso aqui')
    # Input data
    string = input('Enter a playlists\' name you want to find: ')
    #string = 'Indie'
    
    # Search for the given string
    results = sp.search(string, type='playlist')
    print()
    #print(results)
    
    # Show the results and save it to an internal structure
    for i, t in enumerate(results['playlists']['items']):
        print(" %d %32.32s - Total tracks: %d" % (i, t['name'], t['tracks']['total']))
        SpotifyPlaylist(i, t['name'], t['id'], t['owner']['id'], t['tracks']['total'])
    
    '''print()
    print(SpotifyPlaylist.all())'''
        
    # Choose the option you want to download
    strOption = input('\nEnter the option you want it: ')
    option = int(strOption)
    while option > i:
        log('Invalid option')
        strOption = input('Enter the option you want it: ')
        option = int(strOption)
    
    option = 0
    
    # Get all the tracks inside that playlist
    print('\n################################# TRACKS #################################\n')
    results = sp.user_playlist(SpotifyPlaylist.objects[option].playlistUsername, SpotifyPlaylist.objects[option].playlistId,fields="tracks,next")
    tracks = results['tracks']
    show_tracks(tracks)
    while tracks['next']:
        tracks = sp.next(tracks)
        show_tracks(tracks)

if __name__ == '__main__':
    main()