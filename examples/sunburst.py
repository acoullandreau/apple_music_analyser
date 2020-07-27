from apple_music_analyser.Utility import Utility
from apple_music_analyser.Query import QueryFactory
from apple_music_analyser.DataVisualization import SunburstVisualization


# GET THE INPUT - Loading a pickle file
###########################################################################################################################
# see starter_code.py and save_load.py for more details

viz_df_instance = Utility.load_from_pickle('viz_df_instance.pkl')
df_viz = viz_df_instance.get_df_viz()

# BUILD THE SUNBURST LIST WITHOUT QUERY
###########################################################################################################################

# construct a count dict
# possible to replace 'Genres' by: 'Title', 'Artist', 'Track_origin'
count_dict_genres = viz_df_instance.track_summary_objects.build_ranking_dict_per_year(df_viz, 'Genres')

# build the sunburst, with the title 'Genre' (that can be replaced by anything)
sunburst = SunburstVisualization(count_dict_genres, 'Genre')

# render the plot
sunburst.render_sunburst_plot()


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
    'year':[2018, 2019],
    'skipped':False
}

# construct a count dict
# possible to replace 'Genres' by: 'Title', 'Artist', 'Track_origin'
count_dict_genres = viz_df_instance.track_summary_objects.build_ranking_dict_per_year(df_viz, 'Genres', query_params)

# build the sunburst, with the title 'Genre' (that can be replaced by anything)
sunburst = SunburstVisualization(count_dict_genres, 'Genre')

# render the plot
sunburst.render_sunburst_plot()

