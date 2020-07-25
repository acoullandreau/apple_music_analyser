import pandas as pd
import unittest

from apple_music_analyser.Utility import Utility
from apple_music_analyser.Parser import Parser
from apple_music_analyser.Process import ProcessTracks, TrackSummaryObject
from apple_music_analyser.VisualizationDataframe import VisualizationDataframe


class TestVisualizationDataframe(unittest.TestCase):

    def setUp(self):
        target_files = {
            'identifier_infos_path' : 'test_df/Apple Music Activity/Identifier Information.json.zip',
            'library_tracks_path' : 'test_df/Apple Music Activity/Apple Music Library Tracks.json.zip',
            'library_activity_path': 'test_df/Apple Music Activity/Apple Music Library Activity.json.zip',
            'likes_dislikes_path' : 'test_df/Apple Music Activity/Apple Music Likes and Dislikes.csv',
            'play_activity_path': 'test_df/Apple Music Activity/Apple Music Play Activity.csv'
        }
        self.input_df = Utility.get_df_from_archive('apple_music_analyser/tests/test_df.zip', target_files)
        self.df_visualization = VisualizationDataframe(self.input_df)

    def test_init_VisualizationDataframe(self):
        result = self.df_visualization
        self.assertTrue(isinstance(result.parser, Parser))
        self.assertTrue(isinstance(result.process_tracks, ProcessTracks))
        self.assertTrue(isinstance(result.track_summary_objects, TrackSummaryObject))
        self.assertTrue(isinstance(result.likes_dislikes_df, pd.DataFrame))
        self.assertTrue(isinstance(result.play_activity_df, pd.DataFrame))
        self.assertTrue(isinstance(result.identifier_infos_df, pd.DataFrame))
        self.assertTrue(isinstance(result.library_tracks_df, pd.DataFrame))
        self.assertTrue(isinstance(result.library_activity_df, pd.DataFrame))
        self.assertTrue(isinstance(result.df_visualization, pd.DataFrame))
        self.assertTrue(isinstance(result.source_dataframes, dict))
        # df_vizualisation must have as many lines as the play_activity_df we defined -> 165 rows
        self.assertEqual(result.df_visualization.shape[0], self.df_visualization.play_activity_df.shape[0])
        # df_vizualisation must have 3 columns more than play_activity_df -> 20 columns
        self.assertEqual(result.df_visualization.shape[1], self.df_visualization.play_activity_df.shape[1] + 3)
        self.assertIn('Genres', result.df_visualization.columns)
        self.assertNotIn('Genre', result.df_visualization.columns)
        self.assertIn('Rating', result.df_visualization.columns)
        self.assertIn('Track_Instance', result.df_visualization.columns)

    def test_get_df_viz(self):
        result = self.df_visualization.get_df_viz()
        # we test exactly like in the previous test
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(result.shape[0], 165)
        self.assertEqual(result.shape[1], 20)
        self.assertIn('Genres', result.columns)
        self.assertNotIn('Genre', result.columns)
        self.assertIn('Rating', result.columns)
        self.assertIn('Track_Instance', result.columns)

    def test_get_source_dataframes(self):
        result = self.df_visualization.get_source_dataframes()
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 5)
        self.assertEqual(list(result.keys()), ['likes_dislikes_df', 'play_activity_df', 'identifier_infos_df', 'library_tracks_df', 'library_activity_df'])
        for i in range(len(list(result.values()))):
            self.assertTrue(isinstance(list(result.values())[i], pd.DataFrame))

    def test_get_play_activity_df(self):
        shape_before_parse = self.input_df['play_activity_df'].shape
        result = self.df_visualization.get_play_activity_df()
        self.assertTrue(isinstance(result, pd.DataFrame))
        #we expect 1 row with date before 2015 to be dropped
        self.assertEqual(result.shape[0], shape_before_parse[0] -1)
        # when parsing 24 columns are dropped from the input and 10 added
        self.assertEqual(result.shape[1], shape_before_parse[1] - 14)

    def test_get_identifier_info_df(self):
        shape_before_parse = self.input_df['identifier_infos_df'].shape
        result = self.df_visualization.get_identifier_info_df()
        self.assertTrue(isinstance(result, pd.DataFrame))
        # no parsing occured, so no changes in the shape of the df
        self.assertEqual(result.shape[0], shape_before_parse[0])
        self.assertEqual(result.shape[1], shape_before_parse[1])

    def test_get_library_tracks_df(self):
        shape_before_parse = self.input_df['library_tracks_df'].shape
        result = self.df_visualization.get_library_tracks_df()
        self.assertTrue(isinstance(result, pd.DataFrame))
        # no row was removed
        self.assertEqual(result.shape[0], shape_before_parse[0])
        # after parsing, 34 columns are removed
        self.assertEqual(result.shape[1], shape_before_parse[1] - 34)

    def test_get_library_activity_df(self):
        shape_before_parse = self.input_df['library_activity_df'].shape
        result = self.df_visualization.get_library_activity_df()
        self.assertTrue(isinstance(result, pd.DataFrame))
        # no row was removed
        self.assertEqual(result.shape[0], shape_before_parse[0])
        # after parsing, 8 columns are added
        self.assertEqual(result.shape[1], shape_before_parse[1] + 8)
    
    def test_get_likes_dislikes_df(self):
        shape_before_parse = self.input_df['likes_dislikes_df'].shape
        result = self.df_visualization.get_likes_dislikes_df()
        self.assertTrue(isinstance(result, pd.DataFrame))
        # no row was removed
        self.assertEqual(result.shape[0], shape_before_parse[0])
        # after parsing, 2 columns are added
        self.assertEqual(result.shape[1], shape_before_parse[1]  + 2 )

    def test_get_df_from_source_no_source(self):
        self.df_visualization.source_dataframes = {}
        self.assertRaises(Exception, self.df_visualization.get_df_from_source)

    def test_process_tracks_in_df_no_source(self):
        self.df_visualization.source_dataframes = {}
        self.assertRaises(Exception, self.df_visualization.process_tracks_in_df)

    def test_build_df_visualisation_play_activity(self):
        result = self.df_visualization.build_df_visualisation()
        self.assertEqual(result.shape[0], self.df_visualization.play_activity_df.shape[0])
        self.assertEqual(result.shape[1], self.df_visualization.play_activity_df.shape[1] + 3)
        self.assertIn('Genres', result.columns)
        self.assertNotIn('Genre', result.columns)
        self.assertIn('Rating', result.columns)
        self.assertIn('Track_Instance', result.columns)
        # all spaces in column names have been replaces by '_'
        for column_name in result.columns:
            self.assertNotIn(' ', column_name)

if __name__ == '__main__':
    unittest.main()