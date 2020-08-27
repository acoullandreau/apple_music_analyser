import plotly.graph_objs as go
from plotly.subplots import make_subplots

from apple_music_analyser.Utility import Utility

class SunburstVisualization():

    '''
        This class is responsible for generating a sunburst graph from
        the objects contained in a dictionary. 
        Once rendered a page opens automatically in a browser to display the plot.

        Args: 
            viz_dict - dictionary containing ranked counts
                this dictionary can for example be the count of songs per Artist, Genre, Title
                listened to for multiple years
                ex:
                    {2016: {'Soundtrack': 2535, 'Pop': 1145, 'French Pop': 955, 'Classical': 779, 'Rock': 503},
                    2017: {'Soundtrack': 888, 'Pop': 850, 'Classical': 458, 'French Pop': 346, 'Alternative': 312},
                    2018: {'Pop': 1304, 'French Pop': 977, 'Soundtrack': 761, 'Rock': 344, 'Alternative': 335},
                    2019: {'French Pop': 1265, 'Pop': 1175, 'Soundtrack': 594, 'Dance': 581, 'Rock': 325},
                    2020: {'Pop': 571, 'Soundtrack': 504, 'French Pop': 504, 'Dance': 238, 'Classical': 229}}
                This dictionary can be obtained using the build_ranking_dict_per_year method from the Process.TrackSummaryObject class 
            center_title - OPTIONAL, the title to display in the center of the plot

        Methods:
            __init__(viz_dict, center_title='')
            build_sunburst_arrays()
            render_sunburst_plot()

        Example:
            #build the viz_dict
            ranking_dict = df_viz.track_summary_objects.build_ranking_dict_per_year(df_viz.get_df_viz(), 'Genres')
            #create the sunburst instance
            sunburst = SunburstVisualization(ranking_dict, 'Genre')
            #render the plot
            sunburst.render_sunburst_plot()
    '''

    def __init__(self, viz_dict, center_title=''):
        self.viz_dict = viz_dict
        self.center_title = center_title
        self.plot_title = 'Ranking across years: ' + self.center_title
        self.labels = []
        self.parents = []
        self.values = []
        self.ids = []
        self.build_sunburst_arrays()

    def build_sunburst_arrays(self):
        '''
            In order to build the sunburst, we first build a few arrays used by Plotly.
            labels - each portion of the sunburst that should be rendered
            parents - used to keep track of the relationship between each portion on the graph
            values - the proportion of each portion of the plot
            ids - used to have the same parent repeated multiple times

            More specifically, we have the year as a parent and ids, the genre/artist/title as a label
            and the count of songs listened to from the input dictionary as a value.
        '''
        labels = []
        parents = []
        values = []
        ids = []
        for year in self.viz_dict.keys():
            current_index = len(labels)
            ids.append(str(year))
            labels.append(str(year))
            parents.append(self.center_title)
            total_count = 0
            for genre in self.viz_dict[year].keys():
                ids.append(str(year)+' - '+genre)
                labels.append(genre)
                parents.append(str(year))
                values.append(self.viz_dict[year][genre])
                total_count += self.viz_dict[year][genre]
            values.insert(current_index, total_count)

        self.labels = labels
        self.parents = parents
        self.values = values
        self.ids = ids

    def render_sunburst_plot(self):
        # Create the figure
        fig =go.Figure(go.Sunburst(
            ids=self.ids,
            labels=self.labels,
            parents=self.parents,
            values=self.values,
            branchvalues="total",
            insidetextorientation='radial'
        ))
        # Update layout for tight margin
        fig.update_layout(
            title = self.plot_title,
            margin = dict(l=0, r=0, b=0)
        )

        fig.show()


