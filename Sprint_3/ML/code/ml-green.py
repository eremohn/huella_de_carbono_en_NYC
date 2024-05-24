import pandas as pd
import numpy as np
import os
import warnings
import boto3
import pickle
from io import StringIO
from datetime import date
from dateutil import relativedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from skforecast.ForecasterAutoregMultiSeries import ForecasterAutoregMultiSeries
from skforecast.model_selection_multiseries import grid_search_forecaster_multiseries

warnings.filterwarnings("ignore")


def calcular_u1(y_true, y_pred):
    size = len(y_true)
    u = np.sqrt(np.sum(np.square(y_true-y_pred))/size)
    u /= np.sum(np.sqrt(np.sum(np.square(y_true))/size)+np.sqrt(np.sum(np.square(y_pred))/size))
    return u


script_name = os.path.basename(__file__)

# Inicialización de variables
today = date.today()
mes = today.month
steps = mes - 2
year = (today - relativedelta(months=steps, day=1))
dias_feb = 29 if not year % 4 and (year % 100 or not year % 400) else 28
cant_dias_mes = {
    1: 31, 2: dias_feb, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
}
test_start = (today - relativedelta(months=5, day=1))
train_end = test_start - relativedelta(days=1)
test_end = train_end + relativedelta(months=2)

# Información de los buckets
bucket = "henry_pf"
green_dir = f"datos_ml/MONTH={mes}/data_borough/green_trips_day.csv"
s3 = boto3.resource(bucket)
s3_client = boto3.client(bucket)

# Leer archivo csv de taxis amarillos
green_obj = s3_client.get_object(Bucket=bucket, Key=green_dir)
green_string = green_obj["Body"].read().decode()
green_df_pivot = pd.read_csv(StringIO(green_string))
green_df_pivot.index = pd.to_datetime(green_df_pivot.index)

train_size = len(green_df_pivot[green_df_pivot.index < date(year=2024, month=1, day=1)])

# Forecaster
green_forecaster = ForecasterAutoregMultiSeries(
    regressor=RandomForestRegressor(
        random_state=42
    ),
    lags=7,
    transformer_series=StandardScaler()
)

# Búsqueda grid de los mejores parámetros
lags_grid = list(range(4, 15))
param_grid = {
    'n_estimators': [5, 10, 20, 50, 100],
    'max_depth': list(range(4, 16))
}

green_params = {}
for col in ["cant_registros", "sum_distancia", "sum_total", "prom_total"]:
    cols = [x for x in list(green_df_pivot.columns) if col in x]

    green_grid = grid_search_forecaster_multiseries(
        forecaster=green_forecaster,
        series=green_df_pivot.reset_index(),
        param_grid=param_grid,
        lags_grid=lags_grid,
        levels=cols,
        steps=10,
        metric=["mean_squared_error", "mean_absolute_error", calcular_u1],
        initial_train_size=train_size,
        refit=True,
        fixed_train_size=True,
        return_best=True,
        verbose=False,
        show_progress=True
    )

    green_params[col] = green_grid.head(1)[["max_depth", "n_estimators", "lags"]].squeeze().to_dict()

models_folder = f"datos_ml/MONTH={mes}/models/"
preds_folder = f"datos_ml/MONTH={mes}/predicted/"

# Entrenar y guardar los modelos con los mejores parámetros, y hacer predicciones por día
green_predictions = []
for col in green_params.keys():
    cols = [x for x in list(green_df_pivot.columns) if col in x]
    barrios = [c.split("_")[-1] for c in cols]
    
    green_forecaster = ForecasterAutoregMultiSeries(
        regressor=RandomForestRegressor(
            max_depth=green_params[col]["max_depth"],
            n_estimators=green_params[col]["n_estimators"],
            random_state=42
        ),
        lags=len(green_params[col]["lags"]),
        transformer_series=StandardScaler()
    )
    green_forecaster.fit(series=green_df_pivot[cols])
    green_preds = green_forecaster.predict(steps=steps)
    
    model_file = f"green_taxis_{col}.pkl"
    with open(model_file) as model:
        pickle.dump(green_forecaster, model)
    
    boto3.Session().resource('s3').Bucket(bucket).Object(os.path.join(dest_folder, model_file)).upload_file(model_file)
    
    # Resumir las predicciones al mes
    if col == "cant_registros":
        series_preds = green_preds.sum().round().astype(int)
    elif col == "prom_total":
        series_preds = green_preds.mean()
    else:
        series_preds = green_preds.sum()
    series_preds.index = barrios
    series_preds.name = col
    green_predictions.append(series_preds)
    
# Guardar las predicciones para el mes
preds_df = pd.DataFrame(green_predictions).transpose()
preds_df.index.name = "barrio_abordaje"
preds_df.reset_index(inplace=True)
preds_df["mes"] = date(year=year, month=mes, day=1)
preds_file = f"predicciones_{year}-{mes}.csv"
preds_df.to_csv(preds_file, index=False)
boto3.Session().resource('s3').Bucket(bucket).Object(os.path.join(preds_folder, preds_file)).upload_file(preds_file)