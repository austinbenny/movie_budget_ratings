import pandas as pd



df2=pd.read_csv('/Users/austinbenny/Documents/python/movie_budget_ratings/IMDB_data/imdb_data_final.csv')
df3=pd.read_csv('smart_title.csv')
df2['title']=df3
df2.drop(df2.columns[0],axis=1,inplace=True)
df2.to_csv('/Users/austinbenny/Documents/python/movie_budget_ratings/IMDB_data/imdb_data_final_v2.csv',index=False)