class RankingListVisualization():

    '''
        This class is responsible for building an ordered ranking dict of count of tracks of a given number of items.
        To access the output object, it is necessary to call the get_ranked_dict method. 

        Args: 
            viz_dict - dictionary containing ranked counts
                this dictionary can for example be the count of songs per Artist, Genre, Title
                listened to for multiple years
                ex:
                    {2016: {'Soundtrack': 2535, 'Pop': 1145, 'French Pop': 955, 'Classical': 779, 'Rock': 503},
                    2017: {'Soundtrack': 888, 'Pop': 850, 'Classical': 458, 'French Pop': 346, 'Alternative': 312},
                    2018: {'Pop': 1304, 'French Pop': 977, 'Soundtrack': 761, 'Rock': 344, 'Alternative': 335},
                    2019: {'French Pop': 1265, 'Pop': 1175, 'Soundtrack': 594, 'Dance': 581, 'Rock': 325},
                    2020: {'Pop': 571, 'Soundtrack': 504, 'French Pop': 504, 'Dance': 238, 'Classical': 229}}
                This dictionary can be obtained using the build_ranking_dict_per_year method from the Process.TrackSummaryObject class 
            number_of_items_in_ranking - by default set to 10, the number of items we want to be in the ranked dict

        Methods:
            __init__(viz_dict, number_of_items_in_ranking=10)
            rank_items_in_dict()
            get_ranked_dict(print_output=False)

        Example:
            #build the viz_dict
            ranking_dict = df_viz.track_summary_objects.build_ranking_dict_per_year(df, 'Genres')
            #create the RankingList instance with 3 items
            ranking = RankingListVisualization(ranking_dict, 3)
            #get the ranked output and print it
            ranking.get_ranked_dict(print_output=True)
            ## returns something like this : 
                {2016: {'Soundtrack': 2535, 'Pop': 1145, 'French Pop': 955},
                2017: {'Soundtrack': 888, 'Pop': 850, 'Classical': 458},
                2018: {'Pop': 1304, 'French Pop': 977, 'Soundtrack': 761},
                2019: {'French Pop': 1265, 'Pop': 1175, 'Soundtrack': 594},
                2020: {'Pop': 571, 'Soundtrack': 504, 'French Pop': 504}}
    '''

    def __init__(self, viz_dict, number_of_items_in_ranking=10):
        self.viz_dict = viz_dict
        self.num_ranks = number_of_items_in_ranking
        self.ranked_dict = self.rank_items_in_dict()

    def rank_items_in_dict(self):
        ranked_dict = {}
        for year in self.viz_dict.keys():
            ranked_dict[year] = {key: self.viz_dict[year][key] for key in sorted(self.viz_dict[year], key=self.viz_dict[year].get, reverse=True)[:self.num_ranks]}

        return ranked_dict

    def get_ranked_dict(self, print_output=False):
        if print_output is True:
            print(self.ranked_dict)
        return self.ranked_dict


