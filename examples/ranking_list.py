from apple_music_analyser.Utility import Utility
from apple_music_analyser.Query import QueryFactory
from apple_music_analyser.DataVisualization import RankingListVisualization


# GET THE INPUT - Loading a pickle file
###########################################################################################################################
# see starter_code.py and save_load.py for more details

viz_df_instance = Utility.load_from_pickle('viz_df_instance.pkl')
df_viz = viz_df_instance.get_df_viz()

# BUILD THE RANKING LIST WITHOUT QUERY
###########################################################################################################################

# construct a count dict
# possible to replace 'Genres' by: 'Title', 'Artist', 'Track_origin'
count_dict_genres = viz_df_instance.track_summary_objects.build_ranking_dict_per_year(df_viz, 'Genres')

# build the ranking list, limited to 5 items per year
ranking_genres = RankingListVisualization(count_dict_genres, 5)

# get the ranked_dict, printed on the console
ranking_genres.get_ranked_dict(print_output=True)


# BUILD THE RANKING LIST WITH QUERY
###########################################################################################################################

# define the query parameters
	# params_dict = {
	#     'year':list,
	#     'genre':list,
	#     'artist':list,
	#     'title':list,
	#     'rating':list,
	#     'origin':list,
	#     'offline':bool,
	#     'library':bool,
	#     'skipped':bool,
	# }

query_params = {
    'year':[2019],
    'rating':['LOVE'],
    'skipped':False
}

# construct a count dict
# possible to replace 'Artist' by: 'Title', 'Genres', 'Track_origin'
count_dict_artist = viz_df_instance.track_summary_objects.build_ranking_dict_per_year(df_viz, 'Artist', query_params)

# build the ranking list, limited to 3 items per year
ranking_artists = RankingListVisualization(count_dict_artist, 3)

# get the ranked_dict, printed on the console
ranking_artists.get_ranked_dict(print_output=True)


