import pandas as pd
import unittest

from apple_music_analyser.Utility import Utility


class TestUtils(unittest.TestCase):

    def test_compute_ratio_songs(self):
        serie = pd.Series([1, 1, 1, 1, 2, 2, 3, 3, 3, 3])
        result = Utility.compute_ratio_songs(serie).tolist()
        self.assertEqual(result, [40.0, 40.0, 20.0])

    def test_clean_col_with_list(self):
        serie = pd.Series([['Rock'], ['Pop'], ['Soundtrack', 'Pop']])
        result = serie.apply(Utility.clean_col_with_list).tolist()
        self.assertEqual(result, ['Rock', 'Pop', 'Soundtrack && Pop'])

    def test_concat_title_artist(self):
        title = 'Title'
        artist = 'Artist '
        result = Utility.concat_title_artist(title, artist)
        self.assertEqual(result, 'Title && Artist')

    def test_convert_to_local_time(self):
        serie = pd.date_range('2020-01-01', periods=3, freq='H')
        timezone_serie = pd.Series([3600, -7200, 0])
        result = Utility.convert_to_local_time(serie, timezone_serie).tolist()
        result = [str(x) for x in result]
        self.assertEqual(result, ['2020-01-01 01:00:00', '2019-12-31 23:00:00', '2020-01-01 02:00:00'])

    def test_extract_time_info_from_datetime(self):
        serie = pd.to_datetime(pd.Series('2020-01-01'))
        year, month, dom, dow, hod = Utility.extract_time_info_from_datetime(serie)
        self.assertEqual(year.values[0], 2020)
        self.assertEqual(month.values[0], 1)
        self.assertEqual(dom.values[0], 1)
        self.assertEqual(dow.values[0], 'Wednesday')
        self.assertEqual(hod.values[0], 0)

    def test_parse_date_time_column(self):
        '''
            We only test if it returns a dict, as the values come from another function tested
            in a separate test (cf. test_extract_time_info_from_datetime)
        '''
        df = pd.DataFrame(pd.Series('2020-01-01'), columns=['Timestamp'])
        result = Utility.parse_date_time_column(df, 'Timestamp')
        self.assertEqual(type(result), dict) 

    def test_add_time_related_columns(self):
        df = pd.DataFrame(pd.Series('2020-01-01'), columns=['Timestamp'])
        datetime_series = Utility.parse_date_time_column(df, 'Timestamp')
        Utility.add_time_related_columns(df, datetime_series, col_name_prefix='pref_', col_name_suffix='_suff')
        expected = {'Timestamp':['2020-01-01'], 'pref_date time_suff': ['2020-01-01'], 'pref_Year_suff': [2020], 'pref_Month_suff': [1], 'pref_DOM_suff': [1], 'pref_DOW_suff': ['Wednesday'], 'pref_HOD_suff': [0]}
        expected_output = pd.DataFrame.from_dict(expected)
        self.assertEqual(df.shape, expected_output.shape) 
        self.assertEqual(df.columns.tolist(), expected_output.columns.tolist()) 

    def test_get_df_from_archive_bad_archive(self):
        '''
          We test the case where the path is wrong
          This function relies on external package (ZipFile), well covered by tests.
        '''
        archive_path = None
        result = Utility.get_df_from_archive(archive_path)
        self.assertEqual(result, {})


    def test_get_df_from_archive_with_target(self):
        '''
          We test the case where the structure inside the archive is provided as an argument. 
          This function relies on external package (ZipFile), well covered by tests.
        '''        
        target_files = {
            'identifier_infos_path' : 'test_df/Apple Music Activity/Identifier Information.json.zip',
            'library_tracks_path' : 'test_df/Apple Music Activity/Apple Music Library Tracks.json.zip',
            'library_activity_path': 'test_df/Apple Music Activity/Apple Music Library Activity.json.zip',
            'likes_dislikes_path' : 'test_df/Apple Music Activity/Apple Music Likes and Dislikes.csv',
            'play_activity_path': 'test_df/Apple Music Activity/Apple Music Play Activity.csv'
        }
        archive_path = 'apple_music_analyser/tests/test_df.zip'
        result = Utility.get_df_from_archive(archive_path, target_files)
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 5)
        self.assertEqual(list(result.keys()), ['identifier_infos_df', 'library_tracks_df', 'library_activity_df', 'likes_dislikes_df', 'play_activity_df'])
        for key in result.keys():
            self.assertTrue(isinstance(result[key], pd.DataFrame))


if __name__ == '__main__':
    unittest.main()