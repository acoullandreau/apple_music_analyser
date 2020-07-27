from apple_music_analyser.Utility import Utility
from apple_music_analyser.Query import QueryFactory
from apple_music_analyser.DataVisualization import PieChartVisualization


# GET THE INPUT - Loading a pickle file
###########################################################################################################################
# see starter_code.py and save_load.py for more details

viz_df_instance = Utility.load_from_pickle('viz_df_instance.pkl')
df_viz = viz_df_instance.get_df_viz()

# PLOT A PIE CHART FOR A DISTRIBUTION OF COUNT OF SONGS PER YEAR WITH A QUERY
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
query = QueryFactory().create_query(df_viz, query_params)
filtered_df = query.get_filtered_df()

# create the PieChart instance
pie_chart = PieChartVisualization(filtered_df['Play_Year'])

# generate the plot
pie_chart.render_pie_chart()

# display the plot rendered
pie_chart.figure.show()



# PLOT A PIE CHART FOR A DISTRIBUTION OF COUNT OF SONGS PER YEAR WITHOUT A QUERY
###########################################################################################################################

# create the PieChart instance
pie_chart = PieChartVisualization(df_viz['Play_Year'])

# generate the plot
pie_chart.render_pie_chart()

# display the plot rendered
pie_chart.figure.show()



# PLOT A PIE CHART FOR A DISTRIBUTION OF MODEL USED TO USE THE APPLE MUSIC SERVICE
###########################################################################################################################

# get the dataframe
library_activity_df = viz_df_instance.get_library_activity_df()

# create the PieChart instance
pie_chart = PieChartVisualization(library_activity_df['Transaction Agent Model'])

# generate the plot
pie_chart.render_pie_chart()

# display the plot rendered
pie_chart.figure.show()


