import os
import pickle
import pandas as pd
import requests
from model import Model


def main():
    input_file_link = os.getenv("INPUT_FILE_LINK")
    print("INPUT_FILE_LINK", input_file_link)
    output_filename = os.getenv("OUTPUT_FILENAME")
    print("OUTPUT_FILENAME", output_filename)
    min_support = float(os.getenv("MIN_SUPPORT"))
    print("MIN_SUPPORT", min_support)
    min_confidence = float(os.getenv("MIN_CONFIDENCE"))
    print("MIN_CONFIDENCE", min_confidence)
    version = os.getenv("VERSION")
    print("VERSION", version)

    input_filename = "/tmp/playlists.csv"
    response = requests.get(input_file_link)

    if response.status_code != 200:
        raise Exception(f"Failed to download data from {input_file_link}")

    with open(input_filename, "wb") as f:
        f.write(response.content)

    df = pd.read_csv(input_filename)
    print("Data loaded")

    playlists = (
        df.groupby("pid")["track_name"].apply(lambda x: list(map(str, x))).to_list()
    )
    tracks = list(map(str, df["track_name"].unique().tolist()))
    print("Data processed")

    model = Model(version)
    model.fit(playlists, tracks, min_support, min_confidence)
    print("Model trained")

    with open(output_filename, "wb") as f:
        pickle.dump(model, f)
    print("Model saved")


if __name__ == "__main__":
    main()
