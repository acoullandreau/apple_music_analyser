# Apple Music Analyser - Python package


Context of this project
------------------------

This apple\_music\_analyser python package project actually started as a much smaller journey. I started using Apple Music in 2016, and when I found out I could request an archive with all my usage data, I decided to dive into the data!

It occured to me, after a few hours wrangling, cleaning, looking from different angles at the data, that it may be useful for other people to be able to dive into their own data without going through the trouble of parsing and processing it all. And just like that, this python package was born!


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

A brief introduction on how to use this package and a demo are available on [Medium](https://medium.com/@mozart38/apple-music-activity-analyser-part-2-3a62c6284eb0).


Code documentation
------------------

This package is composed of a total of 7 modules:

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
For more details on the structure of the code, please take a look at the [documentation](https://github.com/acoullandreau/apple_music_analyser/tree/master/docs)!


Test functions
-----------------

There is a total of 81 tests available, dispatched in multiple test modules (one per package module). As some tests require to have files to parse, I created an archive test_df.zip that contains each required file with an extract of my own real data. This archive has been constructed as to encounter many "corner" cases I hit during the implementation process. Hopefully, it covers the majority of the corner cases one can encounter when using this package.

Here is the coverage report:

| Name | Stmts | Miss | Cover |
| :--- |  ---: | ---: |  ---: |
| apple\_music\_analyser/DataVisualization.py | 130 | 102 | 22% |
| apple\_music\_analyser/Parser.py | 101 | 2 | 98% |
| apple\_music\_analyser/Process.py | 235 | 5 | 98% |
| apple\_music\_analyser/Query.py | 81 | 1 | 99% |
| apple\_music\_analyser/Track.py | 56 | 0 | 100% |
| apple\_music\_analyser/Utility.py | 93 | 11 | 88% |
| apple\_music\_analyser/VisualizationDataframe.py | 60 | 0 | 100% |
| apple\_music\_analyser/\_\_init\_\_.py | 7 | 0 | 100% |
| apple\_music\_analyser/tests/\_\_init\_\_.py  | 0 | 0 | 100% |
| apple\_music\_analyser/tests/test\_Parser.py | 140 | 1 | 99% |
| apple\_music\_analyser/tests/test\_Process.py | 313 | 1 | 99% |
| apple\_music\_analyser/tests/test\_Query.py | 100 | 1 | 99% |
| apple\_music\_analyser/tests/test\_Track.py | 61 | 1 | 98% |
| apple\_music\_analyser/tests/test\_Utils.py | 58 | 1 | 98% |
| apple\_music\_analyser/tests/test\_VisualizationDataframe.py | 93 | 1 | 99% |
| **TOTAL** |  **1528** | **127** |  **92%** |
    

Let's note that the module DataVisualization is barely tested, as it is actually an interface for the user to simply build Plotly visualizations, but this is not the core of the package! Besides, adding tests for theses would actually be pretty equivalent to testing Plotly (and it is obvisouly irrelevant).

If you want to execute the tests, you can simply run the following command from the package main directory (where the setup.py file is stored!):

```
python -m unittest discover -b
```

And if you want to generate the coverage report, ensure that you have the coverage package (```pip install coverage```) installed, and run the following two commands: 

```
coverage run --source=apple_music_analyser -m unittest discover -b
```

```
coverage report -m
```

-m is going to display the missing lines
-b is going to prevent print statements to be displayed on the terminal when running the tests.

And if you want a much more complete report, run the following command and open the index.html file in the coverage_html folder created:

```
coverage html -d coverage_html
```


Further work and improvements
-----------------------------

I hope to be able to gather feedback from users, because having other people's insight on how to improve this package is most probably going to bring up new ideas! So far, I can identify three areas of improvement:

- use a config file to pass the archive path and file structure, and allow the user to personalize more what actions are performed when parsing the input files (which columns to drop, which ones to add...)
- improve efficiency in the parsing and processing of the data (for a few tens of thousands lines, it around 30 seconds.)
- enhance error handling, corner cases

There may be a way also, one day, to build a pipeline to collect data using the Apple Music API to be able to perform the analysis at any moment, not upon requesting the archive to Apple. At the moment, this would imply being able to store the data somewhere...and actually somewhat recreate the database Apple already feeds... 


Sources, acknowlegments and related content
-------------------------------------------

This project actually started as a much smaller journey, a simple exploration of my personal data from the Apple Music service. It occured to me, after a few hours wrangling, cleaning, looking from different angles at the data, that it may be useful for other people to be able to dive into their own data without going through the trouble of parsing and processing it all. And just like that, two projects were born: this python package, and a webpage for anyone to parse/process locally and visualize a set of nice graphs and representation. 

If you want to check out the data analysis process I went through before building this package --> [Exploratory analysis](https://github.com/acoullandreau/apple_dashboard_exploration)

If you want to follow up the progress on the webpage --> [Apple Music Dashboard](https://github.com/acoullandreau/apple_music_dashboard)

