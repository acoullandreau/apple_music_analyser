from difflib import SequenceMatcher
import pandas as pd
import pickle
from zipfile import ZipFile

class Utility():

    '''
        This class contains helper methods:
            get_df_from_archive(archive_path)
            get_df_from_file(file_path
            validate_input_df_files(input_df)
            parse_date_time_column(df, input_timestamp_col)
            extract_time_info_from_datetime(datetime_col)
            convert_to_local_time(datetime_serie, timezone_serie)
            add_time_related_columns(df, datetime_series, col_name_prefix='', col_name_suffix='')
            compute_similarity_score(a, b)
            concat_title_artist(title, artist)
            clean_col_with_list(x)
            compute_ratio_songs(serie)
            save_to_pickle(object_to_save, file_path)
            load_from_pickle(path_of_file)

    '''

    @staticmethod
    def get_df_from_archive(archive_path, target_files_dict=None):
        '''
            This method accepts a zip file as an input. The zip file must CONTAIN the following structure:
            Apple_Media_Services (folder)
                |_ Apple Music Activity (folder)
                    |_ Identifier Information.json.zip
                    |_ Apple Music Library Tracks.json.zip
                    |_ Apple Music Library Activity.json.zip
                    |_ Apple Music Likes and Dislikes.csv
                    |_ Apple Music Activity/Apple Music Play Activity.csv
            
            It is possible to pass as a parameter a different structure of the archive, with the path to
            each file WITHIN the archive, like so:
            target_files = {
                'identifier_infos_path' : 'Path_to_file_within_archive/Identifier Information.json.zip',
                'library_tracks_path' : 'Path_to_file_within_archive/Apple Music Library Tracks.json.zip',
                'library_activity_path': 'Path_to_file_within_archive/Apple Music Library Activity.json.zip',
                'likes_dislikes_path' : 'Path_to_file_within_archive/Apple Music Likes and Dislikes.csv',
                'play_activity_path': 'Path_to_file_within_archive/Apple Music Play Activity.csv'
            }

            The expected format of each file is as indicated above in the target_files dict (csv, json or json.zip).

            An error message is printed if the zip file provided does not have the right format.
        '''

        if target_files_dict == None:
            target_files = {
                'identifier_infos_path' : 'Apple_Media_Services/Apple Music Activity/Identifier Information.json.zip',
                'library_tracks_path' : 'Apple_Media_Services/Apple Music Activity/Apple Music Library Tracks.json.zip',
                'library_activity_path': 'Apple_Media_Services/Apple Music Activity/Apple Music Library Activity.json.zip',
                'likes_dislikes_path' : 'Apple_Media_Services/Apple Music Activity/Apple Music Likes and Dislikes.csv',
                'play_activity_path': 'Apple_Media_Services/Apple Music Activity/Apple Music Play Activity.csv'
            }
        else:
            target_files = target_files_dict

        if archive_path:
            archive_files = ZipFile(archive_path)
            
            dataframes = {}

            if archive_files.testzip() == None:
                identifier_infos_df = Utility.get_df_from_file(archive_files.open(target_files['identifier_infos_path']))
                dataframes['identifier_infos_df']=identifier_infos_df

                library_tracks_df = Utility.get_df_from_file(archive_files.open(target_files['library_tracks_path']))
                dataframes['library_tracks_df']=library_tracks_df

                library_activity_df = Utility.get_df_from_file(archive_files.open(target_files['library_activity_path']))
                dataframes['library_activity_df']=library_activity_df

                likes_dislikes_df = Utility.get_df_from_file(archive_files.open(target_files['likes_dislikes_path']))
                dataframes['likes_dislikes_df']=likes_dislikes_df

                play_activity_df = Utility.get_df_from_file(archive_files.open(target_files['play_activity_path']))
                dataframes['play_activity_df']=play_activity_df

                archive_files.close()

            else:
                print('WARNING: Please refer to the documentation to see what files are expected in the zip provided. Returned object is empty.')

            return dataframes
        else:
            print('WARNING: Please refer to the documentation to see what files are expected in the zip provided. Returned object is empty.')
            return {}

    @staticmethod
    def get_df_from_file(file_path):
        '''
            Based on the extension of file_path, extracts a dataframe from a file.
        '''

        df = None
        if file_path.name.endswith('.json.zip'):
            df = pd.read_json(file_path, compression='zip')
        elif file_path.name.endswith('.json'):
            df = pd.read_json(file_path)
        elif file_path.name.endswith('.csv'):
            df = pd.read_csv(file_path, error_bad_lines=False, warn_bad_lines=False)
        else:
            print('Please provide a file with extension .csv, .json or .json.zip')
        
        return df


    @staticmethod
    def validate_input_df_files(input_df):
        '''
            This method expects as an input a dictionary of dataframes, with the following structure:
            {  "identifier_infos_df" : identifier_infos_df,
            "library_tracks_df" : library_tracks_df,
            "library_activity_df" : library_activity_df,
            "likes_dislikes_df" : likes_dislikes_df,
            "play_activity_df" : play_activity_df    }
            
            This function validates that the input has the correct format and that it contains dataframes.
            It returns a boolean.

        '''
        expected_files = ['identifier_infos_df','library_tracks_df', 'library_activity_df', 'likes_dislikes_df', 'play_activity_df']
        expected_format = pd.DataFrame
        for key in input_df.keys():
            if key not in expected_files:
                print('The input_df contains an unknown key: ', key)
                return False
            if not isinstance(input_df[key], expected_format):
                print('The value of '+key+' is not a pandas dataframe object.')
                return False
        return True


    @staticmethod
    def parse_date_time_column(df, input_timestamp_col):
        '''
            This method returns a dictionary of series, parsed from a timestamp serie.
            input_timestamp_col is the name of the column of df containing the timestamp.
            
            This method calls extract_time_info_from_datetime to extract year, month,
            day of the month, day of the week and hour of the day from the datetime column.

        '''
        datetime_col = pd.to_datetime(df[input_timestamp_col])
        year, month, dom, dow, hod = Utility.extract_time_info_from_datetime(datetime_col)

        datetime_series = {
            'datetime':datetime_col,
            'year':year,
            'month':month,
            'dom':dom,
            'dow':dow,
            'hod':hod
        }

        return datetime_series


    @staticmethod
    def extract_time_info_from_datetime(datetime_col):
        '''
            This method extracts year, month, day of the month, day of the week and
            hour of the day from a datetime serie.
        '''
        year=datetime_col.dt.year
        month=datetime_col.dt.month
        dom=datetime_col.dt.day
        dow=datetime_col.dt.day_name()
        hod=datetime_col.dt.hour

        return year, month, dom, dow, hod

    @staticmethod
    def convert_to_local_time(datetime_serie, timezone_serie):
        '''
            This method returns a datetime serie converted to a different timezone.
            It accepts as arguments datetime_serie and timezone_serie.
            Both must be of the same size. 
            timezone_serie must contain an offset from GMT in seconds.
        '''
        timedelta = pd.to_timedelta(timezone_serie, unit='s')
        return datetime_serie + timedelta

    @staticmethod
    def add_time_related_columns(df, datetime_series, col_name_prefix='', col_name_suffix=''):
        '''
            This method simply adds columns to a df containing time info with a prefix and/or a suffix.

            Args:
                df - the dataframe to add columns to
                datetime_series - a dictionary of series of the format
                    {
                        'datetime':datetime_serie,
                        'year':year_serie,
                        'month':month_serie,
                        'dom':dom_serie,
                        'dow':dow_serie,
                        'hod':hod_serie
                    }
                col_name_prefix - OPTIONAL, prefix to add to the column name
                col_name_suffix - OPTIONAL, suffix to add to the column name
        '''
        df[col_name_prefix+'date time'+col_name_suffix] = datetime_series['datetime']
        df[col_name_prefix+'Year'+col_name_suffix] = datetime_series['year']
        df[col_name_prefix+'Month'+col_name_suffix] = datetime_series['month']
        df[col_name_prefix+'DOM'+col_name_suffix] = datetime_series['dom']
        df[col_name_prefix+'DOW'+col_name_suffix] = datetime_series['dow']
        df[col_name_prefix+'HOD'+col_name_suffix] = datetime_series['hod']


    
    @staticmethod
    def compute_similarity_score(a, b):
        '''
            This method computes a score of similarity between two strings a and b.
        '''
        return SequenceMatcher(None, a, b).ratio()

    @staticmethod
    def concat_title_artist(title, artist):
        '''
            Returns a concatenated string without trailing spaces of the title and
            artist names passed as args
        '''
        return title.strip()+' && '+artist.strip()

    @staticmethod
    def clean_col_with_list(x):
        '''
            This function is used to break down the values of a serie containing lists.
            The idea is to return the values as a string ('', the unique value of a list, or a join of
            values separated by '&&').
        '''
        if type(x) != float:
            if x == None or len(x) == 0:
                return 'Unknown'
            elif len(x) == 1:
                return x[0]
            else:
                return ' && '.join(x)
        else:
            return 'Unknown'

    @staticmethod
    def compute_ratio_songs(serie):
        '''
            Returns the distribution of each value in a pandas serie.
        '''
        return (serie.value_counts()/serie.count())*100

    @staticmethod
    def save_to_pickle(object_to_save, file_path):
        '''
            Saves the object_to_save as a pickle file at file_path.
        '''
        with open(file_path, 'wb') as output:
          pickle.dump(object_to_save, output, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_from_pickle(path_of_file):
        '''
            Loads a pickle object from path_of_file.
        '''
        with open(path_of_file, 'rb') as input:
            return pickle.load(input)




















