import pandas as pd


def read(path):
    df=pd.read_csv(path)
    return df

lst=['imdb_data_10K.csv','imdb_data_20K.csv','imdb_data_30K.csv','imdb_data_40K.csv','imdb_data_50K.csv']

df=pd.DataFrame()

for s in lst:
    df=df.append(read(s))

df.reset_index(drop=True, inplace=True)
df.drop(df.columns[0],axis=1,inplace=True)
df.to_csv('imdb_data_final.csv')
