import pandas as pd
import numpy as np
from apple_music_analyser.Utility import Utility

class Parser():

    '''
        Instances of this class are in charge of parsing input dataframes. By parsing, understand
        performing a sequence of operations to wrangled the data (add relevant columns, remove outliers,
        missing values, ...) and simplify the df (remove columns). 

        When creating a new instance of this class, parse_input_df and parse_source_dataframes are automatcally executed.
        parse_input_df will validate the input provided (argument source_files) and create a source_dataframes dict.
        parse_source_dataframes will parse the dataframes in the newly created source_dataframes dict.

        Args:
            source_files - a dictionary of dataframes of the followwing format
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
        
        Attributes: 
            source_files - dictionary of dataframes (see Args for more details)
            source_dataframes - a dictionary of the same structure that source_files, but where the values are parsed df


        Raise:
            raises an exception if the source_files could not be properly parsed (see description above).

        Methods:
            __init__(source_files)
            parse_input_df(source_files)
            parse_source_dataframes()
            parse_library_activity_df(library_activity_df)
            parse_play_activity_df(play_activity_df, convert_to_local_time = True, drop_columns=True)
            parse_library_tracks_infos_df(library_tracks_infos_df)
            parse_likes_dislikes_df(likes_dislikes_df)
            set_partial_listening(play_activity_df, end_reason_type, play_duration, media_duration)
            get_track_origin(serie)
            compute_play_duration(play_activity_df, start, end, played_completely, play_duration, media_duration)
            remove_play_duration_outliers(play_activity_df, play_duration, media_duration, percentile)

    '''

    def __init__(self, source_files):
        self.source_files = source_files
        self.source_dataframes = self.parse_input_df(self.source_files)
        self.parse_source_dataframes()

    @staticmethod
    def parse_input_df(source_files):
        '''
            This method is in charge of validating the format of the input source_files.
            If the provided input doesn't contain the required files, or if their format is incorrect, no
            further parsing/processing is possible - so it is important to report the problem early in the process!
            This method simply prints a warning message.
            Otherwise, the dataframes dictionary is populated with the input dataframes. 
        '''

        error_message_bad_input = ("Please ensure that the input_df object has the following structure...\n"

        '{  "identifier_infos_df" : identifier_infos_df, "library_tracks_df" : library_tracks_df,\n'
        '"library_activity_df" : library_activity_df, "likes_dislikes_df" : likes_dislikes_df, "play_activity_df" : play_activity_df    }\n'

        '...And that the values in this dictionary are pandas dataframes. Returned object is empty.')

        dataframes = {}
        if len(source_files) != 5:
            print('WARNING:\n {0}'.format(error_message_bad_input))

        else:
            if Utility.validate_input_df_files(source_files):
                dataframes['likes_dislikes_df'] = source_files['likes_dislikes_df']
                dataframes['play_activity_df'] = source_files['play_activity_df']
                dataframes['identifier_infos_df'] = source_files['identifier_infos_df']
                dataframes['library_tracks_df'] = source_files['library_tracks_df']
                dataframes['library_activity_df'] = source_files['library_activity_df']
            else:
                print('WARNING:\n {0}'.format(error_message_bad_input))
        
        return dataframes


    def parse_source_dataframes(self):
        '''
            If at the previous stage (parse_input_df) an empty self.source_dataframes dictionary was returned, no
            further parsing/processing is possible. Therefore this method will raise an exception.
            If self.source_dataframes is not empty, then we know for sure that the input is correct, and we can
            parse each df individually, calling the following methods:
            parse_library_activity_df(library_activity_df)
            parse_play_activity_df(play_activity_df, convert_to_local_time = True, drop_columns=True)
            parse_library_tracks_infos_df(library_tracks_infos_df)
            parse_likes_dislikes_df(likes_dislikes_df)
        '''
        if self.source_dataframes != {}:
            self.likes_dislikes_df = self.parse_likes_dislikes_df(self.source_dataframes['likes_dislikes_df'])
            self.play_activity_df = self.parse_play_activity_df(self.source_dataframes['play_activity_df'])
            self.identifier_infos_df = self.source_dataframes['identifier_infos_df']
            self.library_tracks_df = self.parse_library_tracks_infos_df(self.source_dataframes['library_tracks_df'])
            self.library_activity_df = self.parse_library_activity_df(self.source_dataframes['library_activity_df'])
        else:
            raise Exception('No source dataframe provided. Please verify the format of the input_files dictionary you provided.')


    @staticmethod
    def parse_library_activity_df(library_activity_df):
        '''
            Method in charge of parsing the library activity dataframe.
            It is responsible for adding time columns from the timestamp column (year, month, day of the month,...), as well
            as agent columns (what performed the action, what model).

        '''
        parsed_df = library_activity_df.copy()
        # parse time related column
        parsed_datetime_series = Utility.parse_date_time_column(parsed_df, 'Transaction Date')
        Utility.add_time_related_columns(parsed_df, parsed_datetime_series, col_name_prefix='Transaction ')
    
        # parse action agent column
        parsed_df['Transaction Agent'] = parsed_df['UserAgent'].str.split('/').str.get(0)
        parsed_df.replace({'Transaction Agent' : { 'itunescloudd' : 'iPhone', 'iTunes' : 'Macintosh'}}, inplace=True)
        parsed_df['Transaction Agent Model'] = parsed_df[parsed_df['Transaction Agent'] == 'iPhone']['UserAgent'].str.split('/').str.get(3).str.split(',').str.get(0)
        parsed_df.loc[parsed_df['Transaction Agent'].eq('Macintosh'), 'Transaction Agent Model'] = 'Macintosh'

        return parsed_df

    @staticmethod
    def parse_play_activity_df(play_activity_df, convert_to_local_time = True, drop_columns=True):
        '''
            Method in charge of parsing the play activity dataframe. The parsing is performed in multiple steps:
            1. Rename the columns containing song title and artist
            2. Time columns: first obtain a timestamp column without missing values, using Event Start Timestamp and Event End Timestamp
            3. Time columns: add time columns from the timestamp column (year, month, day of the month,...), with or without conversion
            to local time (args)
            4. Remove outlier rows (Apple Music service started in 2015, so we drop rows with a year before 2015)
            5. Add a column with a flag for partial vs complete listening of a given track
            6. Add a column with a simplified 'origin' of the song, i.e. how it was found (search, suggestion, library,...)
            7. Add a column with a calculation of the listening duration in minutes
            8. Remove outliers of listening duration (99th percentile)
            9. Drop unused columns (args)

        '''

        columns_to_drop = [
        'Apple Id Number', 'Apple Music Subscription', 'Build Version', 'Client IP Address',
        'Content Specific Type', 'Device Identifier', 'Event Reason Hint Type', 'Activity date time',
        'End Position In Milliseconds', 'Event Received Timestamp', 'Media Type', 'Metrics Bucket Id', 
        'Metrics Client Id','Original Title', 'Source Type', 'Start Position In Milliseconds',
        'Store Country Name', 'Milliseconds Since Play', 'Event End Timestamp', 'Event Start Timestamp',
        'UTC Offset In Seconds','Play Duration Milliseconds', 'Media Duration In Milliseconds', 'Feature Name'
        ]
        # Rename columns for merges later
        parsed_df = play_activity_df.copy()
        parsed_df.rename(columns={'Content Name':'Title', 'Artist Name':'Artist'}, inplace=True)
        
        # Add time related columns
        parsed_df['Activity date time'] = pd.to_datetime(parsed_df['Event Start Timestamp'])
        parsed_df['Activity date time'].fillna(pd.to_datetime(parsed_df['Event End Timestamp']), inplace=True)
        if convert_to_local_time is True:
            parsed_df['Activity date time'] = Utility.convert_to_local_time(parsed_df['Activity date time'], parsed_df['UTC Offset In Seconds'])
        parsed_datetime_series = Utility.parse_date_time_column(parsed_df, 'Activity date time')
        Utility.add_time_related_columns(parsed_df, parsed_datetime_series, col_name_prefix='Play ')

        # We remove year outliers (Apple Music started in 2015, whatever is reported before is a mistake)
        parsed_df = parsed_df.drop(parsed_df[parsed_df['Play Year']< 2015].index)

        # Add partial listening column 
        play_duration = parsed_df['Play Duration Milliseconds']
        media_duration = parsed_df['Media Duration In Milliseconds']
        Parser.set_partial_listening(parsed_df, parsed_df['End Reason Type'], play_duration, media_duration)

        # Add track origin column
        parsed_df['Track origin'] = parsed_df['Feature Name'].apply(Parser.get_track_origin)

        # Add play duration column
        activity_start = pd.to_datetime(parsed_df['Event Start Timestamp'])
        activity_end = pd.to_datetime(parsed_df['Event End Timestamp'])
        played_completely = parsed_df['Played completely']
        Parser.compute_play_duration(parsed_df, activity_start, activity_end, played_completely, play_duration, media_duration)

        # we remove outliers from this play duration column, saying that if a value if above the 99th percentile,
        # we drop it, and replace it by the duration of the media
        percentile = parsed_df['Play duration in minutes'].quantile(0.99)
        Parser.remove_play_duration_outliers(parsed_df, parsed_df['Play duration in minutes'], media_duration, percentile)

        #we can then remove the columns we do not need anymore!
        if drop_columns:
            parsed_df = parsed_df.drop(columns_to_drop, axis=1, errors='ignore')

        return parsed_df

    @staticmethod
    def parse_library_tracks_infos_df(library_tracks_infos_df):
        '''
            This method is in charge of simplifying the library tracks df, by removing
            all the columns that are not used for analysis. 
        '''
        columns_to_drop = ['Content Type', 'Sort Name',
        'Sort Artist', 'Is Part of Compilation', 'Sort Album',
        'Album Artist', 'Track Number On Album',
        'Track Count On Album', 'Disc Number Of Album', 'Disc Count Of Album',
        'Date Added To iCloud Music Library', 'Last Modified Date',
        'Purchase Date', 'Is Purchased', 'Audio File Extension',
        'Is Checked', 'Audio Matched Track Identifier', 'Grouping', 'Comments', 
        'Beats Per Minute', 'Album Rating', 'Remember Playback Position', 
        'Album Like Rating', 'Album Rating Method', 'Work Name', 'Rating',
        'Movement Name', 'Movement Number', 'Movement Count',
        'Display Work Name', 'Copyright', 'Playlist Only Track',
        'Sort Album Artist', 'Sort Composer']
        parsed_df = library_tracks_infos_df.copy()
        parsed_df = parsed_df.drop(columns_to_drop, axis=1, errors='ignore')
        return parsed_df

    @staticmethod
    def parse_likes_dislikes_df(likes_dislikes_df):
        '''
            This method is in charge of parsing the column 'Item Description' of the likes dislikes df
            to create separate columns Title and Artist.

        '''
        parsed_df = likes_dislikes_df.copy()
        parsed_df['Title'] = parsed_df['Item Description'].str.split(' -').str.get(1).str.strip()
        parsed_df['Artist'] = parsed_df['Item Description'].str.split(' - ').str.get(0).str.strip()
        return parsed_df

    @staticmethod
    def set_partial_listening(play_activity_df, end_reason_type, play_duration, media_duration):
        '''
            This method is in charge of adding a new boolean column to the input play_activity_df
            to flag whether a song was skipped/partially listened to, or not.
        '''
        play_activity_df['Played completely'] = False
        play_activity_df.loc[end_reason_type == 'NATURAL_END_OF_TRACK', 'Played completely'] = True
        play_activity_df.loc[play_duration >= media_duration, 'Played completely'] = True


    @staticmethod
    def get_track_origin(x):
        '''
            Provided a serie x of strings, this method will return for each value a new string label.
            This method is to be used with the .apply pandas method on a dataframe serie. 
            The goal here is to simplify the origin of a song, i.e. how it was found to be listened to.
            We consider four types of simplified origin:
                - search
                - library
                - for you (Apple's suggestion)
                    - recently played
                    - personalized mix
                    - other
                - other (siri, radio, music_stack, now_playing, new, or unknown)
        '''
        if str(x) != 'nan':
            x_cat = str(x).split('/')[0].strip()
            if x_cat == 'search' or x_cat =='browse':
                return 'search'
            elif x_cat == 'library' or x_cat == 'my-music' or x_cat == 'playlists' or x_cat == 'playlist_detail':
                return 'library'
            elif x_cat == 'for_you':
                if len(str(x).split('/')) > 1:
                    x_subcat = str(x).split('/')[1].strip()
                    if x_subcat == 'recently_played':
                        return 'for you - recently played'
                    elif x_subcat == 'personalized_mix':
                        return 'for you - personalized mix'
                    else:
                        return 'for you - other'
                else:
                    return 'for you - other'
            else:
                return 'other'
        else:
            return 'other'

    @staticmethod
    def compute_play_duration(play_activity_df, start, end, played_completely, play_duration, media_duration):
        '''
            This method is in charge of computing an as accurate as possible play duration for each track.
            If the song was played partially and we have a value for the play duration in ms recorded, we use this value
            as a play duration (converted to minutes).
            Otherwise, if the start day and end day are the same, we can safely use the difference between the two timestamps
            as a play duration.
            For all the other rows, we use by default the media duration (converted to minutes).
        '''
        play_activity_df['Play duration in minutes'] = media_duration/60000
        play_activity_df.loc[start.dt.day == end.dt.day, 'Play duration in minutes'] = (end - start).dt.total_seconds()/60
        play_activity_df.loc[(played_completely == False)&(type(play_duration)!=float)&(play_duration>0), 'Play duration in minutes'] = play_duration/60000

    @staticmethod
    def remove_play_duration_outliers(play_activity_df, play_duration, media_duration, percentile):
        '''
            This method replaces any play duration outlier (beyong the percentile value) by the media duration.
        '''
        play_activity_df.loc[play_duration > percentile, 'Play duration in minutes'] = media_duration/60000




