from apple_music_analyser.Utility import Utility
from apple_music_analyser.Query import QueryFactory


# GET THE INPUT - Loading a pickle file
###########################################################################################################################
# see starter_code.py and save_load.py for more details

viz_df_instance = Utility.load_from_pickle('viz_df_instance.pkl')


# MAKE THE QUERY
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

# define the query
df_viz = viz_df_instance.get_df_viz()
query = QueryFactory().create_query(df_viz, query_params)

# get the filtered df
filtered_df = query.get_filtered_df()
print(filtered_df.shape)

# get the query string
query_string = query.get_query_string()
print(query_string)


# NOTE ON THE 'year' PARAMETER
###########################################################################################################################

# you may want to add all the years available in the df in your query parameters, and in this case you can do:
# query_params = {
#     'year':sorted(df_viz['Play_Year'].dropna().unique()),
# }