import pandas as pd
import unittest

from apple_music_analyser.Query import Query, QueryFactory

class TestQueryFactory(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        df = {'Artist':['Artist_1', 'Artist_2'], 'Title': ['Title_1', 'Title_2'], 
            'Offline':[False, True], 'Play_Year':[2020, 2019], 
            'Played_completely':[True, False], 'Track_origin':['library', 'other'],
            'Library_Track':[True, False], 'Rating':['LOVE', 'Unknown'],
            'Genres':['Genre_1', 'Genre_2']
        }
        self.reference_df = pd.DataFrame.from_dict(df)
        self.query_factory = QueryFactory()

    def test_init_QueryFactory(self):
        self.assertTrue(isinstance(self.query_factory, QueryFactory))

    def test_query_creator_without_params(self):
        query = self.query_factory.create_query(self.reference_df)
        query_params_default = {
                'year':self.reference_df['Play_Year'].unique()
            }
        self.assertTrue(isinstance(query, Query))
        self.assertEqual(query.reference_df.shape, self.reference_df.shape)
        self.assertEqual(query.reference_df.columns.tolist(), self.reference_df.columns.tolist())
        self.assertEqual(len(query.reference_df['Artist']), 2)
        self.assertEqual(len(query.query_params), len(query_params_default))
        self.assertEqual(len(query.query_params['year']), 2)
        self.assertNotIn('genre', list(query.query_params.keys()))
        self.assertNotIn('artist', list(query.query_params.keys()))
        self.assertNotIn('title', list(query.query_params.keys()))
        self.assertNotIn('rating', list(query.query_params.keys()))
        self.assertNotIn('origin', list(query.query_params.keys()))
        self.assertNotIn('offline', list(query.query_params.keys()))
        self.assertNotIn('library', list(query.query_params.keys()))
        self.assertNotIn('skipped', list(query.query_params.keys()))

    def test_query_creator_with_params(self):
        query_params = {
                'year':[2019],
                'genre':['Genre_1'],
                'artist':['Artist_1'],
                'title':['Title_1'],
                'rating':['LOVE'],
                'origin':['library'],
                'offline':False,
                'library':True,
                'skipped':False,
            }
        query = self.query_factory.create_query(self.reference_df, query_params)
        self.assertTrue(isinstance(query, Query))
        self.assertEqual(query.reference_df.shape, self.reference_df.shape)
        self.assertEqual(query.reference_df.columns.tolist(), self.reference_df.columns.tolist())
        self.assertEqual(len(query.reference_df['Artist']), 2)
        self.assertEqual(len(query.query_params), len(query_params))
        self.assertEqual(len(query.query_params['year']), 1)
        self.assertEqual(query.query_params['genre'], ['Genre_1'])

    @classmethod
    def tearDownClass(self):
        self.reference_df = None
        self.query_factory = None


class TestQuery(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        df = {'Artist':['Artist_1', 'Artist_2'], 'Title': ['Title_1', 'Title_2'], 
            'Offline':[False, True], 'Play_Year':[2020, 2019], 
            'Played_completely':[True, False], 'Track_origin':['library', 'other'],
            'Library_Track':[True, False], 'Rating':['LOVE', 'Unknown'],
            'Genres':['Genre_1', 'Genre_2']
        }
        self.query_params = {
            'year':[2020],
            'genre':['Genre_1'],
            'artist':['Artist_1'],
            'title':['Title_1'],
            'rating':['LOVE'],
            'origin':['library'],
            'offline':False,
            'library':True,
            'skipped':False,
        }
        self.reference_df = pd.DataFrame.from_dict(df)
        self.query = Query(self.reference_df, self.query_params)

    def test_init_Query(self):
        '''
            query_string and filtered_df are tested in individual tests
        '''
        self.assertTrue(isinstance(self.query, Query))
        self.assertEqual(self.query.reference_df.shape, self.reference_df.shape)
        self.assertEqual(self.query.reference_df.columns.tolist(), self.reference_df.columns.tolist())
        self.assertEqual(len(self.query.reference_df['Artist']), 2)
        self.assertEqual(len(self.query.query_params), len(self.query_params))
        self.assertEqual(len(self.query.query_params['year']), 1)
        self.assertEqual(self.query.query_params['genre'], ['Genre_1'])

    def test_get_query_params(self):
        result = self.query.get_query_params()
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 9)

    def test_get_query_string(self):
        result = self.query.get_query_string()
        self.assertTrue(isinstance(result, str))
        self.assertEqual(result, 'Play_Year==2020&Genres.str.contains("Genre_1")&Artist.str.contains("Artist_1")&Title.str.contains("Title_1")&Rating.str.contains("LOVE")&Track_origin.str.contains("library")&Offline.isin([False])&Library_Track.isin([True])&Played_completely.isin([True])')

    def test_get_filtered_df(self):
        result = self.query.get_filtered_df()
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(result.shape[0], 1)
        self.assertEqual(result['Play_Year'][0], 2020)

    def test_build_string_query_element(self):
        result_one_string = self.query.build_string_query_element('Category', ['value_1'])
        result_two_strings = self.query.build_string_query_element('Category', ['value_1', 'value_2'])
        result_three_strings = self.query.build_string_query_element('Category', ['value_1', 'value_2', 'value_3'])
        self.assertTrue(isinstance(result_one_string, str))
        self.assertEqual(result_one_string, 'Category.str.contains("value_1")')
        self.assertTrue(isinstance(result_two_strings, str))
        self.assertEqual(result_two_strings, '(Category.str.contains("value_1")|Category.str.contains("value_2"))')
        self.assertTrue(isinstance(result_three_strings, str))
        self.assertEqual(result_three_strings, '(Category.str.contains("value_1")|Category.str.contains("value_2")|Category.str.contains("value_3"))')

    def test_build_numeric_query_element(self):
        result_one_num = self.query.build_numeric_query_element('Category', [1])
        result_two_num = self.query.build_numeric_query_element('Category', [1, 2])
        result_three_num = self.query.build_numeric_query_element('Category', [1, 2, 3])
        self.assertTrue(isinstance(result_one_num, str))
        self.assertEqual(result_one_num, 'Category==1')
        self.assertTrue(isinstance(result_two_num, str))
        self.assertEqual(result_two_num, '(Category==1|Category==2)')
        self.assertTrue(isinstance(result_three_num, str))
        self.assertEqual(result_three_num, '(Category==1|Category==2|Category==3)')

    def test_build_boolean_query_element(self):
        result_true = self.query.build_boolean_query_element('Category', True)
        result_false = self.query.build_boolean_query_element('Category', False)
        self.assertTrue(isinstance(result_true, str))
        self.assertEqual(result_true, 'Category.isin([True])')
        self.assertTrue(isinstance(result_false, str))
        self.assertEqual(result_false, 'Category.isin([False])')

    @classmethod
    def tearDownClass(self):
        self.reference_df = None
        self.query = None
        self.query_params = None

if __name__ == '__main__':
    unittest.main()