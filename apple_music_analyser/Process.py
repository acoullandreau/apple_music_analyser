from apple_music_analyser.Query import Query, QueryFactory
from apple_music_analyser.Track import Track
from apple_music_analyser.Utility import Utility

class ProcessTracks():

    '''
        This class is responsible for building a data structure of tracks from various input dataframes, 
        namely the following : 
        - likes_dislikes_df
        - play_activity_df
        - identifier_infos_df
        - library_tracks_df

        With this class, we identify characteristics of the tracks listened to, and for each of them
        we create and update a instance of the Track class (see Track module for more details).
        Going through the rows of each input dataframe, we try to identify the songs that may
        represent the same track but with different titles, its associated genres, for each artist
        all the songs listened to, etc.

        Args:
            There is no argument to pass to instantiate the class.
        
        Attributes: 
            increment (int) - used to assign a unique id to each track instance
            track_instance_dict (dict) - used to keep track of the title/artist combination with the ref of the associated track instance
            artist_tracks_titles (dict) - used to keep track of all the titles of an artist, including different spellings of the same title
            genres_list (list) - used to keep track of all the unique values of genres
            items_not_matched (dict of lists) - used to keep track of the rows that were not matched in all dataframes processed,
            with the following format
                {'library_tracks':[], 'identifier_info':[],'play_activity':[], 'likes_dislikes':[]}

        Methods:
            __init__()
            get_track_instance_dict()
            get_artist_tracks_titles()
            get_genres_list()
            get_items_not_matched()
            get_increment()
            update_track_instance(origin_df, track_instance, index, row)
            compare_titles_for_artist(artist, title_to_compare)
            process_library_tracks_df(library_tracks_df)
            process_identifier_df(identifier_infos_df)
            process_play_df(play_activity_df)
            process_likes_dislikes_df(likes_dislikes_df)           

        The methods that processes each df can be called seperately, but only process_library_tracks_df and process_play_df will create
        new instances of Track (the other can only update existing instances). Besides, process_identifier_df requires that the
        existing instances of Tracks have their attribute apple_music_id populated, so it should be executed after processing
        the library_tracks_df.
        Therefore it makes sense to call the methods in this order (2 and 3 can be swapped):
            1. process_library_tracks_df(library_tracks_df)
            2. process_identifier_df(identifier_infos_df)
            3. process_play_df(play_activity_df)
            4. process_likes_dislikes_df(likes_dislikes_df)
    '''


    def __init__(self):
        ## this is used to assign a unique id to each track instance
        self.increment = 0
        ## this is used to keep track of the title/artist combination with the ref of the associated track instance
        self.track_instance_dict = {}
        ## this is used to keep track of all the titles of an artist, including different spellings of the same title
        self.artist_tracks_titles = {}
        ## this is used to keep track of all the unique values of genres
        self.genres_list = []
        ## this is used to keep track of the rows that were not matched in all dataframes processed
        ## can be used to spot why a given row was excluded from the track instances
        self.items_not_matched = {'library_tracks':[], 'identifier_info':[],
                             'play_activity':[], 'likes_dislikes':[]}


    def get_track_instance_dict(self):
        return self.track_instance_dict

    def get_artist_tracks_titles(self):
        return self.artist_tracks_titles

    def get_genres_list(self):
        return self.genres_list

    def get_items_not_matched(self):
        return self.items_not_matched
  
    def get_increment(self):
        return self.increment

    def update_track_instance(self, origin_df, track_instance, index, row):
        '''
            This function calls update_track_from_play_activity or 
            update_track_from_library depending on origin_df. It also 
            updates the genres_list object.
            It is used to simplify the structure of the processing methods.
        '''
        if origin_df == 'play_activity_df':
            track_instance.update_track_from_play_activity(index, row)
            if row['Genre'] not in self.genres_list:
                self.genres_list.append(row['Genre'])
        elif origin_df == 'library_tracks_df':
            track_instance.update_track_from_library(index, row)
            if row['Genre'] not in self.genres_list:
                self.genres_list.append(row['Genre'])
        else:
            print('There is no method to update a track instance from another dataframe than play_activity_df or library_tracks_df')


    def compare_titles_for_artist(self, artist, title_to_compare):
        '''
            Compares the string similarity of any song associated to an artist and an unknown
            title for this artist. The goal here is to be able to match different spellings of 
            the same song. 
            If the similarity score is above the threshold set, it returns the track instance
            of the matching artist song we already know. 
            Otherwise it returns 'No match'.
        '''
        for artist_track in self.artist_tracks_titles[artist]:
            title_similarity_for_artist = Utility.compute_similarity_score(title_to_compare, artist_track)
            # value observed to bring consistently a match between similar songs
            if title_similarity_for_artist > 0.625:
                #we fetch the track instance associated with the close match
                title_artist = Utility.concat_title_artist(artist_track, artist)
                track_instance = self.track_instance_dict[title_artist]
                return track_instance
        return 'No match'


    def process_library_tracks_df(self, library_df):
        '''
            This function goes through each row of the library tracks dataframe, creating and updating
            track instances as they appear.
            As this is the first dataframe we go through, we want to create new instances whenever
            we are not facing unknown songs (NaN as a title)
            The logic works as follows, knowing that we do this for each row of the dataframe:
                - we look only at rows with a title different than NaN, and we set the artist to
                'No Artist' if the artist is also Nan
                - if the track is not in the dictionary of track instances, it means that we never
                saw the combination title/artist of this row. So two options here:
                    - either we know this artist and we can find a similar title in the artist dict, and in
                    this case we update the existing track using update_track_from_library
                    - or we do not know this artist, or we do not find a close match of title for this artist
                    and in this case we create a new track instance using instantiate_track and then
                    update_track_from_library
                - else, we update the existing track using update_track_from_library
        '''
        for index, row in library_df.iterrows():
            if str(row['Title']) != 'nan':
                title = row['Title']
                if str(row['Artist']) != 'nan':
                    artist = row['Artist']
                else:
                    artist = 'No Artist'

                title_artist = Utility.concat_title_artist(title, artist)

                if title_artist not in self.track_instance_dict.keys():
                    if artist in self.artist_tracks_titles.keys():
                        titles_comparison_result = self.compare_titles_for_artist(artist, title)

                        if titles_comparison_result == 'No match':
                            #we instantiate the Track object
                            track_instance = Track(self.increment)
                            track_instance.instantiate_track(title, artist)
                            self.update_track_instance('library_tracks_df', track_instance, index, row)
                            self.track_instance_dict[title_artist] = track_instance
                            self.increment += 1

                        else:
                            track_instance = titles_comparison_result
                            if not track_instance.has_title_name(title):
                                track_instance.add_title(title)
                            self.update_track_instance('library_tracks_df', track_instance, index, row)
                            self.track_instance_dict[title_artist] = track_instance
                            self.artist_tracks_titles[artist].append(title)
                    
                    else:
                        #there was no close match, and the song was never seen, so we instantiate a new Track
                        track_instance = Track(self.increment)
                        track_instance.instantiate_track(title, artist)
                        self.update_track_instance('library_tracks_df', track_instance, index, row)
                        self.track_instance_dict[title_artist] = track_instance
                        self.increment += 1


                else:
                    track_instance = self.track_instance_dict[title_artist]
                    self.update_track_instance('library_tracks_df', track_instance, index, row)


                #we update the artist/track names dictionnary
                if artist not in self.artist_tracks_titles:
                    self.artist_tracks_titles[artist]=[]
                if title not in self.artist_tracks_titles[artist]:
                    self.artist_tracks_titles[artist].append(title)
            else:
                self.items_not_matched['library_tracks'].append(index)



    def process_identifier_df(self, identifier_df):
        '''
            This function goes through each row of the identifier information dataframe, updating
            track instances as they appear.
            Unlike for the tracks dataframe, we have very limited information here, just an identifier
            and a title (not even an artist name). So we need to have a different approach, only
            based on the identifiers. Which may excluse some songs... But prevents false positives.
            The logic works as follows, knowing that we do this for each row of the dataframe:
                - we loop through all the track instances we created so far, and see if any of their 
                identifier matches the id of the row we are looking at
                - if it matches, and if we didn't already have the associated title, we add it to the
                list of titles of that track
                - otherwise, we add it to the tracks we could not match and we ignored.
        '''
        for index, row in identifier_df.iterrows():
            found_match = False
            for title_name in self.track_instance_dict.keys():
                track_instance = self.track_instance_dict[title_name]
                if row['Identifier'] in track_instance.apple_music_id:
                    track_instance.add_appearance({'source': 'identifier_info', 'df_index':index})
                    if not track_instance.has_title_name(row['Title']):
                        track_instance.add_title(row['Title'])
                    found_match = True
                    break
            if found_match is False:
                self.items_not_matched['identifier_info'].append((index, row['Identifier']))


    def process_play_df(self, play_activity_df):
        '''
            This function goes through each row of the play activity dataframe, creating and updating
            track instances as they appear.
            As this is the dataframe we are able to get the most information from, we want to create
            new instances whenever we are not facing unknown songs (NaN as a title).The approach is
            very similar to the one used for the library tracks.
            
            The logic works as follows, knowing that we do this for each row of the dataframe:
                - if the track is in the dictionary of track instances, we update the existing
                track using update_track_from_play_activity
                - else, we have two options :
                    - either we know this artist and we can find a similar title in the artist dict,
                    and in this case we update the existing track using update_track_from_play_activity
                    - or we do not know this artist, or we do not find a close match of title for this
                    artist and in this case we create a new track instance using instantiate_track and
                    then update_track_from_play_activity
        '''
        for index, row in play_activity_df.iterrows():
            #we want to look only at rows where the name of the song is available
            if str(row['Title']) != 'nan':
                title = row['Title']
                if str(row['Artist']) != 'nan':
                    artist = row['Artist']
                else:
                    artist = 'No Artist'
            else:
                self.items_not_matched['play_activity'].append(index)
                continue

            #we check if we already saw this track (using title and artist names)
            title_artist = Utility.concat_title_artist(title, artist)
            if title_artist in self.track_instance_dict.keys():
                track_instance = self.track_instance_dict[title_artist]
                self.update_track_instance('play_activity_df', track_instance, index, row)

            else:
                # if we had no match with title and artist, we look for similarity in the title for the artist
                if artist in self.artist_tracks_titles.keys():
                    titles_comparison_result = self.compare_titles_for_artist(artist, title)
                    if titles_comparison_result == 'No match':
                        #we instantiate the Track object
                        track_instance = Track(self.increment)
                        track_instance.instantiate_track(title, artist)
                        self.update_track_instance('play_activity_df', track_instance, index, row)
                        #we update the dictionary that keeps track of our instances, titles of artists, and increment
                        self.track_instance_dict[title_artist] = track_instance
                        self.artist_tracks_titles[artist].append(title)
                        self.increment+=1

                    else:
                        track_instance = titles_comparison_result
                        if not track_instance.has_title_name(title):
                            track_instance.add_title(title)
                        track_instance.add_appearance({'source': 'play_activity', 'df_index':index})
                        #we also track the match in the track_instances and artist dicts
                        self.track_instance_dict[title_artist] = track_instance
                        self.artist_tracks_titles[artist].append(title)

                # else we know we never saw this track because the artist is unknown      
                else:
                    #we update the artist/track names dictionnary
                    self.artist_tracks_titles[artist]=[]
                    self.artist_tracks_titles[artist].append(title)

                    #we instantiate the Track object
                    track_instance = Track(self.increment)
                    track_instance.instantiate_track(title, artist)
                    self.update_track_instance('play_activity_df', track_instance, index, row)

                    #we update the dictionary that keeps track of our instances, and increment
                    self.track_instance_dict[title_artist] = track_instance
                    self.increment+=1

    def process_likes_dislikes_df(self, likes_dislikes_df):
        '''
            This function goes through each row of the likes_dislikes dataframe, updating
            track instances as they appear.
            This dataframe contains a small proportion of all the tracks ever listened to, and/or in
            the library. As a result, we only want to update existing tracks, and not create new ones.
            The logic works as follows, knowing that we do this for each row of the dataframe:
                - we loop through all the track instances we created so far, and see if any of their 
                identifier matches the id of the row we are looking at
                - if we find a match, we update the track with the rating, appearance, and if we didn't
                already have the associated title, we add it to the list of titles of that track
                - else:
                    - if the track is in the dictionary of track instances, we update the existing
                track's rating and appearance
                    - otherwise, we have two options:
                        - either we know the artist and we can find a similar title in the artist dict,
                    and in this case we update the existing track
                        - or we do not know this artist, or we do not find a close match of title for this
                    artist and in this case we add it to the tracks we could not match and we ignored
        ''' 
        for index, row in likes_dislikes_df.iterrows():
            #we want to look only at rows where the name of the song is available
            if str(row['Title']) != 'nan':
                title = row['Title']
                if str(row['Artist']) != 'nan':
                    artist = row['Artist']
                else:
                    artist = 'No Artist'
            else:
                self.items_not_matched['likes_dislikes'].append(index)
                continue

            title_artist = Utility.concat_title_artist(title, artist)

            # first we check using the Item Reference as an id
            found_match = False
            for title_name in self.track_instance_dict.keys():
                track_instance = self.track_instance_dict[title_name]
                if row['Item Reference'] in track_instance.apple_music_id:
                    track_instance.add_appearance({'source': 'likes_dislikes', 'df_index':index})
                    track_instance.set_rating(row['Preference'])
                    if not track_instance.has_title_name(row['Title']):
                        track_instance.add_title(row['Title'])
                        self.track_instance_dict[title_artist] = track_instance
                        if row['Title'] not in self.artist_tracks_titles[artist]:
                            self.artist_tracks_titles[artist].append(title)
                    found_match = True
                    break

            if found_match is False:
                #we check if we already saw this track (using title and artist names)
                if title_artist in self.track_instance_dict.keys():
                    track_instance = self.track_instance_dict[title_artist]
                    track_instance.add_appearance({'source': 'likes_dislikes', 'df_index':index})
                    track_instance.set_rating(row['Preference'])

                else:
                    # if we had no match with title and artist, we look for similarity in the title for the artist
                    if artist in self.artist_tracks_titles.keys():
                        titles_comparison_result = self.compare_titles_for_artist(artist, title)
                        if titles_comparison_result == 'No match':
                            #we add the item to the items_not_matched
                            self.items_not_matched['likes_dislikes'].append(index)
                        else:
                            track_instance = titles_comparison_result
                            if not track_instance.has_title_name(title):
                                track_instance.add_title(title)
                            track_instance.add_appearance({'source': 'likes_dislikes', 'df_index':index})
                            track_instance.set_rating(row['Preference'])
                            self.track_instance_dict[title_artist] = track_instance
                            self.artist_tracks_titles[artist].append(title)
                    else:
                        #we add the item to the items_not_matched,
                        #we choose not to add it to the Track instances as the amount of information is little
                        #and our reference really is the play activity!
                        self.items_not_matched['likes_dislikes'].append(index)
                        continue





