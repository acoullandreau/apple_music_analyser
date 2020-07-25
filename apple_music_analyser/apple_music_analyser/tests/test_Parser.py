import pandas as pd
import unittest

from apple_music_analyser.Utility import Utility
from apple_music_analyser.Parser import Parser



class TestParser(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        target_files = {
            'identifier_infos_path' : 'test_df/Apple Music Activity/Identifier Information.json.zip',
            'library_tracks_path' : 'test_df/Apple Music Activity/Apple Music Library Tracks.json.zip',
            'library_activity_path': 'test_df/Apple Music Activity/Apple Music Library Activity.json.zip',
            'likes_dislikes_path' : 'test_df/Apple Music Activity/Apple Music Likes and Dislikes.csv',
            'play_activity_path': 'test_df/Apple Music Activity/Apple Music Play Activity.csv'
        }
        self.input_df = Utility.get_df_from_archive('apple_music_analyser/tests/test_df.zip', target_files)

    def test_parse_input_df(self):
        result = Parser.parse_input_df(self.input_df)
        # we expect a dictionary of dataframes
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 5)
        self.assertEqual(list(result.keys()), ['likes_dislikes_df', 'play_activity_df', 'identifier_infos_df', 'library_tracks_df', 'library_activity_df'])
        for i in range(len(list(result.values()))):
            self.assertTrue(isinstance(list(result.values())[i], pd.DataFrame))

    def test_parse_source_dataframes_bad_input(self):
        parser = Parser(self.input_df)
        parser.source_dataframes = {}
        self.assertRaises(Exception, parser.parse_source_dataframes)

    def test_parse_library_activity_df(self):
        library_activity_df = self.input_df['library_activity_df']
        shape_input_df = library_activity_df.shape
        result = Parser.parse_library_activity_df(library_activity_df)
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(result.shape[0], shape_input_df[0])
        self.assertEqual(result.shape[1], shape_input_df[1] + 8)
        self.assertIn('Transaction date time', result.columns)
        self.assertIn('Transaction Year', result.columns)
        self.assertIn('Transaction Month', result.columns)
        self.assertIn('Transaction DOM', result.columns)
        self.assertIn('Transaction DOW', result.columns)
        self.assertIn('Transaction HOD', result.columns)
        self.assertIn('Transaction HOD', result.columns)
        self.assertIn('Transaction Agent', result.columns)
        self.assertIn('Transaction Agent Model', result.columns)

    def test_parse_library_tracks_infos_df(self):
        library_tracks_df = self.input_df['library_tracks_df']
        shape_input_df = library_tracks_df.shape
        result = Parser.parse_library_tracks_infos_df(library_tracks_df)
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(result.shape[0], shape_input_df[0])
        self.assertEqual(result.shape[1], shape_input_df[1] - 34)

    def test_parse_likes_dislikes_df(self):
        likes_dislikes_df = self.input_df['likes_dislikes_df']
        shape_input_df = likes_dislikes_df.shape
        result = Parser.parse_likes_dislikes_df(likes_dislikes_df)
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(result.shape[0], shape_input_df[0])
        self.assertEqual(result.shape[1], shape_input_df[1] + 2)
        self.assertIn('Title', result.columns)
        self.assertIn('Artist', result.columns)

    def test_set_partial_listening(self):
        df = pd.DataFrame.from_dict({
            'End Reason Type':['NATURAL_END_OF_TRACK', 'SCRUB_END', 'FAILED_TO_LOAD'],
            'Play Duration Milliseconds':[111, 22222, 1234],
            'Media Duration In Milliseconds':[444, 3, 12345]
            })
        shape_input_df = df.shape
        Parser.set_partial_listening(df, df['End Reason Type'], df['Play Duration Milliseconds'], df['Media Duration In Milliseconds'])

        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertEqual(df.shape[0], shape_input_df[0])
        self.assertEqual(df.shape[1], shape_input_df[1] + 1)
        self.assertIn('Played completely', df.columns)
        self.assertEqual(df.iloc[0, 3], True)
        self.assertEqual(df.iloc[1, 3], True)
        self.assertEqual(df.iloc[2, 3], False)

    def test_get_track_origin(self):
        df = pd.DataFrame.from_dict({
            'Feature Name':['library / playlist_detail', 'my-music', 'for_you / personalized_mix / playlist_detail', 'now_playing', 'for_you / playlist_detail / album_detail',
            'browse', 'search:none / profile-all', 'for_you / recently_played / playlist_detail', 'Siri-actions-local', 'library / songs']
            })
        shape_input_df = df.shape
        df['Track origin'] = df['Feature Name'].apply(Parser.get_track_origin)
        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertEqual(df.shape[0], shape_input_df[0])
        self.assertEqual(df.shape[1], shape_input_df[1] + 1)
        self.assertIn('Track origin', df.columns)
        self.assertEqual(df['Track origin'].tolist(), ['library', 'library', 'for you - personalized mix', 'other', 'for you - other', 'search', 'other', 'for you - recently played', 'other', 'library'])

    def test_compute_play_duration(self):
        df = pd.DataFrame.from_dict({
            'Event Start Timestamp':['2016-12-02T07:22:34.766Z', '', '2016-10-27T09:45:31.817Z'],
            'Event End Timestamp':['2016-12-02T07:25:34.766Z', '2019-06-19T15:51:09.477Z', '2016-10-27T09:47:36.482Z'],
            'Play Duration Milliseconds':[123, 5342, 60000],
            'Media Duration In Milliseconds':[123, 120000, 120000],
            'Played completely':[True, True, False]
            })

        shape_input_df = df.shape
        activity_start = pd.to_datetime(df['Event Start Timestamp'])
        activity_end = pd.to_datetime(df['Event End Timestamp'])
        played_completely = df['Played completely']
        play_duration = df['Play Duration Milliseconds']
        media_duration = df['Media Duration In Milliseconds']
        Parser.compute_play_duration(df, activity_start, activity_end, played_completely, play_duration, media_duration)

        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertEqual(df.shape[0], shape_input_df[0])
        self.assertEqual(df.shape[1], shape_input_df[1] + 1)
        self.assertEqual(int(df.iloc[0, 5]), 3)
        self.assertEqual(df.iloc[1, 5], 2)
        self.assertEqual(df.iloc[2, 5], 1)

    def test_remove_play_duration_outliers(self):
        df = pd.DataFrame.from_dict({
            'Play duration in minutes':[1, 4, 6, 999],
            'Media Duration In Milliseconds':[123, 345, 678, 120000],
            })

        shape_input_df = df.shape
        duration_minutes = df['Play duration in minutes']
        media_duration = df['Media Duration In Milliseconds']
        percentile = df['Play duration in minutes'].quantile(0.99)
        Parser.remove_play_duration_outliers(df, duration_minutes, media_duration, percentile)
        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertEqual(df.shape[0], shape_input_df[0])
        self.assertEqual(df.shape[1], shape_input_df[1])
        self.assertEqual(int(df.iloc[0, 0]), 1)
        self.assertEqual(df.iloc[1, 0], 4)
        self.assertEqual(df.iloc[2, 0], 6)
        self.assertEqual(df.iloc[3, 0], 2)

    def test_parse_play_activity_df(self):
        play_activity_df = self.input_df['play_activity_df']
        shape_input_df = play_activity_df.shape
        result = Parser.parse_play_activity_df(play_activity_df)
        self.assertTrue(isinstance(result, pd.DataFrame))
        #we expect 1 row with date before 2015 to be dropped
        self.assertEqual(result.shape[0], shape_input_df[0] -1)
        # 24 columns are dropped, and 10 added (those tested below)
        self.assertEqual(result.shape[1], shape_input_df[1] -14)
        self.assertIn('Play date time', result.columns)
        self.assertIn('Play Year', result.columns)
        self.assertIn('Play Month', result.columns)
        self.assertIn('Play DOM', result.columns)
        self.assertIn('Play DOW', result.columns)
        self.assertIn('Play HOD', result.columns)
        self.assertIn('Play HOD', result.columns)
        self.assertIn('Played completely', result.columns)
        self.assertIn('Track origin', result.columns)
        self.assertIn('Play duration in minutes', result.columns)

    def test_init_Parser(self):
        target_files = {
            'identifier_infos_path' : 'test_df/Apple Music Activity/Identifier Information.json.zip',
            'library_tracks_path' : 'test_df/Apple Music Activity/Apple Music Library Tracks.json.zip',
            'library_activity_path': 'test_df/Apple Music Activity/Apple Music Library Activity.json.zip',
            'likes_dislikes_path' : 'test_df/Apple Music Activity/Apple Music Likes and Dislikes.csv',
            'play_activity_path': 'test_df/Apple Music Activity/Apple Music Play Activity.csv'
        }
        input_df = Utility.get_df_from_archive('apple_music_analyser/tests/test_df.zip', target_files)
        shape_input_likes_dislikes_df = input_df['likes_dislikes_df'].shape
        shape_input_play_activity_df = input_df['play_activity_df'].shape
        shape_input_identifier_infos_df = input_df['identifier_infos_df'].shape
        shape_input_library_tracks_df = input_df['library_tracks_df'].shape
        shape_input_library_activity_df = input_df['library_activity_df'].shape
        result = Parser(input_df)
        self.assertTrue(isinstance(result.likes_dislikes_df, pd.DataFrame))
        self.assertEqual(result.likes_dislikes_df.shape, (shape_input_likes_dislikes_df[0], shape_input_likes_dislikes_df[1] + 2))
        self.assertTrue(isinstance(result.play_activity_df, pd.DataFrame))
        self.assertEqual(result.play_activity_df.shape, (shape_input_play_activity_df[0] - 1, shape_input_play_activity_df[1] - 14))
        self.assertTrue(isinstance(result.identifier_infos_df, pd.DataFrame))
        self.assertEqual(result.identifier_infos_df.shape, (shape_input_identifier_infos_df[0], shape_input_identifier_infos_df[1]))
        self.assertTrue(isinstance(result.library_tracks_df, pd.DataFrame))
        self.assertEqual(result.library_tracks_df.shape, (shape_input_library_tracks_df[0], shape_input_library_tracks_df[1] - 34))
        self.assertTrue(isinstance(result.library_activity_df, pd.DataFrame))
        self.assertEqual(result.library_activity_df.shape, (shape_input_library_activity_df[0], shape_input_library_activity_df[1] + 8))

    @classmethod
    def tearDownClass(self):
        self.input_df = None


if __name__ == '__main__':
    unittest.main()