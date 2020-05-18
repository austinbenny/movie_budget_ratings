import imdb
import pandas as pd
import numpy as np
import time
import multiprocessing as mp


def get_info(index):

    '''mulitprocess designed function to get data for each index (movie)'''

    with open(text_path,'a') as file:

        try:

            size=len(inputs)
            row=[np.nan]*size

            try:
                current_movie=ia.get_movie(imdb_id[index])
            except:
                file.write('\n  --------------- (INVALID) Check ID = {} --------------- '.format(imdb_id[index]))
                return row

            print('Index = {}'.format(index))
            if (current_movie.get('aspect ratio')==None or current_movie.get('box office')==None or len(current_movie.get('box office'))<3 or current_movie['box office'].get('Opening Weekend United States')==None):

                file.write('\n Index = {}, Not enough information for = {}'.format(index, title[index]))
                return row

            else:

                col=0
                chars_remove='$,'
                for wants in inputs:

                    if wants =='Budget':
                        budget = current_movie['box office'][wants]
                        budget=budget.split(' ', 1)[0]
                        for character in chars_remove:
                            budget = budget.replace(character, '')
                        row[col]=float(budget)

                    elif wants == 'Cumulative Worldwide Gross':
                        gross = current_movie['box office'][wants]
                        gross=gross.split(' ', 1)[0]
                        for character in chars_remove:
                            gross = gross.replace(character, '')
                        row[col]=float(gross)

                    elif wants == 'Opening Weekend United States':
                        opening=current_movie['box office'][wants]
                        opening=opening.split(' ', 1)[0]
                        for character in chars_remove:
                            opening = opening.replace(character, '')
                        row[col]=float(opening)

                    elif wants == 'runtimes':
                        row[col]=current_movie[wants][0]

                    elif wants == 'title':
                        row[col]=title[index]

                    elif wants == 'aspect ratio':
                        row[col]=current_movie[wants].split(' ',1)[0]

                    else:
                        row[col]=current_movie[wants]

                    col+=1      

                return row

        except KeyError:
            print("-------------- KeyError, index = {}, check movie  = {} ---------------".format(index,imdb_id[index]))
            return row
        except ValueError:
            print("------------ ValueError (maybe a nan?), check index = {} -------------".format(index))
            return row
        except:
            print("------------ something else went wrong, check index = {} -------------".format(index))
            return row



def massage_df(path):
    df=pd.read_csv(path)
    # replace nan and inf
    df.replace([np.inf, -np.inf], np.nan)
    df=df.dropna()
    # reset the index
    df.reset_index(drop=True, inplace=True)
    return df


if __name__ == "__main__":

    # paths
    path = '/Users/austinbenny/Documents/python/movie_budget_ratings/IMDB_data/essential_imdb.csv'
    text_path = '/Users/austinbenny/Documents/python/movie_budget_ratings/IMDB_data/output_imdb.txt'
    csv_path='/Users/austinbenny/Documents/python/movie_budget_ratings/IMDB_data/imdb_data_50K.csv'
    
    # making text file
    file=open(text_path,'w')
    file.write('File for mp_get_data.py | Contains movies not included in csv \n')
    file.close()

    df=massage_df(path)

    global imdb_id
    imdb_id=[df.loc[s,'imdb_id'].replace('tt','') for s in range(len(df))]
    global title
    title=df.loc[:,'title']
    global inputs
    inputs=['title','Cumulative Worldwide Gross','Budget','Opening Weekend United States','rating','runtimes','votes','aspect ratio']
    global ia
    ia=imdb.IMDb(accessSystem='http',reraiseExceptions=True)

    sub=range(40000,len(imdb_id))
    #sub=range(30001,40000)

    start_time = time.time()
    pool = mp.Pool(processes=mp.cpu_count())
    data=pool.map(get_info, sub)
    end_time = time.time()

    duration=end_time-start_time

    # massage new df
    df=pd.DataFrame.from_records(data)
    df=df.dropna()
    df.reset_index(drop=True, inplace=True)
    df.columns=inputs
    df.to_csv(csv_path,index=True)

    shape=df.shape
    with open(text_path,'a') as file:
        file.write('\n\n Processors ran on = {}'.format(mp.cpu_count()))
        file.write('\n Final Shape = {}'.format(shape))
        file.write('\n --------- Duration = {:.3f} secs ---------'.format(duration))
    
    print('Final shape = ',shape)
    print(' --------- Duration = {:.3f} secs ---------'.format(duration))



