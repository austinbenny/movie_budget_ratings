import multiprocessing as mp
import pandas as pd
import numpy as np
import imdb
import time

def get_title(index):

    with open(text_path,'a') as file:

        print('Index = ',index)
        
        final_title=df2.loc[index,'title']
        file.write('\n Title in small DF = {}'.format(final_title))
        row=df.loc[df['title']==final_title].index.tolist()
        file.write('\n Index of movie in large DF = {}'.format(row))

        title_setting='original title'
        if len(row)>1:
            for dupe_idx in row:
                file.write('\n dupe_idx = {}'.format(dupe_idx))
                if float(ia.get_movie(df.loc[dupe_idx,'imdb_id'])['rating']) == df2.loc[index,'rating']:
                    file.write('\n correct dupe_idx = {}, correct movie found = {}'.format(dupe_idx,final_title))#final_title moght be wrong-validate
                    try:
                        return ia.get_movie(df.loc[dupe_idx,'imdb_id'])[title_setting]
                    except:
                        return 'N/A'
        else:
            try:
                return ia.get_movie(df.loc[row,'imdb_id'])[title_setting]
            except:
                return 'N/A' 


source_path = '/Users/austinbenny/Documents/python/movie_budget_ratings/IMDB_data/imdb_data_final.csv'
source_path_2='essential_imdb.csv'
target_path='smart_title.csv'
text_path='titles_output.txt'
with open(text_path,'w+') as file:
    file.write('\n text file for output from get_titles.py \n')


df=pd.read_csv(source_path_2)
df.replace([np.inf, -np.inf], np.nan)
df=df.dropna()
df.reset_index(drop=True, inplace=True)
df['imdb_id']=[df.loc[s,'imdb_id'].replace('tt','') for s in range(len(df))]

df2=pd.read_csv(source_path)
print('Final Index (length of df2) = {}'.format(len(df2)))
ia=imdb.IMDb()

sub=range(0,len(df2))
start_t=time.time()
pool = mp.Pool(processes=mp.cpu_count())
titles=pool.map(get_title, sub)
print('Duration = {}'.format(time.time()-start_t))

df3=pd.DataFrame({'smart title':titles})
df3.to_csv(target_path,index=False)
length_none=len(df3.loc[df3['smart title']=='N/A'].index.tolist())
print('Number of N/A (hopefully 0) = {}'.format(length_none))
df2['title']=df3
df2.drop(df2.columns[0],inplace=True)
df2.to_csv('/Users/austinbenny/Documents/python/movie_budget_ratings/IMDB_data/imdb_data_final_v2.csv',index=False)

