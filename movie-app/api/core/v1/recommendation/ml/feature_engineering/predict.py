from os import path
from api.core.v1.recommendation.schemas import NewUserRatings
from api.core.v1.recommendation.ml.utils import (
    gen_user_vecs,
    generate_subset_movies_not_rated,
    genres,
    get_pred_movies,
)
import joblib
import numpy as np


def predict_new_user(user_ratings=NewUserRatings):

    (
        df_movie_rating,
        df_movie_rating_user_avg,
        model,
        user_columns_start,
        item_columns_start,
        scalerUser,
        scalerItem,
        scalerTarget,
        movies_dict,
    ) = joblib.load(
        path.join(path.dirname(path.realpath(__file__)), "feature_eng_model.joblib")
    )

    new_user_id = user_ratings.id if user_ratings.id else 0
    new_rating_count = user_ratings.rating_count if user_ratings.rating_count else 5
    new_rating_ave = user_ratings.rating_avg if user_ratings.rating_avg else 0.0
    new_user_vec = np.array(
        [
            [
                new_user_id,
                new_rating_count,
                new_rating_ave,
                user_ratings.ratings.action,
                user_ratings.ratings.adventure,
                user_ratings.ratings.animation,
                user_ratings.ratings.childrens,
                user_ratings.ratings.comedy,
                user_ratings.ratings.crime,
                user_ratings.ratings.documentary,
                user_ratings.ratings.drama,
                user_ratings.ratings.fantasy,
                user_ratings.ratings.horror,
                user_ratings.ratings.mystery,
                user_ratings.ratings.romance,
                user_ratings.ratings.scifi,
                user_ratings.ratings.thriller,
            ]
        ]
    )

    item_vecs = generate_subset_movies_not_rated(
        new_user_id, df_movie_rating, df_movie_rating_user_avg, min_imdb_rating=3.0
    )

    # gerar o vetor de users para ser do mesmo tamanho do item_vecs
    user_vecs = gen_user_vecs(new_user_vec, len(item_vecs))

    # transformar os valores
    suser_vecs = scalerUser.transform(user_vecs)
    sitem_vecs = scalerItem.transform(item_vecs)

    # predição
    y_p = model.predict(
        [suser_vecs[:, user_columns_start:], sitem_vecs[:, item_columns_start:]]
    )
    y_pu = scalerTarget.inverse_transform(y_p)

    sorted_index = np.argsort(-y_pu, axis=0).reshape(-1).tolist()
    sorted_ypu = y_pu[sorted_index]
    sorted_items = item_vecs[sorted_index]

    return get_pred_movies(sorted_ypu, sorted_items, movies_dict, maxcount=50)


def predict_existing_user(user_id: int):

    (
        df_movie_rating,
        df_movie_rating_user_avg,
        model,
        user_columns_start,
        item_columns_start,
        scalerUser,
        scalerItem,
        scalerTarget,
        movies_dict,
    ) = joblib.load(
        path.join(path.dirname(path.realpath(__file__)), "feature_eng_model.joblib")
    )

    # agrupa os filmes avaliados com os generos
    df_movie_rating_user_avg_genres = df_movie_rating.groupby(
        ["rater_id", "title"] + genres
    )["rating"].mean()
    df_movie_rating_user_avg_genres = df_movie_rating_user_avg_genres.loc[
        user_id
    ].reset_index()
    rating_count = df_movie_rating_user_avg_genres.value_counts().sum()
    rating_ave = df_movie_rating_user_avg_genres["rating"].mean()
    user_vec = [user_id, rating_count, rating_ave] + [
        df_movie_rating_user_avg_genres[df_movie_rating_user_avg_genres[genre] == 1][
            "rating"
        ].mean()
        for genre in genres
    ]

    item_vecs = generate_subset_movies_not_rated(
        user_id, df_movie_rating, df_movie_rating_user_avg, min_imdb_rating=3.0
    )

    # gerar o vetor de users para ser do mesmo tamanho do item_vecs
    user_vecs = gen_user_vecs(user_vec, len(item_vecs))

    # transformar os valores
    suser_vecs = scalerUser.transform(user_vecs)
    sitem_vecs = scalerItem.transform(item_vecs)

    # predição
    y_p = model.predict(
        [suser_vecs[:, user_columns_start:], sitem_vecs[:, item_columns_start:]]
    )
    y_pu = scalerTarget.inverse_transform(y_p)

    sorted_index = np.argsort(-y_pu, axis=0).reshape(-1).tolist()
    sorted_ypu = y_pu[sorted_index]
    sorted_items = item_vecs[sorted_index]

    return get_pred_movies(sorted_ypu, sorted_items, movies_dict, maxcount=50)
