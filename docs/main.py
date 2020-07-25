from apple_music_analyser.VisualizationDataframe import VisualizationDataframe
from apple_music_analyser.Utility import Utility
from apple_music_analyser.DataVisualization import SunburstVisualization, RankingListVisualization, HeatMapVisualization, PieChartVisualization, BarChartVisualization
from apple_music_analyser.Query import Query, QueryFactory

import time

start0 = time.time()

# get the input files
#input_df = Utility.get_df_from_archive('data/Apple_Media_Services_L.zip')

# create an instance of the visualization dataframe class
#df_viz = VisualizationDataframe(input_df)
#Utility.save_to_pickle(df_viz, 'df_viz.pkl')

#df_viz = Utility.load_from_pickle('df_viz.pkl')


path_to_archive = '../apple_music_analyser/apple_music_analyser/tests/test_df.zip'
target_files = {
	'identifier_infos_path' : 'test_df/Apple Music Activity/Identifier Information.json.zip',
	'library_tracks_path' : 'test_df/Apple Music Activity/Apple Music Library Tracks.json.zip',
	'library_activity_path': 'test_df/Apple Music Activity/Apple Music Library Activity.json.zip',
	'likes_dislikes_path' : 'test_df/Apple Music Activity/Apple Music Likes and Dislikes.csv',
	'play_activity_path': 'test_df/Apple Music Activity/Apple Music Play Activity.csv'
	}
input_df = Utility.get_df_from_archive(path_to_archive, target_files)
df_viz = VisualizationDataframe(input_df)

print(df_viz.df_visualization.shape)


###########################################################################################################################
#extract a df using a query
# query_params = {
#     'year':[2017, 2018, 2019],
#     'rating':['LOVE']
# }
#filtered_df = QueryFactory().create_query(df_viz.get_df_viz(), query_params)
#print(filtered_df.filtered_df.shape)


###########################################################################################################################
#plot a sunburst
# query_params = {
#     'year':[2016, 2017, 2018, 2019],
# }
# ranking_dict = df_viz.track_summary_objects.build_ranking_dict_per_year(df_viz.get_df_viz(), 'Genres') #optional query_params
# sunburst = SunburstVisualization(ranking_dict, 'Genre')
# sunburst.render_sunburst_plot()


###########################################################################################################################
#get a ranking dict
# df = df_viz.get_df_viz()
# query_params = {
#     'year':sorted(df['Play_Year'].dropna().unique()),
# }
# ranking_dict = df_viz.track_summary_objects.build_ranking_dict_per_year(df, 'Genres', query_params)
# ranking = RankingListVisualization(ranking_dict, 5)
# ranking.get_ranked_dict(print_output=True)



###########################################################################################################################
#plot a heatmap DOM for a single year
# query_params = {
#     'year':[2018],
#     'rating':['LOVE']
# }
# filtered_df = QueryFactory().create_query(df_viz.get_df_viz(), query_params)
# heat_map = HeatMapVisualization(filtered_df.filtered_df)
# heat_map.render_heat_map('DOM', '2018')
# heat_map.figure.show()

#plot a heatmap for multiple years
# query_params = {
#     'year':[2017, 2018, 2019],
#     'rating':['LOVE']
# }

# heat_map = HeatMapVisualization(df_viz.get_df_viz(), 3)

# for year in query_params['year']:
#   year_query_params = query_params
#   year_query_params['year'] = [year]
#   filtered_df = QueryFactory().create_query(df_viz.get_df_viz(), query_params)
#   heat_map.df = filtered_df.filtered_df
#   heat_map.render_heat_map('DOM', str(year))

# heat_map.figure.show()

#plot a heatmap DOW for a single year
# query_params = {
#     'year':[2018],
# }
# filtered_df = QueryFactory().create_query(df_viz.get_df_viz(), query_params)
# heat_map = HeatMapVisualization(filtered_df.filtered_df)
# heat_map.render_heat_map('DOW', '2018')
# heat_map.figure.show()


#plot a heatmap DOW for a multiple years
# query_params = {
#     'year':[2015, 2016, 2017, 2018, 2019],
# }

# heat_map = HeatMapVisualization(df_viz.get_df_viz(), 5)

# for year in query_params['year']:
#   year_query_params = query_params
#   year_query_params['year'] = [year]
#   filtered_df = QueryFactory().create_query(df_viz.get_df_viz(), query_params)
#   heat_map.df = filtered_df.filtered_df
#   heat_map.render_heat_map('DOW', str(year))

# heat_map.figure.show()


###########################################################################################################################

