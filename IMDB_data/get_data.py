from imdb import IMDb
import pandas as pd
import numpy as np
import time
import sys



path = '/Users/austinbenny/Documents/python/movie_budget_ratings/IMDB_data/essential_imdb.csv'
text_path = '/Users/austinbenny/Documents/python/movie_budget_ratings/IMDB_data/output_imdb.txt'
csv_path='/Users/austinbenny/Documents/python/movie_budget_ratings/IMDB_data/imdb_data.csv'

file = open(text_path,'w+')

df=pd.read_csv(path)
# replace nan and inf
df.replace([np.inf, -np.inf], np.nan)
df=df.dropna()
# reset the index
df.reset_index(drop=True, inplace=True)
# remove tt and extract into lists
imdb_id=[df.loc[s,'imdb_id'].replace('tt','') for s in range(len(df))]
title=df.loc[:,'title']



ia=IMDb()
inputs=['title','Cumulative Worldwide Gross','Budget','Opening Weekend United States','rating','runtimes','votes','aspect ratio']
size=len(inputs)


index=0 # keeps track of original index used from old lists
df=pd.DataFrame()

start_time = time.time()

try:
    final_len=6
    for movie in imdb_id[0:final_len]:
    #for movie in imdb_id:

        current_movie=ia.get_movie(movie)
        #print('current movie index=',index)
        #print('Current movie=',current_movie)
        #file.write('\n Index = {}'.format(index))
        print('Index = {}'.format(index))


        row_act=0
        if (ia.get_movie(movie).get('box office')==None) or (len(current_movie.get('box office'))<3) or (ia.get_movie(movie)['box office'].get('Opening Weekend United States')==None):

            file.write('\n Not enough info for = {}'.format(title[index]))
            col+=1

        else:

            row=[0]*size # preallocate row
            #print('row before=',row)
            col=0 # index=column
            #print('column=',inputs[col])

            for wants in inputs:

                if wants =='Budget':

                    budget = current_movie['box office'][wants]
                    budget=budget.split(' ', 1)[0]
                    chars_remove='$,'
                    for character in chars_remove:
                        budget = budget.replace(character, '')
                    row[col]=float(budget)

                elif wants == 'Cumulative Worldwide Gross':
                    gross = current_movie['box office'][wants]
                    gross=gross.split(' ', 1)[0]
                    chars_remove='$,'
                    for character in chars_remove:
                        gross = gross.replace(character, '')
                    row[col]=float(gross)

                elif wants == 'Opening Weekend United States':

                    opening=current_movie['box office'][wants]
                    opening=opening.split(' ', 1)[0]
                    chars_remove='$,'
                    for character in chars_remove:
                        opening = opening.replace(character, '')
                    row[col]=float(opening)

                elif wants == 'runtimes':
                    row[col]=current_movie[wants][0]

                elif wants == 'title':
                    row[col]=title[index]

                else:
                    row[col]=current_movie[wants]

                col+=1

            # check if happens after for loop wants
            #print('row=',row)
            df.insert(row_act, imdb_id[index],row,True)
            row_act+=1 

        # end of for loop
        index+=1

except OSError as err:
    file.write('\n Index of error = {}'.format(index))
    file.write('\n Type of error = {}'.format(err))

file.write('\n\n --------- Completed successfully in {:.3f} seconds --------- '.format((time.time() - start_time)))

df.index=inputs
df=df.T
df.index.name='imdb_id'

df.to_csv(csv_path,index=True)



file.close()