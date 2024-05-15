from api.core.v1.recommendation.ml.feature_engineering.predict import (
    predict_existing_user,
    predict_new_user,
)
from api.core.v1.recommendation.schemas import NewUserRatings, Recommendations


def create_recommendations(newUserRatings: NewUserRatings) -> list[Recommendations]:
    movie_list = []
    df_recommends = predict_new_user(newUserRatings)
    for index, row in df_recommends.iterrows():
        movie_list.append(
            Recommendations(title=row["title"], genres=row["genres"].split("|"))
        )
    return movie_list


def get_recommendations(user_id: int) -> list[Recommendations]:
    movie_list = []
    df_recommends = predict_existing_user(user_id)
    for index, row in df_recommends.iterrows():
        movie_list.append(
            Recommendations(title=row["title"], genres=row["genres"].split("|"))
        )
    return movie_list
