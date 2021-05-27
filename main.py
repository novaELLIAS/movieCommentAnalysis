import pandas as pd


minTotNum = 1000
minFemNum = 200
minMalNum = 200

if __name__ == '__main__':

    u_cols = ['user_id', 'gender', 'age', 'occupation', 'zip']
    users = pd.read_table('data/users.dat', sep='::', header=None, names=u_cols, engine='python')
    r_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
    ratings = pd.read_table('data/ratings.dat', sep='::', header=None, names=r_cols, engine='python')
    m_cols = ['movie_id', 'title', 'genres']
    movies = pd.read_table('data/movies.dat', sep='::', header=None, names=m_cols, engine='python')

    # u_cols = ['user_id', 'age', 'gender', 'occupation', 'zip_code']
    # users = pd.read_csv('data/u.user', sep='|', names=u_cols, encoding="ISO-8859-1")
    # r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
    # ratings = pd.read_csv('data/u.data', sep='\t', names=r_cols, encoding="ISO-8859-1")
    # m_cols = ['movie_id', 'title', 'release_date', 'video_release_date', 'imdb_url']
    # movies = pd.read_csv('data/u.item', sep='|', names=m_cols, usecols=range(5), encoding="ISO-8859-1")

    lens = pd.merge(pd.merge(ratings, users), movies)

    print("-----LENS PRINT:-----")
    print(lens)
    print("---------------------")

    size_by_title = lens.groupby('title').size()
    pre_active_name = size_by_title.index[size_by_title >= minTotNum]

    pre_active_name = list(set(pre_active_name))

    active_filter = lens.groupby('title').gender.value_counts()

    print("-------FILTER:-------")
    print(active_filter)
    print("---------------------")

    active_name = list()
    for title in pre_active_name:
        try:
            if (active_filter[(title, 'F')] > minFemNum) & (active_filter[(title, 'M')] > minMalNum):
                if title not in active_name:
                    active_name.append(title.encode('unicode-escape').decode('unicode-escape'))
        except Exception as e:
            print(e)
            continue

    print("-----ACTIVE_NAME-----")
    print(pd.Series(active_name))
    print("---------------------")

    lens = lens.pivot_table('rating', index='title', columns='gender', aggfunc='mean')
    mean_ratings = lens.loc[active_name]
    mean_ratings['diff'] = mean_ratings['F'] - mean_ratings['M']

    print("-----MEAN_RATING:----")
    print(mean_ratings.head())
    print("---------------------")

    sorted_ratings = mean_ratings.sort_values(by='diff')
    print("------MOST_CONTROVERSIAL::MALE_LIKES------")
    print(sorted_ratings[:10])
    print("---------------------")
    print("-----MOST_CONTROVERSIAL::FEMALE_LIKES-----")
    print(sorted_ratings[::-1][:10])
    print("------------------------------------------")

    mean_ratings['diff'] = abs(mean_ratings['F'] - mean_ratings['M'])
    sorted_ratings = mean_ratings.sort_values(by='diff')
    print("-----------LEAST_CONTROVERSIAL:-----------")
    print(sorted_ratings[:10])
    print("------------------------------------------")
    print("------------MOST_CONTROVERSIAL------------")
    print(sorted_ratings[::-1][:10])
    print("------------------------------------------")