import json
import pickle
import pandas as pd
from model import Model


def main():
    params = {}
    with open("/app/params.json", "r") as f:
        params = json.load(f)

    input_filename = params["input_filename"]
    output_filename = params["output_filename"]
    min_support = params["min_support"]
    min_confidence = params["min_confidence"]

    df = pd.read_csv(input_filename)
    playlists = df.groupby("pid")["track_name"].apply(set).to_list()

    model = Model()
    model.fit(playlists, min_support, min_confidence)

    with open(output_filename, "wb") as f:
        pickle.dump(model, f)


if __name__ == "__main__":
    main()
