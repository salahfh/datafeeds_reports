from pathlib import Path
import pandas as pd


def write_output_to_csv(df: pd.DataFrame, filename: Path) -> bool:
    df.to_csv(filename)
    return True

