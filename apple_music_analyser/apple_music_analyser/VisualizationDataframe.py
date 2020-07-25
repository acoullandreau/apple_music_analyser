import pandas as pd
import pickle

from apple_music_analyser.Utility import Utility
from apple_music_analyser.Parser import Parser
from apple_music_analyser.Process import ProcessTracks, TrackSummaryObject

class VisualizationDataframe():

    '''
        This class is responsible for generating a dataframe that can be used for analysis
        and visualizations. This dataframe is obtained after parsing, processing and merging
        several input dataframes, namely the following : 
        - likes_dislikes_df
        - play_activity_df
        - identifier_infos_df
        - library_tracks_df
        and library_activity_df

        Args:
            input_df - a dictionary of dataframes of the followwing format
            {  "identifier_infos_df" : identifier_infos_df,
            "library_tracks_df" : library_tracks_df,
            "library_activity_df" : library_activity_df,
            "likes_dislikes_df" : likes_dislikes_df,
            "play_activity_df" : play_activity_df    }
            This dictionary is obtained from Utility.get_df_from_archive(archive_path), where archive_path is a zip file 
            that must CONTAIN the following structure:
            Apple Music Activity (folder)
                |_ Identifier Information.json.zip
                |_ Apple Music Library Tracks.json.zip
                |_ Apple Music Library Activity.json.zip
                |_ Apple Music Likes and Dislikes.csv
                |_ Apple Music Activity/Apple Music Play Activity.csv

        Raises:
            raises an exception if the input_df doesn't have the format described above

        Methods:
            __init__(input_df)
            get_df_viz()
            get_source_dataframes()
            get_play_activity_df()
            get_identifier_info_df()
            get_library_tracks_df()
            get_library_activity_df()
            get_likes_dislikes_df()
            get_df_from_source()
            process_tracks_in_df()
            build_df_visualisation()

        Modules:
            When creating a new instance of this class, the following process is automatically carried on:
            1. Create a instance of Parser with the input_df
            2. The Parser instance has a source_dataframes dictionary that contains the parsed input_df (parsed = cleaned)
            From this source_dataframes dictionary, get each dataframe.
            3. Create an instance of ProcessTracks
            4. Process each of the individual dataframes
            5. Create an instance of TrackSummaryObject, used in particular to be able to merge infos between dataframes
            6. Build the output df_visualization dataframe
            Refer to the documentation of Parser and Process for more details.

    '''

    def __init__(self, input_df):
        self.input_df = input_df
        self.parser = Parser(input_df)
        self.source_dataframes = self.parser.source_dataframes
        self.likes_dislikes_df = None
        self.play_activity_df = None
        self.identifier_infos_df = None
        self.library_tracks_df = None
        self.library_activity_df = None
        self.get_df_from_source()
        self.process_tracks = ProcessTracks()
        self.process_tracks_in_df()
        self.track_summary_objects = TrackSummaryObject(self.process_tracks.track_instance_dict, self.process_tracks.artist_tracks_titles, self.process_tracks.genres_list, self.process_tracks.items_not_matched)
        self.df_visualization = self.build_df_visualisation()

    def get_df_viz(self):
        return self.df_visualization

    def get_source_dataframes(self):
        return self.source_dataframes

    def get_play_activity_df(self):
        return self.play_activity_df

    def get_identifier_info_df(self):
        return self.identifier_infos_df

    def get_library_tracks_df(self):
        return self.library_tracks_df

    def get_library_activity_df(self):
        return self.library_activity_df

    def get_likes_dislikes_df(self):
        return self.likes_dislikes_df

    def get_df_from_source(self):
        '''
            Sets dataframes as instance properties.
            If the parsing of the input failed (Parser.source_dataframes is empty), an error is raised.
        '''
        if self.source_dataframes != {}:
            # we get the parsed likes dislikes df
            self.likes_dislikes_df = self.parser.likes_dislikes_df
            # we get the parsed play activity df
            self.play_activity_df = self.parser.play_activity_df
            # we get the parsed identifier infos df
            self.identifier_infos_df = self.parser.identifier_infos_df
            # we get the parsed library tracks df
            self.library_tracks_df = self.parser.library_tracks_df
            # we get the parsed library activity df
            self.library_activity_df = self.parser.library_activity_df
        else:
            raise Exception('No source dataframe provided.')

    def process_tracks_in_df(self):
        '''
            Calls the process methods of the ProcessTracks instance on the parsed dataframes.
            If the parsing of the input failed (Parser.source_dataframes is empty), an error is raised.
        '''
        if self.source_dataframes != {}:
            # we process the library tracks
            self.process_tracks.process_library_tracks_df(self.library_tracks_df)
            # # we process the identifier infos
            self.process_tracks.process_identifier_df(self.identifier_infos_df)
            # # we process the play activity
            self.process_tracks.process_play_df(self.play_activity_df)
            # # we process the likes dislikes
            self.process_tracks.process_likes_dislikes_df(self.likes_dislikes_df)
        else:
            raise Exception('No source dataframe provided.')

    def build_df_visualisation(self):
        '''
            Constructs the output dataframe ready for analysis and visualizations. 
            The play_activity dataframe is used as a reference. Are appended to this dataframe three columns
            populated with the information coming from the data structure built with ProcessTracks.
        '''
        # build a dict matching the indexes of play_activity that are linked to a track instance
        # note that this is possible since play_activity_df was used to create/update track instances, and that the index
        # of each row used was recorded by the track instance
        self.track_summary_objects.build_index_track_instance_dict('play_activity')
        match_index_instance_activity = self.track_summary_objects.match_index_instance
        # we create a df from this dict
        index_instance_df = pd.DataFrame.from_dict(match_index_instance_activity, orient='index', columns=['Track Instance', 'Library Track', 'Rating', 'Genres'])
        # we remove the existing 'Genre' column of play_activity_df, and merge the two df
        df_visualization = self.play_activity_df.drop(['Genre'], axis=1, errors='ignore')
        df_visualization = pd.concat([df_visualization,index_instance_df], axis=1)
        # we clean the added columns: 'Rating' and 'Genres' are lists that we transform into str, and we fill NAN of 'Library Track'
        df_visualization['Rating'] = df_visualization['Rating'].apply(Utility.clean_col_with_list)
        df_visualization['Genres'] = df_visualization['Genres'].apply(Utility.clean_col_with_list)
        df_visualization['Library Track'].fillna(False, inplace=True)
        # column names are cleaned up (space replaced by '_').
        df_visualization.columns = [c.replace(' ', '_') for c in df_visualization.columns]
        return df_visualization







