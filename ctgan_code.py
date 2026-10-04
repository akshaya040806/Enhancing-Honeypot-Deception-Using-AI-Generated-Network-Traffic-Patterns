import pandas as pd
from ctgan import CTGANSynthesizer
from sklearn.preprocessing import LabelEncoder
import os

def process_zeek_json(path):
    df = pd.read_json(path, lines=True)

    # You can add more features if needed
    selected_columns = ['proto', 'duration', 'orig_bytes', 'resp_bytes', 'conn_state']
    df = df[selected_columns].dropna()

    cat_cols = ['proto', 'conn_state']
    encod = {}
    for col in cat_cols:
        encod[col] = LabelEncoder()
        df[col] = encod[col].fit_transform(df[col])
    return df, cate_cols, encod

def train_ctgan(df, cat_cols, epochs=300):
    ctg = CTGANSynthesizer(epochs=epochs)
    ctg.fit(df, cat_cols)
    return ctg

def generate_traffic(ctg, encod, cat_cols, samples=15):
    df_madeup = ctg.sample(samples)
    for col in cat_cols:
        df_madeup[col] = encod[col].inverse_transform(df_makeup[col].round().astype(int))
    return df_madeup

def main():
    input_json = "zeek_logs/GIVE_THE_DIRECTORY_INSIDE_YOU_WANT_IT_IN"
    out_csv = "output_for_tcp/synthetic.csv"

    os.makedirs("zeek_logs", exist_ok=True)
    os.makedirs("output_for_tcp", exist_ok=True)

    df, cat_cols, encod = preprocess_zeek_json(input_json)
    ctg = train_ctgan(df, cat_cols)
    synthetic_df = generate_traffic(ctg, encod, cat_cols, samples=20)
    synthetic_df.to_csv(out_csv, index=False)
    print(f"Synthetic traffic details saved to: {out_csv}")

if __name__ == "__main__":
    main()
