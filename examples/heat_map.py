from apple_music_analyser.Utility import Utility
from apple_music_analyser.Query import QueryFactory
from apple_music_analyser.DataVisualization import HeatMapVisualization



# GET THE INPUT - Loading a pickle file
###########################################################################################################################
# see starter_code.py and save_load.py for more details

viz_df_instance = Utility.load_from_pickle('viz_df_instance.pkl')
df_viz = viz_df_instance.get_df_viz()


# BUILD THE HEATMAP DAY OF MONTH FOR A SINGLE YEAR
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

# in this example we specify just the target year, but you can add any other key to filter more!
query_params = {
    'year':[2018]
}

# define the query
query = QueryFactory().create_query(df_viz, query_params)
filtered_df = query.get_filtered_df()

# we create the heat map
# create the HeatMap instance
heat_map = HeatMapVisualization(filtered_df)
# generate the plot
heat_map.render_heat_map('DOM', '2018')
# display the plot rendered
heat_map.figure.show()



# BUILD THE HEATMAP DAY OF MONTH FOR MULTIPLE YEARS
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
    'year':[2017, 2018, 2019],
    'rating':['LOVE']
}

# create the HeatMap instance, with 3 subplots as we want to plot three years
heat_map = HeatMapVisualization(df_viz, 3)

# for each year, get a filtered dataframe, and generate the subplots
for year in query_params['year']:
	year_query_params = query_params
	year_query_params['year'] = [year]
	query = QueryFactory().create_query(df_viz, query_params)
	filtered_df = query.get_filtered_df()
	heat_map.df = filtered_df
	heat_map.render_heat_map('DOM', str(year))

# display the plot rendered
heat_map.figure.show()


# BUILD THE HEATMAP DAY OF WEEK FOR A SINGLE YEAR
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

# in this example we specify just the target year, but you can add any other key to filter more!
query_params = {
    'year':[2018]
}	

# define the query
query = QueryFactory().create_query(df_viz, query_params)
filtered_df = query.get_filtered_df()

# we create the heat map
# create the HeatMap instance
heat_map = HeatMapVisualization(filtered_df)
# generate the plot
heat_map.render_heat_map('DOW', '2018')
# display the plot rendered
heat_map.figure.show()



# BUILD THE HEATMAP DAY OF WEEK FOR MULTIPLE YEAR
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
    'year':[2017, 2018, 2019],
    'rating':['LOVE']
}

# create the HeatMap instance, with 3 subplots as we want to plot three years
heat_map = HeatMapVisualization(df_viz, 3)

# for each year, get a filtered dataframe, and generate the subplots
for year in query_params['year']:
	year_query_params = query_params
	year_query_params['year'] = [year]
	query = QueryFactory().create_query(df_viz, query_params)
	filtered_df = query.get_filtered_df()
	heat_map.df = filtered_df
	heat_map.render_heat_map('DOW', str(year))

# display the plot rendered
heat_map.figure.show()
