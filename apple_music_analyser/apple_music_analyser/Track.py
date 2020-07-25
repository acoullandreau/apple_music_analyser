

class Track():

    '''
        This class allows the representation and description of each track present in a df.
        The instances of this class are songs, identified using either a combination of their
        title and artist names, or an identifier when available
        We track in which file we found the track for (appearance), as well as rating, genre and whether
        it is in the library or not

        Args:
            identifier - a unique id (can be of any type, int, string....)

        Attributes:
            titles (list) - a list of all the titles this track is identifiable with
            artist (str) - the artist of the track
            is_in_lib (bool) - whether the track is in the library
            appearances (list) - a list of dict of the following formats
                {'source': source, 'df_index':index}
                where source can take 4 different values : 
                    - 'play_activity',
                    - 'identifier_info'
                    - 'likes_dislikes'
                    - 'library_tracks'

            genre (list) - a list of all the genres associated with this track
            apple_music_id (list) - a list of all the ids used by Apple to identify the track
            rating (list) - a list of all the ratings associated with this track

        Methods:
            __init__(identifier)
            has_title_name(title)
            add_title(title)
            set_artist(artist)
            set_apple_music_id(apple_music_id)
            set_library_flag()
            set_genre(genre)
            add_appearance(appearance_dict)
            set_rating(rating)
            instantiate_track(title, artist)
            update_track_from_library(index, row)
            update_track_from_play_activity(index, row)

    '''

    def __init__(self, identifier):
        self.identifier = identifier
        self.titles = []
        self.artist = None
        self.is_in_lib = False
        self.appearances = []
        self.genre = []
        self.apple_music_id = []
        self.rating = []
    
    def has_title_name(self, title):
        '''
            Test whether a title is already in self.titles. 
            Returns a boolean.
        '''
        if title in self.titles:
            return True
        return False
    
    def add_title(self, title):
        '''
            Appends a title to self.titles. 
        '''
        self.titles.append(title)
    
    def set_artist(self, artist):
        '''
            Assigns artist to self.artist.
        '''
        self.artist = artist
    
    def set_apple_music_id(self, apple_music_id):
        '''
            Appends apple_music_id if not in self.apple_music_id.
        '''
        if apple_music_id not in self.apple_music_id:
            self.apple_music_id.append(apple_music_id)
               
    def set_library_flag(self):
        '''
            Sets the flag self.is_in_lib to True. 
        '''
        self.is_in_lib = True
    
    def set_genre(self, genre):
        '''
            Appends genre if not NaN and not in self.genre.
        '''
        if type(genre) != float:
            if genre not in self.genre:
                self.genre.append(genre.strip())
        
    def add_appearance(self, appearance_dict):
        '''
            Appends a new appearance dict to self.appearances.
        '''
        self.appearances.append(appearance_dict)

    def set_rating(self, rating):
        '''
            This method uniformises the rating value.
            For LOVE and LIKE it is set to LOVE.
            For DISLIKE it remains DISLIKE.
            For any other rating, nothing is added to the track attribute. 
        '''
        if rating == 'LOVE' or rating == 'LIKE':
            if 'LOVE' not in self.rating:
                self.rating.append(rating)
        elif rating == 'DISLIKE':
            if rating not in self.rating:
                self.rating.append(rating)


    def instantiate_track(self, title, artist):
        '''
            Creates an instance of the Track class, setting both the title and artist
            names used when creating it (multiple titles may be found latter on and added 
            to the list of titles for this track
        '''
        self.add_title(title)
        self.set_artist(artist)


    def update_track_from_library(self, index, row):
        '''
            For a given track instance, updates the properties of the track using the library
            tracks dataframe:
                - its appearance in the library_tracks_info_df, and at which index
                - the genre and rating of the song when available
                - the flag is_in_lib
                - any of the available identifiers used to identify the track
        '''
        self.set_library_flag()
        self.add_appearance({'source': 'library_tracks', 'df_index':index})
        self.set_genre(row['Genre'])
        self.set_rating(row['Track Like Rating'])
        # we add all the unique ids associated to this track,coming from multiple columns of the library_track df
        # Apple Music Track Identifier, Tag Matched Track Identifier or Purchased Track Identifier
        if str(row['Apple Music Track Identifier'])!='nan':
            self.set_apple_music_id(str(int(row['Apple Music Track Identifier'])))
            if str(row['Tag Matched Track Identifier']) !='nan' and row['Tag Matched Track Identifier'] != row['Apple Music Track Identifier']:
                self.set_apple_music_id(str(int(row['Tag Matched Track Identifier'])))
        else:
            self.set_apple_music_id(str(int(row['Track Identifier'])))
            if str(row['Purchased Track Identifier']) !='nan':
                self.set_apple_music_id(str(int(row['Purchased Track Identifier'])))

    def update_track_from_play_activity(self, index, row):
        '''
            For a given track instance, updates the properties of the track using the play
            activity dataframe:
                - its appearance in the play_activity_df, and at which index
                - the genre of the song when available
                - the flag is_in_lib whenever the song was found from the library
        '''
        self.add_appearance({'source': 'play_activity', 'df_index':index})
        self.set_genre(row['Genre'])
        if row['Track origin'] == 'library' and self.is_in_lib is False:
            self.set_library_flag()

