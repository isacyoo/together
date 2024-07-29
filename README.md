# Football data dashboard

This is a simple web application that displays football match data of 11 different European football leagues between 2008/2009 season and 2015/2016 season.

## How to run the application

### Dataset
The dataset is available at [Kaggle](https://www.kaggle.com/hugomathien/soccer/data). Download the dataset and place it in the root directory of the project. Use the same name as the original file `database.sqlite`.

### Environment
This project uses Python 3.11, but it should work with any Python >= 3.8. Simply run the following commands to create a virtual environment and install the dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the application
To run the application, simply run the following command:

```bash
python app.py
```