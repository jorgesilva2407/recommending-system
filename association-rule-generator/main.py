import json
import pickle
import pandas as pd
from model import Model


def main():
    print("Loading parameters...")
    params = {}
    with open("/app/params.json", "r") as f:
        params = json.load(f)

    input_filename = params["input_filename"]
    output_filename = params["output_filename"]
    min_support = params["min_support"]
    min_confidence = params["min_confidence"]
    print("Parameters loaded.")

    print("Loading data...")
    df = pd.read_csv(input_filename)
    print("Data loaded.")

    print("Preprocessing data...")
    playlists = df.groupby("pid")["track_name"].apply(list).to_list()
    print("Data preprocessed.")

    print("Training model...")
    model = Model()
    model.fit(playlists, min_support, min_confidence)
    print("Model trained.")

    print("Saving model...")
    with open(output_filename, "wb") as f:
        pickle.dump(model, f)
    print("Model saved.")


if __name__ == "__main__":
    main()
