[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/)

# A Cars Web Data Project

This is a personal project about the used cars market in Italy. Its content is for **educational purposes only**.

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
A small web app made in Streamlit. You can find:
- a **Dashboard** showing the main metrics and plots about the collected data
- a **Car Evaluator** where you can insert the features of your car (e.g. model, age and power) to obtain a real time estimate of its value.

<p align="center">
  <img width="500" src="/Screenshots/Dashboard%201.png"> <img width="500"src="/Screenshots/Dashboard%202.png">
</p>
<p align="center">
  <img width="600" src="/Screenshots/Evaluator.png">
</p>
