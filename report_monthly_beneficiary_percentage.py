from pathlib import Path
import pandas as pd 


FILE_PATTERN = '*MonthEndProcessing_BeneficiaryPercentage.csv'
BENEFFTYPE_MIN_COUNT = {
    'Conting. Benef (Revocable)': 4,
    'Conting. Benef (Irrevocable)': 4,
    'Revocable': 10,
    'Beneficiary': 10
}


def read_and_filter_data(filepath: Path) -> pd.DataFrame:
    df_raw = pd.read_csv(filepath)
    fltr = df_raw['beneftype'].isin(BENEFFTYPE_MIN_COUNT.keys())
    df = df_raw[fltr].groupby(['Registration_Number', 'beneftype'])['beneftype'].count()
    df = df.unstack()
    df = df.fillna(0)
    df = df.astype(int)
    df_percentage = df_raw[['percentage_sum', 'Registration_Number']].drop_duplicates().set_index('Registration_Number')
    df = df.join(df_percentage)
    return df


def flag_errors_in_data(df: pd.DataFrame) -> pd.DataFrame:
    # Flag based on benefftype min count: 
    df['Error'] = ''
    df['Audit'] = [[] for _ in range(len(df))]
    for col in BENEFFTYPE_MIN_COUNT.keys(): 
        col_max_count = BENEFFTYPE_MIN_COUNT.get(col)
        fltr = df[col] > col_max_count
        df.loc[fltr, 'Error'] = True 
        df.loc[fltr]['Audit'].apply(lambda error: error.append(f'{col} more than {col_max_count}'))
    
    # if perecentage more than 100
    fltr = df['percentage_sum'] > 100
    df.loc[fltr, 'Error'] = True 
    df.loc[fltr]['Audit'].apply(lambda error: error.append('Percentage more than 100%'))
    return df


def formating_output(df: pd.DataFrame) -> pd.DataFrame:
    df['Audit'] = df['Audit'].apply(lambda errors: ';'.join(errors) if errors else '')
    return df


def write_output(df: pd.DataFrame, filename: Path) -> None:
    ...


def discover_file(search_path: Path, file_pattern: str) -> Path:
    # Return first most recent file or raise exception
    for f in sorted(search_path.glob(file_pattern), key=lambda f: f.stat().st_birthtime, reverse=True):
        # validate file matches?
        return f
    raise FileNotFoundError(f'No file with this pattern ("{file_pattern}") was found. Try adding a "*" to the pattern.')


def clean_processed_files(rename: bool=True, remove: bool=False) -> bool:
    ...


def main(): 
    file = discover_file(search_path=SEARCH_PATH, file_pattern=FILE_PATTERN)
    df = read_and_filter_data(filepath=file)
    df = flag_errors_in_data(df=df)
    df = formating_output(df=df)
    df.to_csv(output_file_name)
    print(df)


if __name__ == '__main__':
    SEARCH_PATH = Path(__file__).parents[0] / 'data'
    output_file_name = SEARCH_PATH / 'output.csv'
    main()