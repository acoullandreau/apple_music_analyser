from setuptools import setup

setup(
    name="apple_music_analyser",
    version="0.1.1",
    description="Data wrangling and processing for visualization of the usage of the Apple Music service",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/acoullandreau/apple_dashboard",
    author="Alexina Coullandreau",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization"
    ],
    packages=['apple_music_analyser', 'apple_music_analyser.tests'],
    install_requires=["numpy==1.18.4", "pandas==1.0.4", "plotly==4.8.1"],
    include_package_data=True,
    python_requires='>=3.6',
    test_suite='tests',
    tests_require=['coverage'],
)