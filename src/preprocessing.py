import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder


def load_data(path: str) -> pd.DataFrame:
    """Load raw loan dataset"""
    return pd.read_csv(path)


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns for clarity"""
    df.columns = [
        "gender", "age", "debt", "marital_status", "bank_customer",
        "education", "ethnicity", "years_employed", "prior_default",
        "employed", "credit_score", "drivers_license", "citizen",
        "zip_code", "income", "approval"
    ]
    return df


def encode_target(df: pd.DataFrame) -> pd.DataFrame:
    """Convert approval labels to numeric"""
    df["approval"] = df["approval"].map({"+": 1, "-": 0})
    return df


def preprocess_features(df: pd.DataFrame):
    """Encode categorical features & scale numerical features"""

    categorical_cols = df.select_dtypes(include="object").columns
    numerical_cols = df.select_dtypes(include=["int64", "float64"]).columns
    numerical_cols = numerical_cols.drop("approval")

    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    scaler = StandardScaler()

    X_cat = encoder.fit_transform(df[categorical_cols])
    X_num = scaler.fit_transform(df[numerical_cols])

    X = np.hstack([X_num, X_cat])
    y = df["approval"].values

    return X, y, encoder, scaler


def split_data(X, y, test_size=0.2):
    """Train-test split"""
    return train_test_split(X, y, test_size=test_size, stratify=y, random_state=42)