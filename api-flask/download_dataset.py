import os
from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

datasets = "djilax/allocine-french-movie-reviews"
download_path = os.path.join(os.getcwd(), "kaggle_data")

os.makedirs(download_path, exist_ok=True)

print("Télechargment du dataset")

api.dataset_download_files(datasets, path=download_path, unzip=True)

print(f"datasets telechrge et decompose dans : {download_path}")

