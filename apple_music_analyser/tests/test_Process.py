import pandas as pd
import unittest

from apple_music_analyser.Utility import Utility
from apple_music_analyser.Track import Track
from apple_music_analyser.Query import Query, QueryFactory
from apple_music_analyser.Parser import Parser
from apple_music_analyser.Process import ProcessTracks, TrackSummaryObject

class TestProcess(unittest.TestCase):

    @classmethod
    def setUp(self):
        target_files = {
            'identifier_infos_path' : 'test_df/Apple Music Activity/Identifier Information.json.zip',
            'library_tracks_path' : 'test_df/Apple Music Activity/Apple Music Library Tracks.json.zip',
            'library_activity_path': 'test_df/Apple Music Activity/Apple Music Library Activity.json.zip',
            'likes_dislikes_path' : 'test_df/Apple Music Activity/Apple Music Likes and Dislikes.csv',
            'play_activity_path': 'test_df/Apple Music Activity/Apple Music Play Activity.csv'
        }
        self.input_df = Utility.get_df_from_archive('apple_music_analyser/tests/test_df.zip', target_files)
        self.parser = Parser(self.input_df)
        self.likes_dislikes_df = self.parser.likes_dislikes_df
        self.play_activity_df = self.parser.play_activity_df
        self.identifier_infos_df = self.parser.identifier_infos_df
        self.library_tracks_df = self.parser.library_tracks_df
        self.library_activity_df = self.parser.library_activity_df
        self.process = ProcessTracks()
        self.track_instance = Track(self.process.increment)

    def test_init_Process(self):
        self.assertTrue(isinstance(self.process, ProcessTracks))
        self.assertEqual(self.process.increment, 0)
        self.assertEqual(self.process.track_instance_dict, {})
        self.assertEqual(self.process.artist_tracks_titles, {})
        self.assertEqual(self.process.genres_list, [])
        self.assertEqual(self.process.items_not_matched, {'library_tracks':[], 'identifier_info':[],
                             'play_activity':[], 'likes_dislikes':[]})

    def test_get_track_instance_dict(self):
        self.process.track_instance_dict = {'key':'value', 'key_2':'value_2'}
        result = self.process.get_track_instance_dict()
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 2)

    def test_get_artist_tracks_titles(self):
        self.process.artist_tracks_titles = {'key':'value', 'key_2':'value_2'}
        result = self.process.get_artist_tracks_titles()
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 2)

    def test_get_increment(self):
        self.process.increment = 1
        result = self.process.get_increment()
        self.assertTrue(isinstance(result, int))
        self.assertEqual(result, 1)

    def test_get_genres_list(self):
        self.process.genres_list = ['Genre', 'Other_genre']
        result = self.process.get_genres_list()
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 2)

    def test_get_items_not_matched(self):
        self.process.items_not_matched = {'library_tracks':['item'], 'identifier_info':['item', 'item_2'],
                             'play_activity':[], 'likes_dislikes':[]}
        result = self.process.get_items_not_matched()
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 4)
        self.assertEqual(list(result.keys()), ['library_tracks', 'identifier_info', 'play_activity', 'likes_dislikes'])
        self.assertEqual(len(result['library_tracks']), 1)
        self.assertEqual(len(result['identifier_info']), 2)


    def test_compare_titles_for_artist(self):
        self.process.artist_tracks_titles = { 'Artist_1': ['Title_1', 'Other_Title'], 'Artist_2': ['Title_1', 'Other_Title'] }
        self.process.track_instance_dict = { 'Title_1 && Artist_1': self.track_instance }
        result_no_match = self.process.compare_titles_for_artist('Artist_1', 'Title_Very_Different')
        self.assertEqual(result_no_match, 'No match')
        result_match = self.process.compare_titles_for_artist('Artist_1', 'Title_2')
        self.assertTrue(isinstance(result_match, Track))


    def test_update_track_instance_play(self):
        index_play = 50
        row_play = self.play_activity_df.iloc[50]
        self.process.update_track_instance('play_activity_df', self.track_instance, index_play, row_play)
        self.assertEqual(self.process.genres_list, ['Soundtrack'])
        self.assertEqual(self.track_instance.genre, ['Soundtrack'])
        self.assertEqual(self.track_instance.appearances, [{'source': 'play_activity', 'df_index': 50}])

    def test_update_track_instance_lib(self):
        index_lib = 31
        row_lib = self.library_tracks_df.iloc[31]
        self.process.update_track_instance('library_tracks_df', self.track_instance, index_lib, row_lib)
        self.assertEqual(self.process.genres_list, ['French Pop'])
        self.assertEqual(self.track_instance.genre, ['French Pop'])
        self.assertEqual(self.track_instance.appearances, [{'source': 'library_tracks', 'df_index': 31}])

    def test_update_track_instance_other(self):
        index_other = 10
        row_other = self.identifier_infos_df.iloc[10]
        self.process.update_track_instance('identifier_infos_df', self.track_instance, index_other, row_other)
        self.assertEqual(self.process.genres_list, [])
        self.assertEqual(self.track_instance.genre, [])
        self.assertEqual(self.track_instance.appearances, [])

    def test_process_library_tracks_df(self):
        self.process.process_library_tracks_df(self.library_tracks_df)
        self.assertEqual(len(self.process.track_instance_dict), 36)
        self.assertIn('Clandestino && Manu Chao', self.process.track_instance_dict.keys())
        self.assertEqual(len(self.process.artist_tracks_titles), 29)
        self.assertEqual(len(self.process.artist_tracks_titles['Céline Dion']), 3)
        self.assertEqual(len(self.process.genres_list), 16)
        self.assertEqual(self.process.items_not_matched['library_tracks'], [])

    def test_process_identifier_df(self):
        # we expect modifications of the process objects only if they are not empty
        self.process.process_identifier_df(self.identifier_infos_df)
        self.assertEqual(self.process.track_instance_dict, {})
        self.assertEqual(self.process.genres_list, [])
        self.assertEqual(self.process.artist_tracks_titles, {})
        self.assertEqual(self.process.increment, 0)
        self.assertEqual(len(self.process.items_not_matched['identifier_info']), self.identifier_infos_df.shape[0])

    def test_process_play_df(self):
        self.process.process_play_df(self.play_activity_df)
        self.assertEqual(self.process.increment, 110)
        # because the Genre nan is associated to a row without title it is dropped in the process
        self.assertEqual(len(self.process.genres_list), 25)
        self.assertEqual(len(self.process.track_instance_dict), 110)
        self.assertEqual(len(self.process.artist_tracks_titles), 89)
        self.assertEqual(self.process.track_instance_dict['The Unforgiven && Metallica'].titles, ['The Unforgiven'])
        self.assertEqual(self.process.track_instance_dict['The Unforgiven && Metallica'].artist, 'Metallica')
        self.assertEqual(self.process.track_instance_dict['The Unforgiven && Metallica'].appearances, [{'source': 'play_activity', 'df_index': 101}, {'source': 'play_activity', 'df_index': 153}, {'source': 'play_activity', 'df_index': 154}])
        self.assertEqual(self.process.track_instance_dict['The Unforgiven && Metallica'].genre, ['Heavy Metal'])
        self.assertEqual(self.process.track_instance_dict['The Unforgiven && Metallica'].identifier, 70)
        self.assertEqual(self.process.track_instance_dict['The Unforgiven && Metallica'].is_in_lib, True)
        self.assertIn('The Unforgiven', self.process.artist_tracks_titles['Metallica'])
        # rows with NaN as the title are added to items_not_matched
        self.assertEqual(self.process.items_not_matched['play_activity'], [0, 1, 2, 3, 96, 116, 165])
        # these info come from other df, so they should remain empty
        self.assertEqual(self.process.track_instance_dict['The Unforgiven && Metallica'].rating, [])
        self.assertEqual(self.process.track_instance_dict['The Unforgiven && Metallica'].apple_music_id, [])


    def test_process_likes_dislikes_df(self):
        # we expect modifications of the process objects only if they are not empty
        self.process.process_likes_dislikes_df(self.likes_dislikes_df)
        self.process.process_identifier_df(self.identifier_infos_df)
        self.assertEqual(self.process.track_instance_dict, {})
        self.assertEqual(self.process.genres_list, [])
        self.assertEqual(self.process.artist_tracks_titles, {})
        self.assertEqual(self.process.increment, 0)
        self.assertEqual(len(self.process.items_not_matched['likes_dislikes']), self.likes_dislikes_df.shape[0])


    def test_process_all_df(self):
        self.process.process_library_tracks_df(self.library_tracks_df)
        self.process.process_identifier_df(self.identifier_infos_df)
        self.process.process_play_df(self.play_activity_df)
        self.process.process_likes_dislikes_df(self.likes_dislikes_df)
        # in the test df, there are 3 tracks with similar names
        # and 15 common tracks (among them one is already counted in the 3 similarly named tracks)
        # so we want to validate that the number of track instances is :
        # 110 (play_activity tracks) + 35 (library tracks) - 3 - 14 = 128
        # and that increment is one unit above, so 129
        self.assertEqual(self.process.increment, 129)
        # and that we have 132 entries in track_instance_dict (110 (play_activity tracks) + 35 (library tracks) - 14 (common) + 3 (similar names))
        self.assertEqual(len(self.process.track_instance_dict), 133)
        # there are 10 songs labeled with the same genre, so output genres_list should have 31 values
        self.assertEqual(len(self.process.genres_list), 31)
        #the items not matched of library_tracks_df and play_activity_df should be the same than in the individual test functions defined above
        self.assertEqual(self.process.items_not_matched['play_activity'], [0, 1, 2, 3, 96, 116, 165])
        self.assertEqual(self.process.items_not_matched['library_tracks'], [])
        # but for the other df the values are different!
        # for likes and dislikes, we expect 7 rows to be unmatched
        self.assertEqual(self.process.items_not_matched['likes_dislikes'], [3, 4, 5, 10, 19, 20, 21])
        # for increment actually many more! Total of 51 unmatched, because we use the identifier as a key to match, and not the title
        self.assertEqual(len(self.process.items_not_matched['identifier_info']), 51)
        # we expect to find 19 common artists, so the length of artist_tracks_titles should be 29 + 89 - 19 = 99 
        self.assertEqual(len(self.process.artist_tracks_titles), 99)
        #and the artist with the more songs should be Michele McLaughlin with 5 tracks
        max_artist = max(self.process.artist_tracks_titles, key=lambda x:len(self.process.artist_tracks_titles[x]))
        max_value = len(self.process.artist_tracks_titles[max_artist])
        self.assertEqual(max_artist, 'Michele McLaughlin')
        self.assertEqual(max_value, 5)

        #now we focus on one song that appears in multiple df
        self.assertEqual(self.process.track_instance_dict['Nicolas Le Floch - Générique && Stéphane Moucha'].titles, ['Nicolas Le Floch - Générique', 'Nicolas Le Floch'])
        self.assertEqual(self.process.track_instance_dict['Nicolas Le Floch - Générique && Stéphane Moucha'].artist, 'Stéphane Moucha')
        self.assertEqual(self.process.track_instance_dict['Nicolas Le Floch - Générique && Stéphane Moucha'].appearances, [{'source': 'library_tracks', 'df_index': 11}, {'source': 'identifier_info', 'df_index': 14}, {'source': 'play_activity', 'df_index': 72}, {'source': 'likes_dislikes', 'df_index': 28}])
        self.assertEqual(self.process.track_instance_dict['Nicolas Le Floch - Générique && Stéphane Moucha'].identifier, 9)
        # we verify that the track is indeed in the library and properly flagged
        self.assertIn('Nicolas Le Floch - Générique', self.library_tracks_df['Title'].unique())
        self.assertEqual(self.process.track_instance_dict['Nicolas Le Floch - Générique && Stéphane Moucha'].is_in_lib, True)
        #we verify that the genre assigned to the track matches in all df available
        self.assertEqual(self.process.track_instance_dict['Nicolas Le Floch - Générique && Stéphane Moucha'].genre, self.library_tracks_df[self.library_tracks_df['Title']=='Nicolas Le Floch - Générique']['Genre'].values)
        self.assertEqual(self.process.track_instance_dict['Nicolas Le Floch - Générique && Stéphane Moucha'].genre, self.play_activity_df[self.play_activity_df['Title']=='Nicolas Le Floch - Générique']['Genre'].values)
        self.assertIn('Nicolas Le Floch - Générique', self.process.artist_tracks_titles['Stéphane Moucha'])
        #we verify that the rating corresponds to the value in likes_dislikes_df
        #note that in likes_dislikes_df the song rated is represented by the same track, but a different title!
        self.assertEqual(self.process.track_instance_dict['Nicolas Le Floch - Générique && Stéphane Moucha'].rating, self.likes_dislikes_df[self.likes_dislikes_df['Title']=='Nicolas Le Floch']['Preference'].values)
        #we verify that the apple id corresponds to the value in identifier_infos_df
        self.assertEqual(self.process.track_instance_dict['Nicolas Le Floch - Générique && Stéphane Moucha'].apple_music_id, self.identifier_infos_df[self.identifier_infos_df['Title']=='Nicolas Le Floch - Générique']['Identifier'].values)
        #let's note here that this value has to be also available in library_tracks_df, as the match from identifier_infos_df are made on the ids and not the titles
        ids_from_library = [int(x) for x in self.library_tracks_df[self.library_tracks_df['Title']=='Nicolas Le Floch - Générique'][['Apple Music Track Identifier', 'Track Identifier', 'Purchased Track Identifier', 'Tag Matched Track Identifier']].values[0]]
        self.assertIn(int(self.process.track_instance_dict['Nicolas Le Floch - Générique && Stéphane Moucha'].apple_music_id[0]), ids_from_library)

    @classmethod
    def tearDown(self):
        self.process = None
        self.parser = None
        self.likes_dislikes_df = None
        self.play_activity_df = None
        self.identifier_infos_df = None
        self.library_tracks_df = None
        self.library_activity_df = None
        self.track_instance = None


