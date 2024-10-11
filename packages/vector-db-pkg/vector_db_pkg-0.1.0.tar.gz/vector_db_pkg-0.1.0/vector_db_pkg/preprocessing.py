import pandas as pd

def preprocess_data(df):
    # Example preprocessing function
    text_column = 'text_column'
    df[text_column] = df[text_column].fillna('').str.lower()
    return df