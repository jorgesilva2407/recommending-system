import json
import pickle
import pandas as pd
from fpgrowth_py import fpgrowth


def main():
    params = {}
    with open("/app/params.json", "r") as f:
        params = json.load(f)

    input_filename = params["input_filename"]
    output_filename = params["output_filename"]
    min_support = params["min_support"]
    min_confidence = params["min_confidence"]

    df = pd.read_csv(input_filename)
    playlists = df.groupby("pid")["track_uri"].apply(list).values.tolist()

    rules = []

    try:
        _, rules = fpgrowth(playlists, min_support, min_confidence)
    except Exception as e:
        rules = []

    tuple_rules = [(rule[0], rule[1]) for rule in rules]

    pickle.dump(
        tuple_rules,
        open(output_filename, "wb"),
    )


if __name__ == "__main__":
    main()
