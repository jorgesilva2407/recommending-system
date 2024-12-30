import os
import pickle
import pandas as pd
from model import Model


def main():
    input_filename = os.getenv("INPUT_FILENAME")
    print("INPUT_FILENAME", input_filename)
    output_filename = os.getenv("OUTPUT_FILENAME")
    print("OUTPUT_FILENAME", output_filename)
    min_support = os.getenv("MIN_SUPPORT")
    print("MIN_SUPPORT", min_support)
    min_confidence = os.getenv("MIN_CONFIDENCE")
    print("MIN_CONFIDENCE", min_confidence)

    df = pd.read_csv(input_filename)
    print("Data loaded")

    playlists = df.groupby("pid")["track_name"].apply(list).to_list()
    tracks = df["track_name"].unique().tolist()
    print("Data processed")

    model = Model()
    model.fit(playlists, tracks, min_support, min_confidence)
    print("Model trained")

    with open(output_filename, "wb") as f:
        pickle.dump(model, f)
    print("Model saved")


if __name__ == "__main__":
    main()
