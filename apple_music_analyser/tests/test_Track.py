import unittest

from apple_music_analyser.Track import Track

class TestTrack(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.track = Track('id')

    def test_init_track(self):
        self.assertTrue(isinstance(self.track, Track))
        self.assertEqual(self.track.identifier, 'id')
        self.assertEqual(self.track.titles, [])
        self.assertEqual(self.track.artist, None)
        self.assertEqual(self.track.is_in_lib, False)
        self.assertEqual(self.track.appearances, [])
        self.assertEqual(self.track.genre, [])
        self.assertEqual(self.track.apple_music_id, [])
        self.assertEqual(self.track.rating, [])

    def test_has_title_name(self):
        self.track.titles = ['Title']
        self.assertEqual(self.track.has_title_name('Title'), True)
        self.assertEqual(self.track.has_title_name('Other Title'), False)
        self.track.titles = []

    def test_add_title(self):
        self.track.add_title('New Title')
        self.assertEqual(self.track.titles, ['New Title'])

    def test_set_artist(self):
        self.track.set_artist('New Artist')
        self.assertEqual(self.track.artist, 'New Artist')

    def test_set_apple_music_id(self):
        self.track.set_apple_music_id(1234567)
        self.assertEqual(self.track.apple_music_id, [1234567])

    def test_set_library_flag(self):
        self.assertEqual(self.track.is_in_lib, False)
        self.track.set_library_flag()
        self.assertEqual(self.track.is_in_lib, True)

    def test_set_genre(self):
        genre = float('NaN')
        self.track.set_genre(genre)
        self.assertEqual(self.track.genre, [])
        genre = 'Genre'
        self.track.set_genre(genre)
        self.assertEqual(self.track.genre, ['Genre'])

    def test_add_appearance(self):
        appearance_dict = {'source': 'source', 'df_index':'index'}
        self.track.add_appearance(appearance_dict)
        self.assertEqual(self.track.appearances, [{'source': 'source', 'df_index':'index'}])

    def test_set_rating(self):
        rating = 'LOVE'
        self.track.set_rating(rating)
        self.assertEqual(self.track.rating, ['LOVE'])
        rating = 'LIKE'
        self.track.set_rating(rating)
        self.assertEqual(self.track.rating, ['LOVE'])
        rating = 'DISLIKE'
        self.track.set_rating(rating)
        self.assertEqual(self.track.rating, ['LOVE', 'DISLIKE'])
        rating = 'other rating'
        self.track.set_rating(rating)
        self.assertEqual(self.track.rating, ['LOVE', 'DISLIKE'])

    @classmethod
    def tearDown(self):
        self.track = None


if __name__ == '__main__':
    unittest.main()