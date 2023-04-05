[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/)

# A Car Web Data Project

This is a personal project about the used cars market in Italy.

The data were collected from December 2022 to March 2023 from a large European online car market.
However only offers from Italy were collected.

The project currently includes the following sections:
- Data Acquisition
- Data Analysis
- Serving

## Data Acquisition
This section of the project includes the scripts used to collect the data:
- a **Web Scraper** that collects the data from the market website
- a **Cleaner** script that performs a first stage cleaning and merges the data batches in a single file
- a **Scheduler** script that runs the web scraper hourly

## Data Analysis
A collection of jupyter-notebooks used to:
- Refine the data cleaning
- Explore the data
- Model the data with some Machine Learning models


## Serving
A small web app made in streamlit. You can find:
- a **Dashboard** showing the main metrics and plots about the collected data
- a **Car Evaluator** where you can insert the features of your car (e.g. model, age and power) to obtain a real time estimate of its value.
