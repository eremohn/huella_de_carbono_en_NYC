import pandas as pd
import numpy as np
import os
import warnings
import boto3
import pickle
from io import StringIO
from datetime import date
from dateutil import relativedelta
from sklearn.linear_model import Ridge
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from skforecast.model_selection import grid_search_forecaster

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
bucket = "henry-pf"
nyc_co2_dir = f"datos-dashboard/MONTH={mes}/NYC_CO2/NYC_CO2.csv"
s3 = boto3.resource(bucket)
s3_client = boto3.client(bucket)

# Leer archivo csv de CO2
obj = s3_client.get_object(Bucket=bucket, Key=nyc_co2_dir)
string = obj["Body"].read().decode()
df = pd.read_csv(StringIO(string))
len_train = len(df)-5

# Forecaster y búsqueda grid de los mejores parámetros
lags_grid = list(range(2, 15))
param_grid = {
    "alpha": [1, 0.1, 0.01, 0.001, 0.0001, 0],
    "fit_intercept": [True, False],
    "solver": ['svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga']
}

forecaster = ForecasterAutoreg(
    regressor=Ridge(random_state=42),
    lags=7
)

grid = grid_search_forecaster(
    forecaster=forecaster,
    y=df.Total,
    param_grid=param_grid,
    lags_grid=lags_grid,
    steps=5,
    metric=["mean_squared_error", "mean_absolute_error", calcular_u1],
    initial_train_size=len_train,
    refit=True,
    fixed_train_size=True,
    return_best=True,
    verbose=False,
    show_progress=True
)

# Entrenar y guardar el modelo con los mejores parámetros
params = grid.head(1)[["alpha", "fit_intercept", "solver", "lags"]].squeeze().to_dict()
final_forecaster_ridge = ForecasterAutoreg(
    regressor=Ridge(
        alpha=params["alpha"],
        fit_intercept=params["fit_intercept"],
        solver=params["solver"],
        random_state=42
    ),
    lags=len(params["lags"])
)
final_forecaster_ridge.fit(y=df.Total)

models_folder = f"datos_ml/MONTH={mes}/models/"
preds_folder = f"datos_ml/MONTH={mes}/predicted/"

with open("co2_preds.pkl", "wb") as model:
    pickle.dump(final_forecaster_ridge, model)
boto3.Session().resource('s3').Bucket(bucket).Object(os.path.join(models_folder, "co2_preds.pkl")).upload_file("co2_preds.pkl")

# Predicciones
steps = 10
year_init = df.Year.max()+1
preds = final_forecaster_ridge.predict(steps=steps)
preds.index = list(range(year_init,year_init+steps+1))
preds.index.name = "Year"
preds.name = "Total"
preds.to_csv("co2_predicciones.csv")

boto3.Session().resource('s3').Bucket(bucket).Object(os.path.join(preds_folder, "co2_predicciones.csv")).upload_file("co2_predicciones.csv")