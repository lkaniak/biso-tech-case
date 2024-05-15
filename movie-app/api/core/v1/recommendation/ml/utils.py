import math
from random import sample
from api.infrastructure.database.utils import get_db_url
import numpy as np
import re
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

genres = [
    "Action",
    "Adventure",
    "Animation",
    "Children",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Fantasy",
    "Horror",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
]

user_features = [
    "user id",
    "rating count",
    "rating ave",
    "Action",
    "Adventure",
    "Animation",
    "Children",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Fantasy",
    "Horror",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
]

year_regex_pattern = "([(])([0-9]{4})([)]$)"

item_features = [
    "movie id",
    "year",
    "ave rating",
    "Action",
    "Adventure",
    "Animation",
    "Children",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Fantasy",
    "Horror",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
]


def generate_target(item_train, df_movies):
    y_df = pd.merge(item_train, df_movies, left_on=["movie id"], right_on=["id"])
    y_df = y_df["imdb_rating"]
    return y_df


def generate_user_profile(df_movie_rating):
    users_id = df_movie_rating["rater_id"].unique()
    data = [
        generate_user_profile_values(user_id, df_movie_rating) for user_id in users_id
    ]
    df = pd.DataFrame(data, columns=user_features)
    df[["user id", "rating count"]] = df[["user id", "rating count"]].astype(int)
    return pd.DataFrame(data, columns=user_features)


def generate_user_profile_values(user_id, df_movie_rating):
    rating_ave = (
        df_movie_rating[(df_movie_rating["rater_id"] == user_id)]
        .groupby("title")["rating"]
        .mean()
        .mean()
    )
    rating_count = (
        df_movie_rating[(df_movie_rating["rater_id"] == user_id)]
        .groupby("title")["rating"]
        .count()
        .count()
    )
    genres_mean = [
        df_movie_rating[
            (df_movie_rating["rater_id"] == user_id) & (df_movie_rating[genre] == 1)
        ]
        .groupby("title")["rating"]
        .mean()
        .mean()
        for genre in genres
    ]
    return np.array([user_id] + [rating_count] + [rating_ave] + genres_mean)


def generate_movies_profile(movies_id, df_movie_rating):
    data = [
        generate_movies_profile_values(movie_id, df_movie_rating)
        for movie_id in movies_id
    ]
    df = pd.DataFrame(data, columns=item_features)
    df[["movie id", "year"] + genres] = df[["movie id", "year"] + genres].astype(int)
    return df


def generate_movies_profile_values(movie_id, df_movie_rating):
    rating_ave = (
        df_movie_rating[(df_movie_rating["movie_rated_id"] == movie_id)]
        .groupby("title")["rating"]
        .mean()
        .mean()
    )
    genres_belonging = [
        df_movie_rating[(df_movie_rating["movie_rated_id"] == movie_id)][genre].values[
            0
        ]
        for genre in genres
    ]
    year = df_movie_rating[(df_movie_rating["movie_rated_id"] == movie_id)][
        "year"
    ].values[0]
    return np.array([movie_id] + [int(year)] + [rating_ave] + genres_belonging)