class TestProcessTrackSummaryObject(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #we use the test df
        target_files = {
            'identifier_infos_path' : 'test_df/Apple Music Activity/Identifier Information.json.zip',
            'library_tracks_path' : 'test_df/Apple Music Activity/Apple Music Library Tracks.json.zip',
            'library_activity_path': 'test_df/Apple Music Activity/Apple Music Library Activity.json.zip',
            'likes_dislikes_path' : 'test_df/Apple Music Activity/Apple Music Likes and Dislikes.csv',
            'play_activity_path': 'test_df/Apple Music Activity/Apple Music Play Activity.csv'
        }
        cls.input_df = Utility.get_df_from_archive('apple_music_analyser/tests/test_df.zip', target_files)
        cls.parser = Parser(cls.input_df)
        cls.likes_dislikes_df = cls.parser.likes_dislikes_df
        cls.play_activity_df = cls.parser.play_activity_df
        cls.identifier_infos_df = cls.parser.identifier_infos_df
        cls.library_tracks_df = cls.parser.library_tracks_df
        cls.library_activity_df = cls.parser.library_activity_df
        #we process the df
        cls.process = ProcessTracks()
        cls.process.process_library_tracks_df(cls.library_tracks_df)
        cls.process.process_identifier_df(cls.identifier_infos_df)
        cls.process.process_play_df(cls.play_activity_df)
        cls.process.process_likes_dislikes_df(cls.likes_dislikes_df)
        #we extract the useful objects from the process instance
        cls.track_instance_dict = cls.process.track_instance_dict
        cls.artist_tracks_titles = cls.process.artist_tracks_titles
        cls.genres_list = cls.process.genres_list
        cls.items_not_matched = cls.process.items_not_matched

    def setUp(self):
        self.track_summary_object = TrackSummaryObject(self.track_instance_dict, self.artist_tracks_titles, self.genres_list, self.items_not_matched)

    def test_init_TrackSummaryObject(self):
        result = self.track_summary_object
        # we verify that the track_instance_dict of the TrackSummaryObject is the one we passed as an input
        self.assertEqual(result.track_instance_dict, self.track_instance_dict)
        #idem for artist_tracks_titles and items_not_matched
        self.assertEqual(result.artist_tracks_titles, self.artist_tracks_titles)
        self.assertEqual(result.items_not_matched, self.items_not_matched)
        # genres_list has only one item to clean up, the nan item
        self.assertEqual(len(result.genres_list), len(self.genres_list))
        self.assertIn('', result.genres_list)
        #we validate that a new object is available for the TrackSummaryObject object
        self.assertEqual(result.match_index_instance, {})

    def test_get_track_instance_dict(self):
        result = self.track_summary_object.get_track_instance_dict()
        self.assertEqual(result, self.track_instance_dict)

    def test_get_artist_tracks_titles(self):
        result = self.track_summary_object.get_artist_tracks_titles()
        self.assertEqual(result, self.artist_tracks_titles)

    def test_get_genres_list(self):
        result = self.track_summary_object.get_genres_list()
        self.assertEqual(len(result), len(self.genres_list))
        self.assertIn('', result)

    def test_get_items_not_matched(self):
        result = self.track_summary_object.get_items_not_matched()
        self.assertEqual(result, self.items_not_matched)

    def test_get_match_index_instance(self):
        result = self.track_summary_object.get_match_index_instance()
        self.assertEqual(result, {})

    def test_build_index_track_instance_dict_play_activity(self):
        #we update the match_index_instance
        self.track_summary_object.build_index_track_instance_dict('play_activity')
        result = self.track_summary_object.match_index_instance
        # we have 165 items from play_activity_df, but 7 appear twice (indexes 16, 17, 72, 80, 85, 138 and 155)
        self.assertEqual(len(result), 158)
        self.assertTrue(isinstance(result[100], list))
        self.assertEqual(len(result[100]), 4)
        self.assertTrue(isinstance(result[100][1], bool))
        self.assertTrue(isinstance(result[100][2], list))
        self.assertTrue(isinstance(result[100][3], list))

    def test_build_index_track_instance_dict_library_tracks(self):
        #we update the match_index_instance
        self.track_summary_object.build_index_track_instance_dict('library_tracks')
        result = self.track_summary_object.match_index_instance
        # we have 39 items from play_activity_df, but 3 appear twice (indexes 4, 5, 10)
        self.assertEqual(len(result), 37)
        self.assertTrue(isinstance(result[0], list))
        self.assertEqual(len(result[0]), 4)
        self.assertTrue(isinstance(result[0][1], bool))
        self.assertTrue(isinstance(result[0][2], list))
        self.assertTrue(isinstance(result[0][3], list))

    def test_build_index_track_instance_dict_identifier_infos(self):
        #we update the match_index_instance
        self.track_summary_object.build_index_track_instance_dict('identifier_info')
        result = self.track_summary_object.match_index_instance
        # we have 31 items from play_activity_df, but 3 appear twice (indexes 13, 14, 19)
        self.assertEqual(len(result), 28)
        self.assertTrue(isinstance(result[20], list))
        self.assertEqual(len(result[20]), 4)
        self.assertTrue(isinstance(result[20][1], bool))
        self.assertTrue(isinstance(result[20][2], list))
        self.assertTrue(isinstance(result[20][3], list))

    def test_build_index_track_instance_dict_likes_dislikes(self):
        #we update the match_index_instance
        self.track_summary_object.build_index_track_instance_dict('likes_dislikes')
        result = self.track_summary_object.match_index_instance
        # we have 29 items from play_activity_df, but 2 appear twice (indexes 8, 28)
        self.assertEqual(len(result), 27)
        self.assertTrue(isinstance(result[0], list))
        self.assertEqual(len(result[0]), 4)
        self.assertTrue(isinstance(result[0][1], bool))
        self.assertTrue(isinstance(result[0][2], list))
        self.assertTrue(isinstance(result[0][3], list))

    def test_simplify_genre_list(self):
        genres_list = [float('NaN'), 'Genre_1', 'Genre_2 && Genre_3', ' Genre_4  ']
        result = self.track_summary_object.simplify_genre_list(genres_list)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], '')
        self.assertEqual(result[1], 'Genre_1')
        self.assertEqual(result[2], 'Genre_2 && Genre_3')
        self.assertEqual(result[3], 'Genre_4')

    def test_build_genres_count_dict(self):
        genres_serie = pd.Series(['Rock', 'Pop', 'Soundtrack && Pop'])
        result = self.track_summary_object.build_genres_count_dict(genres_serie)
        #we expect the output dictionary to be the same length than the genres_list of TrackSummaryObjects
        self.assertEqual(len(result), len(self.genres_list))
        # we expect the count of Rock and Soundtrack to be 1, and of Pop to be 2
        self.assertEqual(result['Pop'], 2)
        self.assertEqual(result['Rock'], 1)
        self.assertEqual(result['Soundtrack'], 1)

    def test_build_count_dict(self):
        target_serie = pd.Series(['Item_1', 'Item_1', 'Item_2'])
        result = self.track_summary_object.build_count_dict(target_serie)
        #we expect the output dictionary to be 2, as there are two distinct items in the target_serie
        self.assertEqual(len(result), 2)
        # we expect the count of Rock and Soundtrack to be 1, and of Pop to be 2
        self.assertEqual(result['Item_1'], 2)
        self.assertEqual(result['Item_2'], 1)

    def test_build_ranking_dict_per_year_per_genre(self):
        df = pd.DataFrame.from_dict({
            'Play_Year':[2020, 2020, 2020, 2019],
            'Genres':['Rock', 'Pop', 'Soundtrack && Pop', 'Rock'],
            'Artist':['Artist_1', 'Artist_3', 'Artist_1', 'Artist_2']
            })
        result = self.track_summary_object.build_ranking_dict_per_year(df, 'Genres')
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 2)
        self.assertTrue(isinstance(result[2020], dict))
        self.assertEqual(len(result[2020]), len(self.genres_list))
        self.assertEqual(result[2020]['Rock'], 1)
        self.assertEqual(result[2020]['Pop'], 2)
        self.assertEqual(result[2020]['Soundtrack'], 1)
        self.assertTrue(isinstance(result[2019], dict))
        self.assertEqual(len(result[2019]), len(self.genres_list))
        self.assertEqual(result[2019]['Rock'], 1)
        self.assertEqual(result[2019]['Pop'], 0)
        self.assertEqual(result[2019]['Soundtrack'], 0)

    def test_build_ranking_dict_per_year_per_artist(self):
        df = pd.DataFrame.from_dict({
            'Play_Year':[2020, 2020, 2020, 2019],
            'Genres':['Rock', 'Pop', 'Soundtrack && Pop', 'Rock'],
            'Artist':['Artist_1', 'Artist_3', 'Artist_1', 'Artist_2']
            })
        result = self.track_summary_object.build_ranking_dict_per_year(df, 'Artist')
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 2)
        self.assertTrue(isinstance(result[2020], dict))
        self.assertEqual(len(result[2020]), 2)
        self.assertEqual(result[2020]['Artist_3'], 1)
        self.assertNotIn('Artist_2', list(result[2020].keys()))
        self.assertEqual(result[2020]['Artist_1'], 2)
        self.assertTrue(isinstance(result[2019], dict))
        self.assertEqual(len(result[2019]), 1)
        self.assertEqual(result[2019]['Artist_2'], 1)
        self.assertNotIn('Artist_1', list(result[2019].keys()))
        self.assertNotIn('Artist_3', list(result[2019].keys()))

    def test_build_ranking_dict_per_year_per_other(self):
        df = pd.DataFrame.from_dict({
            'Play_Year':[2020, 2020, 2020, 2019],
            'Genres':['Rock', 'Pop', 'Soundtrack && Pop', 'Rock'],
            'Artist':['Artist_1', 'Artist_3', 'Artist_1', 'Artist_2']
            })
        result = self.track_summary_object.build_ranking_dict_per_year(df, 'Other_Key')
        self.assertEqual(result, {})

    def tearDown(self):
        self.track_summary_object = None

    @classmethod
    def tearDownClass(cls):
        cls.input_df = None
        cls.parser = None
        cls.likes_dislikes_df = None
        cls.play_activity_df = None
        cls.identifier_infos_df = None
        cls.library_tracks_df = None
        cls.library_activity_df = None
        cls.process = None
        cls.track_instance_dict = None
        cls.artist_tracks_titles = None
        cls.genres_list = None
        cls.items_not_matched = None

if __name__ == '__main__':
    unittest.main()