class HeatMapVisualization():

    '''
        This class is responsible for generating a 2D histogram, heatmap like, graph from
        the objects contained in a dictionary. 
        It is meant to display the time of listening:
            - per day of the month (month on x-axis, and day of the month (DOM) on y-axis)
            - per day of the week (DOW - week day on x-axis, and hour of the day (HOD) on y-axis)
        Note that the time listening will be summed up in each cell if the combination month/DOM or DOW/HOD
        appears multiple times in the input dataframe. 
        It is possible to plot multiple subplots, for example one per year for combination month/DOM, or one
        per month for combination DOW/HOD. The filter should be done on the input dictionary (i.e. render the
        individual plots using different input dictionaries).
        To display the rendered plot, it is necessary to call the .show() method of Plotly. See example below.

        Args: 
            ------ For the instance
            df_viz - dataframe used to calculate the listening time for the target period represented
                This dataframe is an object of the VisualizationDataframe (parsed and processed df). 
            with_subplots - by default set to 1, and in this case, only one plot is rendered
            
            ------ For the methods
            title - string used to identify the subplot, for example, the year plotted, or the month
            type - whether it is a DOM or a DOW plot, i.e. month on x-axis, and day of the month (DOM) on y-axis, or
            week day on x-axis, and hour of the day (HOD) on y-axis

        Methods:
            __init__(df_viz, with_subplots=1)
            build_day_heat_map(title)
            build_week_heat_map(title)
            update_figure_info()

        Example - single plot:
            # get the filtered input df
            query_params = {
                 'year':[2018],
            }
            filtered_df = QueryFactory().create_query(df_viz.get_df_viz(), query_params)
            # create the HeatMap instance
            heat_map = HeatMapVisualization(filtered_df.filtered_df)
            # generate the plot
            heat_map.render_heat_map('DOW', '2018')
            # display the plot rendered
            heat_map.figure.show()

        Example - multiple subplots:
            query_params = {
                'year':[2017, 2018, 2019],
                'rating':['LOVE']
            }

            # create the HeatMap instance
            heat_map = HeatMapVisualization(df_viz.get_df_viz(), 3)

            # for each year, get a filtered dataframe, and generate the subplots
            for year in query_params['year']:
              year_query_params = query_params
              year_query_params['year'] = [year]
              filtered_df = QueryFactory().create_query(df_viz.get_df_viz(), query_params)
              heat_map.df = filtered_df.filtered_df
              heat_map.render_heat_map('DOM', str(year))

            # display the plot rendered
            heat_map.figure.show()
    '''

    def __init__(self, df_viz, with_subplots=1):
        self.df = df_viz
        self.with_subplots = with_subplots
        self.title = 'Heat map of the play duration in minutes for each day'
        self.figure = make_subplots(rows=self.with_subplots, cols=1)
        self.height = 0
        self.row = 1
        self.data = None
        self.xaxis = None

    def build_day_heat_map(self, title):
        '''
            This function is in charge of building a single 2D Histogram trace specifically 
            for a DOM plot, i.e. month on x-axis, and day of the month (DOM) on y-axis.
        '''
        hist = go.Histogram2d(
            y=self.df['Play_DOM'],
            x=self.df['Play_Month'],
            autobiny=False,
            ybins=dict(start=1.5, end=31.5, size=1),
            autobinx=False,
            xbins=dict(start=0.5, end=12.5, size=1),
            z=self.df['Play_duration_in_minutes'],
            histfunc="sum",
            hovertemplate=
            "<b>%{y} %{x}</b><b> "+title+"<b><br>" +
            "Time listening: %{z:,.0f} minutes<br>" +
            "<extra></extra>",
            coloraxis="coloraxis"
        )
        self.data = hist
       
    def build_week_heat_map(self, title):
        '''
            This function is in charge of building a single 2D Histogram trace specifically 
            for a DOW plot, i.e. week day on x-axis, and hour of the day (HOD) on y-axis.
        '''
        hist = go.Histogram2d(
            y=self.df['Play_HOD'],
            x=self.df['Play_DOW'],
            ybins=dict(start=0.5, end=23.5, size=1),
            z=self.df['Play_duration_in_minutes'],
            histfunc="sum",
            hovertemplate=
            title +" - %{x}s, %{y}h<b><br>" +
            "Time listening: %{z:,.0f} minutes<br>" +
            "<extra></extra>",
            coloraxis="coloraxis"
        )
        self.data = hist 

    def render_heat_map(self, type, title):
        if type == 'DOM':
            self.build_day_heat_map(title)
            self.xaxis = dict(tickangle = -45, tickmode = 'array', tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                ticktext = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
        elif type == 'DOW':
            self.build_week_heat_map(title)
            self.xaxis = dict(tickangle = -45, categoryorder='array', categoryarray = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

        self.figure.add_trace(self.data, row = self.row, col=1)
        self.height += 500
        self.update_figure_info()
        self.row +=1

    def update_figure_info(self):
        self.figure.update_xaxes(self.xaxis)
        self.figure.update_yaxes(autorange="reversed")

        self.figure.update_layout(
            title=self.title,
            height = self.height,
            coloraxis=dict(colorscale='hot'),
            showlegend=False,
        )
        self.figure.update_xaxes(matches='x')


class BarChartVisualization():

    '''
        This class is responsible for generating a bar chart from the objects contained in a dataframe. 
        It is meant to display eith the count of tracks or the percentage of tracks listened to:
            - per month
            - per day of the month (DOM)
            - per day of the week (DOW)
            - per hour of the day (HOD)
        Note that the count/percentage will be summed up in each bar if the period targeted appears multiple times
        in the input dataframe. 
        It is possible to plot multiple subplots, for example one per year, or one per month, or one per day... the filter
        should be done on the input dictionary (i.e. render the individual plots using different input dataframes).
        To display the rendered plot, it is necessary to call the .show() method of Plotly. See example below.

        Args: 
            ------ For the instance
            df_viz - dataframe used to calculate the listening time for the target period represented
                This dataframe is an object of the VisualizationDataframe (parsed and processed df). 
            with_subplots - by default set to 0, and in this case, only one plot is rendered
            
            ------ For the methods
            x_serie - the period targeted (month, DOM, DOW, HOD)
            y_serie - either the count of song, or the percentage of songs
            name - useful in particular for the subplot, for example, the year plotted

        Methods:
            __init__(df_viz, with_subplots=0)
            create_figure()
            build_bar_chart(x_serie, y_serie, name)
            render_bar_chart(x_serie, y_serie, name)

        Example - single plot:
            # get the input df 
            df = df_viz.get_df_viz()
            df = df[df['Play_Year']==2020]
            # create the BarChart instance
            bar_chart = BarChartVisualization(df)
            # render the plot
            x_serie = df['Play_HOD'].unique()
            y_serie = df['Play_HOD'].value_counts()
            bar_chart.render_bar_chart(x_serie, y_serie, '2020')
            # display the rendered plot
            bar_chart.figure.show()

        Example - multiple subplots:
            # get the input df 
            df = df_viz.get_df_viz()
            years_to_plot = sorted(df['Play_Year'].dropna().unique())
            # create the BarChart instance
            bar_chart = BarChartVisualization(df)
            bar_chart.hover_unit = '%'

            # for each year, build the x and y series, computing the percentage of songs, and generate the subplots
            for year in years_to_plot:
                x_serie = df[df['Play_Year']==year]['Play_DOW'].unique()
                y_serie = Utility.compute_ratio_songs(df[df['Play_Year']==year]['Play_DOW'])
                bar_chart.render_bar_chart(x_serie, y_serie, str(year))

            # edit the layout of the xaxis and show the rendered plot
            xaxis=dict(categoryorder='array',
                        tickangle = -45,
                        categoryarray = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

            bar_chart.figure.update_layout(xaxis =xaxis)
            bar_chart.figure.show()


        Example - multiple series on same plot:
            # get the input df 
            df = df_viz.get_df_viz()
            years_to_plot = sorted(df['Play_Year'].dropna().unique())
            # create the BarChart instance
            bar_chart = BarChartVisualization(df)
            bar_chart.title='Ratio of tracks skipped, versus listened to completely, per year'
            bar_chart.hover_unit = '%'

            df_track_complete = df[df['Played_completely']==True]
            df_track_partial = df[df['Played_completely']==False]
            y_complete = []
            y_partial = []

            # for each year, build the x and y series, computing the percentage of songs
            for year in years_to_plot:
                count_tracks_complete = df_track_complete[df_track_complete['Play_Year']==year].shape[0]
                count_tracks_partial = df_track_partial[df_track_partial['Play_Year']==year].shape[0]
                percent_tracks_complete = 100*count_tracks_complete/df[df['Play_Year']==year].shape[0]
                percent_tracks_partial = 100*count_tracks_partial/df[df['Play_Year']==year].shape[0]
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
    '''

    def __init__(self, df_viz, with_subplots=0):
        self.df = df_viz
        self.with_subplots = with_subplots
        self.title = 'Distribution of tracks'
        self.figure = self.create_figure()
        self.hover_unit = ''
        self.height = 500
        self.row = 1
        self.data = None

    def create_figure(self):
        '''
            This method is in charge of creating a plotly figure, according to
            whether we want subplots or not (different Plotly function called).
        '''
        if self.with_subplots == 0:
            return go.Figure()
        else:
            return make_subplots(rows=self.with_subplots, cols=1)


    def build_bar_chart(self, x_serie, y_serie, name):
        '''
            This function is in charge of building a bar chart trace.
        '''
        bar = go.Bar(
            name=name,
            x=x_serie,
            y=y_serie,
            hovertemplate=
            "<b>{0}</b><br>".format(name) +
            "<b>%{x}</b><br>" +
            "%{y:,.0f}" + "{0}<br>".format(self.hover_unit) +
            "<extra></extra>"
            )

        self.data = bar


    def render_bar_chart(self, x_serie, y_serie, name):
        self.build_bar_chart(x_serie, y_serie, name)

        if self.with_subplots == 0:
            self.figure.add_trace(self.data)
        else:
            self.figure.add_trace(self.data, row = self.row, col=1)
            self.height += 500
        self.update_figure_info()
        self.row +=1


    def update_figure_info(self):
        self.figure.update_layout(
            title=self.title,
            height = self.height,
        )

class PieChartVisualization():

    '''
        This class is responsible for generating a pie chart from a serie. 
        To display the rendered plot, it is necessary to call the .show() method of Plotly. See example below.

        Args: 
            serie_to_plot - the serie that will be used to populate the pie chart

        Methods:
            __init__(serie_to_plot)
            build_pie()
            render_pie_chart()
            update_figure_info()

        Example:
            # create the PieChart instance
            pie_chart = PieChartVisualization(df_viz.get_library_activity_df()['Transaction Agent Model'])
            # render the plot
            pie_chart.render_pie_chart()
            # display the rendered plot
            pie_chart.figure.show()

    '''
    
    def __init__(self, serie_to_plot):
        self.serie_to_plot = serie_to_plot
        self.title = 'Pie chart'
        self.figure = go.Figure()
        self.height = 500
        self.data = None

    def build_pie(self):
        '''
            This function is in charge of building a pie chart.
        '''
        labels = self.serie_to_plot.value_counts().index.tolist()
        values = self.serie_to_plot.value_counts()
        
        pie = go.Pie(labels=labels, values=values, textinfo='label+percent')
        self.data = pie

    def render_pie_chart(self):
        self.build_pie()
        self.figure.add_trace(self.data)
        self.update_figure_info()

    def update_figure_info(self):
        self.figure.update_layout(
            title=self.title,
            height = self.height,
            showlegend=False,
        )