def load_data():
    logger.info("loading and transforming data...")

    # lê as tabelas do sql
    df_movies = pd.read_sql_table("movie", con=get_db_url())
    df_ratings = pd.read_sql_table("rating", con=get_db_url())

    # gera um dicionário { id_filme: [filme] } (a ser usado para facilitar as predições)
    df_movies_orig = df_movies
    movies_dict = df_movies_orig.set_index(df_movies_orig["id"]).T.to_dict()
    del df_movies_orig

    # faz one-hot encoding nos gêneros para facilitar a análise
    df_movies = df_movies.reindex(
        df_movies.columns.tolist() + genres, axis=1, fill_value=0
    )
    for genre in genres:
        df_movies[genre] = df_movies["genres"].str.contains(genre).astype("int")
    df_movies = df_movies.drop(columns=["genres"])

    # cria um join entre movie e rating e adiciona a coluna ano para concentrar os dados
    df_movie_rating = pd.merge(
        df_movies, df_ratings, left_on=["id"], right_on=["movie_rated_id"]
    )
    df_movie_rating = df_movie_rating.drop(columns=["id_y", "id_x"])
    df_movie_rating["year"] = df_movie_rating["title"].str.extract(
        year_regex_pattern, flags=re.X, expand=False
    )[1]
    df_movie_rating.fillna(2005, inplace=True)

    # agregado entre nome do filme e rating do usuário
    df_movie_rating_avg = pd.DataFrame(
        df_movie_rating.groupby("title")["rating"].mean()
    )
    df_movie_rating_avg["num_ratings"] = pd.DataFrame(
        df_movie_rating.groupby("title")["rating"].count()
    )

    # agregado entre user(rater_id), nome do filme e rating
    df_movie_rating_user_avg = pd.DataFrame(
        df_movie_rating.groupby(["rater_id", "title"])["rating"].mean()
    )

    # gera os feature vectors dos users, movies e do target (coluna imdb_rating)
    movies_id = df_movie_rating["movie_rated_id"].unique()
    df_item_set = generate_movies_profile(movies_id, df_movie_rating)
    df_y_set = generate_target(df_item_set, df_movies)
    df_user_set = generate_user_profile(df_movie_rating)

    total_items = df_item_set.value_counts().sum()
    total_users = df_user_set.value_counts().sum()
    users_to_fill = math.trunc(total_items / total_users)
    users_to_fill_mod = total_items % total_users

    # "preenche" o df_user_set para ficar do mesmo tamanho do df_item_set
    df_user_set = df_user_set._append(
        [df_user_set] * (users_to_fill - 1), ignore_index=True
    )
    df_user_set = df_user_set._append(
        [df_user_set[:users_to_fill_mod]], ignore_index=True
    )

    # converte para np para utilizar no treinamento
    user_set = df_user_set.to_numpy()
    y_set = df_y_set.to_numpy()
    item_set = df_item_set.to_numpy()

    logger.info("done loading data.")

    return (
        item_set,
        user_set,
        y_set,
        movies_dict,
        df_movie_rating,
        df_movie_rating_user_avg,
    )


def gen_user_vecs(user_vec, num_items):
    """gerar um vetor de mesmo tamanho dos items para o treino"""
    user_vecs = np.tile(user_vec, (num_items, 1))
    return user_vecs


def generate_subset_movies_not_rated(
    userId, df_movie_rating, df_movie_rating_user_avg, min_imdb_rating=4.0
):
    """gera, com base no df de filmes, um subset de 60% de tamanho só com filmes que o user não avaliou.
    Os filmes tem que ter uma avaliação mínima no imdb_rating de min_imdb_rating"""
    try:
        df_result = df_movie_rating_user_avg.loc[userId].reset_index()["movie_rated_id"]
        df_result = df_movie_rating[~df_movie_rating["movie_rated_id"].isin(df_result)]
    except KeyError:
        df_result = df_movie_rating

    df_result = df_result[df_result["imdb_rating"] > min_imdb_rating]
    movies_id = df_result["movie_rated_id"].unique()
    subset_movies_id = np.random.choice(
        movies_id, size=math.ceil(len(movies_id) * 0.6), replace=False
    )
    return generate_movies_profile(subset_movies_id, df_movie_rating).to_numpy()


def get_pred_movies(y_p, item, movie_dict, maxcount=50):
    """retorna um df com os resultados da predicao de um novo user com inputs ordenados."""
    count = 0
    disp = [["y_p", "movie id", "rating ave", "title", "genres"]]

    for i in range(0, y_p.shape[0]):
        if count == maxcount:
            break
        count += 1
        movie_id = item[i, 0].astype(int)
        disp.append(
            [
                np.around(y_p[i, 0], 1),
                movie_id,
                np.around(item[i, 2].astype(float), 1),
                movie_dict[movie_id]["title"],
                movie_dict[movie_id]["genres"],
            ]
        )
    return pd.DataFrame(data=disp[1:], columns=disp[0])


def sq_dist(a, b):
    return np.linalg.norm(a - b) ** 2
