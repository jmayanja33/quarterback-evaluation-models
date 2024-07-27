# Predicting NCAA Quarterback Success in the National Football League

## Description

The National Football League is a multi-billion dollar enterprise, with millions of fans all over the world.
Every Sunday from September to January, these fans watch their teams, some cheering on a Super Bowl
contender, and others suffering through a losing season. For many in the latter, looking forward to the
annual NFL draft in April is much more exciting than the current games, as their team will likely have a
high pick, and the chance to select a franchise changing player. Oftentimes, the players selected at the top
of the draft are Quarterbacks, as they are the leader of a team’s offense.

Finding a quarterback that can become a franchise changing player has actually proven to be a very
challenging task. Since 1970, over 500 quarterbacks have been selected, and the probability that one becomes
a First Team All-Pro selection is just 4.6%. This probability rises to 9.4% for quarterbacks in the first round,
and 11.9% for quarterbacks drafted in the Top 5.

Undertaken for a graduate school project in the Georgia Tech Master's of Analytics program, This project aims to enhance
the current quarterback evaluation methods through the use of machine learning. The main objective of the project was to
project how well a quarterback would transition from the NCAA to the NFL by classifying
each NCAA quarterback drafted into the NFL into one of 6 tiers:

* Hall of Fame QB
* Elite Mobile QB
* Elite Pocket Passer
* Starting QB
* Backup QB
* Practice Squad Member

Additionally, 4 additional models were created to predict the number of First Team All-Pro selections, Years as a Starter,
and Pro Bowl Selections. A fifth model was attempted for Weighted Career Approximate Value, but this model was
too unstable to provide reliable results. View accuracy metrics for each below.

* Quarterback Tier: 
  * Accuracy: 0.7105
  * R-squared: -0.1737
  * Adj. R-squared: -0.6084

* First Team All-Pro Selections: 
  * RMSE: 0.0931
  * R-squared: 0
  * Adj. R-squared: 0.3704

* Years as a Starter: 
  * RMSE: 3.0273
  * R-squared: 0.0287
  * Adj. R-squared: -0.3310

* Pro Bowl Selections: 
  * RMSE: 1.3363
  * R-squared: 0.1244
  * Adj. R-squared: -0.1999

All NFL data for this project was scraped from Pro Football Reference (https://www.pro-football-reference.com/) and all
NCAA football data scraped from SRCFB (https://www.sports-reference.com/cfb/). All combine data was scraped from 
NFL Combine Results (https://nflcombineresults.com/). See the sections below for code descriptions of each directory 
in the repository. See the paper in `Reports/Group_097_Final_Project_Report.pdf` for a full description of the methods and results.

## Requirements

* Python 3.10.x
* All libraries in the `requirements.txt` file
* An internet connection will be needed if running any code from the `Scrapers` directory.

## Code

### Cleaners

This directory holds all code to clean data after it has been scraped.

* Run `initial_clean_main.py` immediately after scraping the data. This will filter out all quarterbacks with missing data from the data collected.
* Run `final_clean_main.py` immediately after clustering the data. This will assign every data point from the `Data/cleaned_ncaa_drafted_qbs.csv` file
with the correct dependent variables. It will save the results to `Data/cleaned_clustered_ncaa_drafted_qbs.csv`.
* Run `split_data.py` to split the data into a training and test set. 85% of the data will be allocated to the training set,
and the remaining 15% to the test set. The Data will be saved in the `Data/TrainingData` folder, with a directory for
each dependent variable holding the 2 split datasets for each (the datasets all have the same data points, just 
different dependent variables). Additionally, a dataset called `young_qb_test_data.csv` will be created in each of these 
directories, which holds data for all quarterbacks drafted in the 2023 and 2024 classes as live test data.

### Data

This directory holds all the data collected and used in this project. 

* `ClusterPlots` and `ClusterResults` hold all csv files and plots of clustering results.
* `Multicollinearity` holds all csv files used to review and eliminate multicollinearity in the data.
* `Predictions` holds all predictions and player comparisons made by the models created in this project.
* `TrainingData` holds all data used to train models and evaluate model performance.
* `cleaned_clustered_ncaa_drafted_qbs.csv` is the full data set that was used to create the training and test sets.
It was built from `cleaned_ncaa_drafted_qbs.csv`.
* `ncaa_drafted_qbs.csv` and `nfl_draft_qbs.csv` is the raw data that was scraped from the internet.

### EDA

This folder holds all scripts used to explore clustering and multicollinearity. The data used in this section is all
from `Data/cleaned_clustered_ncaa_drafted_qbs.csv`.

* Run `main.py` to cluster the data using HDBSCAN and K-Means. Results will be stored in `Data/ClusterPlots` and `Data/ClusterResults`.
The script uses K-Means and HDBSCAN objects to cluster, which are located in `kmeans.py` and `hdbscan.py`.
* Run `multicollinearity.py` to get VIF scores and eliminate multicollinearity from the data. Results will be stored in
`Data/Multicollinearity`.

### Helpers

This directory holds a helper file `helpers.py` which holds utility functions to automate tasks such as making directories.

### Logs

This directory holds a Logger object, which writes logs to the console and to an output log file.

### Models

This directory holds all models and all code needed to train them. `model.py` is a base model class, off of which
5 model types were built:

  * Artificial Neural Network (ANN)
  * K-Nearest Neighbors (KNN)
  * Random Forest
  * Support Vector Machines (SVM)
  * XGBoost

All code for each model type is held in the corresponding directory. Each will have a `.py` file named after it which
holds the model object. Run the `main.py` in each of the model's folders to train each of the respective models on all
5 dependent variables. Training results will be held in the `Results` folder, and the model object will be stored as 
`model.pkl` or `model.keras`, depending on the model type.

* Note that all models will be trained with 5-fold cross validation and a grid search to tune hyperparameters, except for
the neural networks and the SVM models due to computational complexity.

* Also note that issues may arise running XGBoost on MacOS with an M-Series chip. The issues seem to stem from the pip
installation, with the library unable to find some installed files. It is recommended to use a Windows system if running
any of the XGBoost models.

### Predictors

This directory holds all code to make predictions on the quarterbacks from the 2023 and 2024 NFL draft classes
(`Data/TrainingData/$DependentVaraible/young_qb_test_data.csv`) using the best model identified in training. The best
models are identified in a python dictionary in `Data/columns.py`. 

Run `main.py` to make predictions for all dependent variables, using the best model for each. This script will also
find the most similar college quarterbacks for each quarterback in the live test data, as well as storing the probabilities
of each quarterback developing into each tier in the NFL. All code need to make predictions is in `predictor.py`, and all
results are saved in `Data/Predictions`.

### Reports

This directory holds all reports written for the project. `Group_097_Progress_Report.pdf`, is the progress report submitted
halfway through the semester, and `Group_097_Final_Project_Report.pdf` is the final report.

### Scrapers

This directory holds all code used to scrape the data needed for this project from the internet. 
`scrpaer.py` holds a scraper object, from which three more scrapers were built:

* `combine_scraper.py` holds a scraper object to collect NFL combine data for quarterbacks.
* `ncaa_scraper.py` holds a scraper object to collect NCAA statistics for quarterbacks.
* `nfl_scraper.py` holds a scraper object to collect NFL statistics for all quarterbacks drafted into the league.

Run `main.py` to collect all NFL, NCAA, and NFL combine data for all quarterbacks drafted into the NFL between 2000 and 2024
(the years can be configured when initializing the NFL scraper). All results are stored in 
`Data/ncaa_drafted_qbs.csv` and `Data/nfl_draft_qbs.csv`.
