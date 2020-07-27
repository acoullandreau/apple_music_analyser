from apple_music_analyser.Utility import Utility
from apple_music_analyser.VisualizationDataframe import VisualizationDataframe




# CASE 1 - you pass the archive provided by Apple
###########################################################################################################################

# get the input files - with a structure like the one of the archive Apple provides
input_df = Utility.get_df_from_archive(path_to_archive)

# create an instance of the visualization dataframe class
viz_df_instance = VisualizationDataframe(input_df)



# CASE 2 - you want to pass the files in an archive with a custom structure
###########################################################################################################################

# get the input files - from an archive with a custom structure
# you can run this code as is, we use the files used for testing

path_to_archive = '../apple_music_analyser/tests/test_df.zip'
target_files = {
	'identifier_infos_path' : 'test_df/Apple Music Activity/Identifier Information.json.zip',
	'library_tracks_path' : 'test_df/Apple Music Activity/Apple Music Library Tracks.json.zip',
	'library_activity_path': 'test_df/Apple Music Activity/Apple Music Library Activity.json.zip',
	'likes_dislikes_path' : 'test_df/Apple Music Activity/Apple Music Likes and Dislikes.csv',
	'play_activity_path': 'test_df/Apple Music Activity/Apple Music Play Activity.csv'
	}

input_df = Utility.get_df_from_archive(path_to_archive, target_files)

# create an instance of the visualization dataframe class
viz_df_instance = VisualizationDataframe(input_df)