import pandas as pd

def preprocess(df, region_df):
    
    # filter out Summer Olympics data
    df = df[df['Season'] == 'Summer']
    
    # merge with regions data
    df = df.merge(region_df, on ='NOC', how='left')

    df.drop_duplicates(inplace=True)
    
    # one hot encode the 'Medal' column
    df = pd.concat([df, pd.get_dummies(df['Medal'], dtype=int)], axis=1)
    return df