class TrackSummaryObject():

    '''
        This class is responsible for building two main types of objects using the data structure of tracks
        constructed by Process.ProcessTracks :
        - count dictionaries
        - dataframe index / track instance matching dictionary
        
        The dataframe index / track instance matching dictionary is used to be able to add information
        from the track instances to any of the input dataframes, at the relevant rows. For example, we may
        want to add a pointer to the track instance in a df, or add the rating associated to the track to 
        a dataframe that doesn't contain this information. 
        As part of building the data structure of tracks, we keep track of the "appearance" property,
        that matches the dataframe name with the index we saw the track in.

        Args:
            ------ For the instance
            The attributes of a ProcessTracks class
            track_instance_dict - dictionary that contains a 'title && artist' combined key, and the
            reference of the associated track instance
            artist_tracks_titles - dictionary that contains the artist name as a key and an array of titles
            associated to this artist
            genres_list - list of all the unique values of genres
            items_not_matched - dictionary of the following structure listing all the indexes associated
            with each df processed
                {'library_tracks':[], 'identifier_info':[],'play_activity':[], 'likes_dislikes':[]}

        Methods:
            __init__(track_instance_dict, artist_tracks_titles, genres_list, items_not_matched)
            get_track_instance_dict()
            get_artist_tracks_titles()
            get_genres_list()
            get_items_not_matched()
            get_match_index_instance()
            build_index_track_instance_dict(target_df_label)
            simplify_genre_list(genres_list)
            build_genres_count_dict(genres_serie)
            build_count_dict(target_serie)
            build_ranking_dict_per_year(df, ranking_target, query_params=None)

    '''

    def __init__(self, track_instance_dict, artist_tracks_titles, genres_list, items_not_matched):
        self.track_instance_dict = track_instance_dict
        self.artist_tracks_titles = artist_tracks_titles
        self.genres_list = TrackSummaryObject.simplify_genre_list(genres_list)
        self.items_not_matched = items_not_matched
        self.match_index_instance = {}

    def get_track_instance_dict(self):
        return self.track_instance_dict

    def get_artist_tracks_titles(self):
        return self.artist_tracks_titles

    def get_genres_list(self):
        return self.genres_list

    def get_items_not_matched(self):
        return self.items_not_matched
  
    def get_match_index_instance(self):
        return self.match_index_instance

    def build_index_track_instance_dict(self, target_df_label):
        '''
            Returns a dictionary matching the index of the target dataframe with a reference to its
            associated Track instance.
            
            Argument can be of four types, for the four df we used to build the Track instances:
                - play_activity
                - library_tracks
                - likes_dislikes
                - identifier_info
        '''
        # for each combination of 'title && artist', we look at the appearances of the associated track instance
        for title_artist in self.track_instance_dict.keys():
            instance = self.track_instance_dict[title_artist]
            for appearance in instance.appearances:
                # if the targeted df is listed among the recorded appearances, we add the related indexes to a dict
                # along with the instance reference, the library flag, the rating and the genre(s)
                if target_df_label in appearance['source']:
                    if appearance['df_index'] not in self.match_index_instance:
                        self.match_index_instance[appearance['df_index']] = []
                    if instance not in self.match_index_instance[appearance['df_index']]:
                        self.match_index_instance[appearance['df_index']].append(instance)
                        self.match_index_instance[appearance['df_index']].append(instance.is_in_lib)
                        self.match_index_instance[appearance['df_index']].append(instance.rating)
                        self.match_index_instance[appearance['df_index']].append(instance.genre)

    @staticmethod
    def simplify_genre_list(genres_list):
        '''
            This method will replace NaN value with '' and remove extra spaces.
        '''
        genres_list_clean = [x if str(x) != 'nan' else '' for x in genres_list]
        genres_list_clean = [x.strip() for x in genres_list_clean]
        return genres_list_clean


    def build_genres_count_dict(self, genres_serie):
        '''
            This method builds a dictionary with a genre as a key and a count of occurence of
            this genre as a value, using a pandas serie as an input.
        '''
        genres_count_dict = {}
        # we add a key per unique genre listed in genres_list
        for ref_genre in self.genres_list:
            genres_count_dict[ref_genre] = 0
        # for each element of genre array in genres_serie, we increment the count in the dict
        for genre_in_serie in genres_serie.tolist():
            if '&&' in genre_in_serie:
                genres = genre_in_serie.split('&&')
                for genre in genres:
                    if genre.strip() in genres_count_dict.keys():
                        genres_count_dict[genre.strip()] += 1
            else:
                if genre_in_serie in genres_count_dict.keys():
                    genres_count_dict[genre_in_serie] += 1
        return genres_count_dict

    def build_count_dict(self, target_serie):
        '''
            This method builds a dictionary with a target element as a key (for example Artist, Title)
            and a count of occurence of this element as a value, using a pandas serie as an input.
        '''
        ref_list = target_serie.unique()
        
        count_dict = {}
        # we add a key per unique genre not NaN available in target_serie
        for ref_elem in ref_list:
            if str(ref_elem) != 'nan':
                count_dict[ref_elem] = 0

        # for each element in target_serie, we increment the count in the dict
        for df_elem in target_serie.tolist():
            if str(df_elem) != 'nan':
                if df_elem in count_dict.keys():
                    count_dict[df_elem] += 1
            else:
                continue      
        return count_dict

    def build_ranking_dict_per_year(self, df, ranking_target, query_params=None):
        '''
            This method builds a dictionary of dictionaries of counts. 
            The keys of the output dict is a year, and for each year, the value is a 
            count dict for a target element (for example Genre, Artist, Title). 

            Args:
                df - the dataframe from which series are used to build count dict
                    This dataframe MUST contain at least a column Play_Year and the
                    column used as a target element (see below)
                ranking_target - the target to use for the count dict, can be of four types:
                    - Genres
                    - Artist
                    - Track_origin
                    - Title
                    The choosen target MUST be a column name of the input dataframe.
                query_param - OPTIONAL, used to perform a filter on the dataframe.

            Logic:
                - if no filtering parameters are passed, the output dict will have one
                key per year present in the input df (column 'Play_Year')
                - for each year, if further filtering is required, a filtered_df is constructed
                and a count dict is built using the appropriate function (build_genres_count_dict
                if the target is 'Genres', build_count_dict otherwise)

        '''
        ranking_dict = {}
        if query_params == None:
            query_params = {
                'year':df['Play_Year'].unique(),
            }
        
        years = query_params['year']
        for year in years:
            instance_params = query_params
            instance_params['year'] = [year]
            query_instance = QueryFactory().create_query(df, instance_params)
            filtered_df = query_instance.get_filtered_df()
            if ranking_target == 'Genres':
                ranking_dict[year] = self.build_genres_count_dict(filtered_df[ranking_target])
            elif ranking_target in ['Artist', 'Track_origin', 'Title']:
                ranking_dict[year] = self.build_count_dict(filtered_df[ranking_target])   
        
        return ranking_dict