# plot a pie chart
# query_params = {
#     'year':[2017, 2018, 2019],
#     'rating':['LOVE']
# }
# filtered_df = QueryFactory().create_query(df_viz.get_df_viz(), query_params)
# pie_chart = PieChartVisualization(filtered_df.filtered_df['Play_Year'])
# pie_chart.render_pie_chart()
# pie_chart.figure.show()

# # plot a pie chart with another df
# pie_chart = PieChartVisualization(df_viz.get_library_activity_df()['Transaction Agent Model'])
# pie_chart.render_pie_chart()
# pie_chart.figure.show()


###########################################################################################################################
# plot a bar chart - DOW
# df = df_viz.get_df_viz()
# years_to_plot = sorted(df['Play_Year'].dropna().unique())
# bar_chart = BarChartVisualization(df)
# bar_chart.hover_unit = '%'

# for year in years_to_plot:
#     x_serie = df[df['Play_Year']==year]['Play_DOW'].unique()
#     y_serie = Utility.compute_ratio_songs(df[df['Play_Year']==year]['Play_DOW'])
#     bar_chart.render_bar_chart(x_serie, y_serie, str(year))

# xaxis=dict(categoryorder='array',
#             tickangle = -45,
#             categoryarray = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

# bar_chart.figure.update_layout(xaxis =xaxis)
# bar_chart.figure.show()

# plot a bar chart - Month
# df = df_viz.get_df_viz()
# years_to_plot = sorted(df['Play_Year'].dropna().unique())
# bar_chart = BarChartVisualization(df)
# bar_chart.title = 'Distribution of number of tracks listened to per mont for different years'

# for year in years_to_plot:
#     x_serie = df[df['Play_Year']==year]['Play_Month'].unique()
#     y_serie = df[df['Play_Year']==year]['Play_Month'].value_counts()
#     bar_chart.render_bar_chart(x_serie, y_serie, str(year))

# xaxis=dict(
#     tickangle = -45,
#     tickmode = 'array',
#     tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
#     ticktext = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

# yaxis=dict(
#     title='Percentage of tracks listened to per year',
#     titlefont_size=16,
#     tickfont_size=14,
# )

# bar_chart.figure.update_layout(xaxis = xaxis, yaxis = yaxis)
# bar_chart.figure.show()



# plot subplots of bar chart - HOD
# df = df_viz.get_df_viz()
# years_to_plot = sorted(df['Play_Year'].dropna().unique())
# years_to_plot = [2018, 2019]
# bar_chart = BarChartVisualization(df, with_subplots=len(years_to_plot))

# for year in years_to_plot:
#     x_serie = df[df['Play_Year']==year]['Play_HOD'].unique()
#     y_serie = df[df['Play_Year']==year]['Play_HOD'].value_counts()
#     bar_chart.render_bar_chart(x_serie, y_serie, str(year))

# bar_chart.figure.show()


# plot subplots of bar chart - HOD, single year
# # get the input df 
# df = df_viz.get_df_viz()
# df = df[df['Play_Year']==2020]
# # create the BarChart instance
# bar_chart = BarChartVisualization(df)
# # render the plot
# x_serie = df['Play_HOD'].unique()
# y_serie = df['Play_HOD'].value_counts()
# bar_chart.render_bar_chart(x_serie, y_serie, '2020')
# # display the rendered plot
# bar_chart.figure.show()



# plot bar chart with two series
# df = df_viz.get_df_viz()
# years_to_plot = sorted(df['Play_Year'].dropna().unique())
# bar_chart = BarChartVisualization(df)
# bar_chart.title='Ratio of tracks skipped, versus listened to completely, per year'
# bar_chart.hover_unit = '%'

# df_track_complete = df[df['Played_completely']==True]
# df_track_partial = df[df['Played_completely']==False]
# y_complete = []
# y_partial = []

# for year in years_to_plot:
#     count_tracks_complete = df_track_complete[df_track_complete['Play_Year']==year].shape[0]
#     count_tracks_partial = df_track_partial[df_track_partial['Play_Year']==year].shape[0]
#     percent_tracks_complete = 100*count_tracks_complete/df[df['Play_Year']==year].shape[0]
#     percent_tracks_partial = 100*count_tracks_partial/df[df['Play_Year']==year].shape[0]
#     y_complete.append(percent_tracks_complete)
#     y_partial.append(percent_tracks_partial)

# bar_chart.render_bar_chart(years_to_plot, y_complete, 'Complete listening')
# bar_chart.render_bar_chart(years_to_plot, y_partial, 'Partial listening')

# bar_chart.figure.update_layout(
#     barmode='stack',
#     yaxis=dict(title='Percentage of tracks')
# )
# bar_chart.figure.show()




end = time.time()
print('Total', end - start0)
