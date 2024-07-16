from pathlib import Path
import pandas as pd


def write_output_to_csv(df: pd.DataFrame, filename: Path) -> bool:
    # if filename exists add _1 or _2 or (1) or (2)
    df.to_csv(filename)
    return True

