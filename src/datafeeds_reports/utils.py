from pathlib import Path
import pandas as pd


def write_output_to_csv(df: pd.DataFrame, filename: Path) -> bool:
    df.to_csv(filename)
    return True


def discover_file(search_path: Path, file_pattern: str) -> Path:
    # Return first most recent file or raise exception
    for f in sorted(search_path.glob(file_pattern), key=lambda f: f.stat().st_birthtime, reverse=True):
        # validate file matches?
        return f
    raise FileNotFoundError(f'No file with this pattern ("{file_pattern}") was found in the folder "{search_path}".')


def clean_processed_files(filepath: Path, rename: bool=True, remove: bool=False) -> bool:
    if remove:
        if filepath.exists():
            filepath.unlink()
    elif rename:
        new_filepath = filepath.parents[0] / f'Parsed_{filepath.name}'
        filepath.rename(new_filepath)
    return True

