from apple_music_analyser.Utility import Utility
from apple_music_analyser.Query import QueryFactory
from apple_music_analyser.DataVisualization import BarChartVisualization


# GET THE INPUT - Loading a pickle file
###########################################################################################################################
# see starter_code.py and save_load.py for more details

viz_df_instance = Utility.load_from_pickle('viz_df_instance.pkl')
df_viz = viz_df_instance.get_df_viz()
# note that you can filter this df_viz using queries (see query.py for examples!)


# BUILD A BAR CHART FOR DAY OF THE WEEK WITH RATIO OF SONGS
###########################################################################################################################

# create the BarChart instance
years_to_plot = sorted(df_viz['Play_Year'].dropna().unique())
bar_chart = BarChartVisualization(df_viz)
bar_chart.hover_unit = '%'

# for each year, build the x and y series, computing the percentage of songs, and generate the traces
for year in years_to_plot:
    x_serie = df_viz[df_viz['Play_Year']==year]['Play_DOW'].unique()
    y_serie = Utility.compute_ratio_songs(df_viz[df_viz['Play_Year']==year]['Play_DOW'])
    bar_chart.render_bar_chart(x_serie, y_serie, str(year))

# edit the layout of the xaxis and show the rendered plot
xaxis=dict(categoryorder='array',
            tickangle = -45,
            categoryarray = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

bar_chart.figure.update_layout(xaxis =xaxis)
bar_chart.figure.show()


# BUILD A BAR CHART FOR MONTH WITH COUNT OF SONGS
###########################################################################################################################

# create the BarChart instance
years_to_plot = sorted(df_viz['Play_Year'].dropna().unique())
bar_chart = BarChartVisualization(df_viz)
bar_chart.title = 'Distribution of number of tracks listened to per mont for different years'

# for each year, build the x and y series, computing the count of songs, and generate the traces
for year in years_to_plot:
    x_serie = df_viz[df_viz['Play_Year']==year]['Play_Month'].unique()
    y_serie = df_viz[df_viz['Play_Year']==year]['Play_Month'].value_counts()
    bar_chart.render_bar_chart(x_serie, y_serie, str(year))

# edit the layout of the xaxis, yaxis and show the rendered plot
xaxis=dict(
    tickangle = -45,
    tickmode = 'array',
    tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    ticktext = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

yaxis=dict(
    title='Percentage of tracks listened to per year',
    titlefont_size=16,
    tickfont_size=14,
)

bar_chart.figure.update_layout(xaxis = xaxis, yaxis = yaxis)
bar_chart.figure.show()



# BUILD A BAR CHART FOR HOUR OF THE DAY WITH COUNT OF SONGS AND ONE PLOT PER YEAR (SUBPLOTS)
###########################################################################################################################

# create the BarChart instance
years_to_plot = [2018, 2019]
bar_chart = BarChartVisualization(df_viz, with_subplots=len(years_to_plot))

# for each year, build the x and y series, computing the count of songs, and generate the subplots
for year in years_to_plot:
    x_serie = df_viz[df_viz['Play_Year']==year]['Play_HOD'].unique()
    y_serie = df_viz[df_viz['Play_Year']==year]['Play_HOD'].value_counts()
    bar_chart.render_bar_chart(x_serie, y_serie, str(year))

bar_chart.figure.show()



# BUILD A BAR CHART FOR HOUR OF THE DAY WITH PERCENTAGE OF SONGS FOR ONE SINGLE YEAR WITHOUT QUERY
###########################################################################################################################

# get the input df
df = df_viz[df_viz['Play_Year']==2020]

# create the BarChart instance
bar_chart = BarChartVisualization(df)

# render the plot
x_serie = df['Play_HOD'].unique()
y_serie = Utility.compute_ratio_songs(df['Play_HOD'])
bar_chart.render_bar_chart(x_serie, y_serie, '2020')

# display the rendered plot
bar_chart.figure.show()



# BUILD A BAR CHART FOR MULTIPLE SERIES ON A SINGLE TRACE
###########################################################################################################################

# create the BarChart instance
years_to_plot = sorted(df_viz['Play_Year'].dropna().unique())
bar_chart = BarChartVisualization(df_viz)
bar_chart.title='Ratio of tracks skipped, versus listened to completely, per year'
bar_chart.hover_unit = '%'

df_track_complete = df_viz[df_viz['Played_completely']==True]
df_track_partial = df_viz[df_viz['Played_completely']==False]
y_complete = []
y_partial = []

# for each year, build the x and y series, computing the percentage of songs
for year in years_to_plot:
    count_tracks_complete = df_track_complete[df_track_complete['Play_Year']==year].shape[0]
    count_tracks_partial = df_track_partial[df_track_partial['Play_Year']==year].shape[0]
    percent_tracks_complete = 100*count_tracks_complete/df_viz[df_viz['Play_Year']==year].shape[0]
    percent_tracks_partial = 100*count_tracks_partial/df_viz[df_viz['Play_Year']==year].shape[0]
    y_complete.append(percent_tracks_complete)
    y_partial.append(percent_tracks_partial)

# render each trace on the same plot
bar_chart.render_bar_chart(years_to_plot, y_complete, 'Complete listening')
bar_chart.render_bar_chart(years_to_plot, y_partial, 'Partial listening')

# edit the layout and show the rendered plot
bar_chart.figure.update_layout(
    barmode='stack',
    yaxis=dict(title='Percentage of tracks')
)
bar_chart.figure.show()



