apple_music_analyser package - basics
=======================================


Purpose of this package
-----------------------

This package is designed to assist users of the Apple Music service with the processing of their raw data, in order to perform analysis.
This package is composed of two main blocks:
- a module that parses and processes the data into a clean dataframe, ready to be analysed
- a module that relies on Plotly to simply render various types of plots based on the clean dataframe

More specifically, it allows you to:
- input the .zip archive Apple provides upon request (see Apple’s Data and Privacy page)
- create a clean dataframe that contains all your play activity, and as much information as possible regarding each track (genre, rating, skipped,...)
- either from there on be able to manipulate this pandas dataframe on your own, or plot insightful visualizations to learn more about the data


Requirements
------------

The code is written in Python 3.7.

There are several dependencies for this package. The versions provided here are those used for testing.

- difflib (python standard library)
- numpy 1.18.4
- pandas 1.0.4
- pickle (python standard library)
- plotly 4.8.1
- unittest (python standard library)
- zipfile (python standard library)


Installation
------------

To install the package:

```
pip install apple-music-analyser
```

It relies in particular on two libraries: Pandas and Plotly.
The setup.py file lists all dependencies.


Tutorial
---------

A brief introduction on how to use this package and a demo are available on [Medium](https://medium.com/@mozart38).


Code documentation
------------------

This package is composed of a total of 7 modules
- VisualizationDataframe
- Parser
- Process
- Track
- Query
- Utility
- DataVisualization

Each module's code is documented. For you to easily get access to the help, simply use the help built-in method.
For example, from the python interpreter:

```
import apple_music_analyser.Utility
help(apple_music_analyser.Utility)
```

This will print both the docstring of the Utility class, as well as all the methods defined in this class and their docstring.
For more details on the structure of the code, please take a look at the docs folder in the [GitHub repository](https://github.com/acoullandreau/apple_dashboard)!


Test functions
-----------------







There is a total of 37 tests available, that should cover most of the classes and methods available. 


| Name 		   | Stmts | Miss | Cover | Missing         |
| ------------ | ----- | ---- | ----- | --------------- |
| classfile.py | 214   |  10  |  95%  | 20-28, 155-156  |
| utility.py   | 33    |   0  |  100% |                 |

Note: tests can be executed using the following command from the geo_rendering main directory (where the setup.py file is stored!)

```
python setup.py test
```


Further work and improvements
-----------------------------

Some improvements that could be performed on the package:

- convert id should not go beyond 0
- handle errors if points in calculate_boundaries are not lists of tuples (it doesn't make sense otherwise)
- handle errors if points in calculate_centroid are not lists of tuples (it doesn't make sense otherwise)
- handle errors if points to render on map is not a list of coordinates (type POLYGON)
- format of input for interpolate_next_position
- in general, handle better errors related to the format of an input


Sources, acknowlegments and related content
-------------------------------------------

This work is inspired from a data visualisation project about the NYC taxi rides ([link to the repository of the project](https://github.com/acoullandreau/nyc_taxi_trips))
