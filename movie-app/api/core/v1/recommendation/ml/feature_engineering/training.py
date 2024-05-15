from api.core.v1.recommendation.ml.utils import load_data
from os import path
import keras
import joblib
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split


def training_feature_engineering():
    (
        item_set,
        user_set,
        y_set,
        movies_dict,
        df_movie_rating,
        df_movie_rating_user_avg,
    ) = load_data()

    # configs

    num_user_features = (
        user_set.shape[1] - 3
    )  # remover userid, rating count and ave rating durante o treino
    num_item_features = item_set.shape[1] - 1  # remover movie id durante o treino

    # indices auxiliares
    user_vector_start = 3
    item_vector_start = 3
    user_columns_start = 3
    item_columns_start = 1

    # transformar os dados

    scalerItem = StandardScaler()
    scalerItem.fit(item_set)
    item_set = scalerItem.transform(item_set)

    scalerUser = StandardScaler()
    scalerUser.fit(user_set)
    user_set = scalerUser.transform(user_set)

    scalerTarget = MinMaxScaler((-1, 1))
    scalerTarget.fit(y_set.reshape(-1, 1))
    y_set = scalerTarget.transform(y_set.reshape(-1, 1))

    # separar em treino e teste

    item_train, item_test = train_test_split(
        item_set, train_size=0.70, shuffle=True, random_state=1
    )
    user_train, user_test = train_test_split(
        user_set, train_size=0.70, shuffle=True, random_state=1
    )
    y_train, y_test = train_test_split(
        y_set, train_size=0.70, shuffle=True, random_state=1
    )

    ### definicao das NNs

    # criar os inputs
    input_user = keras.layers.Input(shape=(num_user_features,))
    input_item = keras.layers.Input(shape=(num_item_features,))

    user_NN = keras.models.Sequential(
        [
            keras.layers.Dense(256, activation="relu"),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(32, activation="linear"),
        ]
    )

    item_NN = keras.models.Sequential(
        [
            keras.layers.Dense(256, activation="relu"),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(32, activation="linear"),
        ]
    )

    # direcionar para as NNs
    vu = user_NN(input_user)
    vu = keras.layers.LayerNormalization(axis=1)(vu)

    vm = item_NN(input_item)
    vm = keras.layers.LayerNormalization(axis=1)(vm)

    output = keras.layers.Dot(axes=1)([vu, vm])

    # especificar o input e o output do modelo
    model = keras.Model([input_user, input_item], output)

    # hiperparametros
    cost_fn = keras.losses.MeanSquaredError()
    opt = keras.optimizers.Adam(learning_rate=0.1)

    # compilar e rodar
    model.compile(optimizer=opt, loss=cost_fn)
    model.fit(
        [user_train[:, user_columns_start:], item_train[:, item_columns_start:]],
        y_train,
        epochs=30,
    )

    # salvar no mesmo diretório desse script
    model_name = path.join(
        path.dirname(path.realpath(__file__)), "feature_eng_model.joblib"
    )
    joblib.dump(
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
        ),
        model_name,
    )
