from apple_music_analyser.VisualizationDataframe import VisualizationDataframe
from apple_music_analyser.Utility import Utility


# LOAD A PICKLE 
###########################################################################################################################

# we assume you have an instance of the visualization dataframe class saved in the same folder under the name 'viz_df_instance.pkl'
viz_df_instance = Utility.load_from_pickle('viz_df_instance.pkl')


# SAVE A PICKLE 
###########################################################################################################################

# get the input file - see starter_code.py for more details

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

# save the instance
Utility.save_to_pickle(viz_df_instance, 'viz_df_instance.pkl')

