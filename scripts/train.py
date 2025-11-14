from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

import pandas as pd
import xgboost as xgb

from sklearn.model_selection import train_test_split


def load_dataset(path: str) -> pd.DataFrame:
    '''for explanation of selected features see notebook.ipynb '''

    df = pd.read_csv(path, sep=";")
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    df['is_excellent'] = df['quality'] >= 8
    df = df.drop(columns=['density', 'total_sulfur_dioxide','citric_acid', 'quality'])
    print(f"Loaded dataset. Size {df.shape}")
    return df


def train_model(df: pd.DataFrame) -> xgb.XGBClassifier:
    '''for explanation of selected params see notebook.ipynb '''

    features = df.copy()
    del features['is_excellent']
    
    targets = df['is_excellent']

    X_train_full, X_test, y_train_full, y_test = train_test_split(
        features, targets, test_size=0.2, random_state=1, stratify=targets
    )

    xgb_model = xgb.XGBClassifier(
        objective='binary:logistic',
        seed=1,
        n_estimators=2000,
        eval_metric='logloss',
        learning_rate=0.5,
        max_depth=7,
        min_child_weight=1,
        subsample=0.8,
        colsample_bytree=0.6,
        early_stopping_rounds=20,
    )

    final_model = xgb_model.fit(X_train_full, y_train_full, eval_set=[(X_test, y_test)])
    score = final_model.score(X_test, y_test)
    print(f"Model trained. Accuracy: {score}")

    return final_model


def save_model(model: xgb.XGBClassifier, path: str | None = None) -> None:
    breakpoint()
    path = path or '.'

    result_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_path = Path(path) / f"model_{result_date}.json"

    model.save_model(full_path)
    print(f"Model saved to: {full_path}")


if __name__ == "__main__":
    parser = ArgumentParser(description="train CLI")

    parser.add_argument("input_file")
    parser.add_argument("-o", "--output_dir", required=False)

    call_args = vars(parser.parse_args())
    df = load_dataset(call_args['input_file'])
    model = train_model(df)
    save_model(model, call_args['output_dir'])
