from datetime import datetime
from pathlib import Path
import pandas as pd 
from datafeeds_reports.utils import write_output_to_csv, discover_file, clean_processed_files


FILE_PATTERN = 'Sheet*MonthEndProcessing_BeneficiaryPercentage.csv'
BENEFFTYPE_MIN_COUNT = {
    'Conting. Benef (Revocable)': 4,
    'Conting. Benef (Irrevocable)': 4,
    'Revocable': 10,
    'Beneficiary': 10,
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
        fltr = df[col] >= col_max_count
        df.loc[fltr, 'Error'] = True 
        df.loc[fltr]['Audit'].apply(lambda error: error.append(f'{col} more than or equal to {col_max_count}'))
    
    # if perecentage more than 100
    fltr = df['percentage_sum'] > 100
    df.loc[fltr, 'Error'] = True 
    df.loc[fltr]['Audit'].apply(lambda error: error.append('Percentage more than 100%'))
    return df


def formating_output(df: pd.DataFrame) -> pd.DataFrame:
    df['Audit'] = df['Audit'].apply(lambda errors: ';'.join(errors) if errors else '')

    # filter only those with errors
    df = df[df['Error'] == True]
    return df


def run_report(file_search_path: Path, file_pattern: str, final_output_filename: Path) -> None:
    file = discover_file(search_path=file_search_path, file_pattern=file_pattern)
    df = read_and_filter_data(filepath=file)
    df = flag_errors_in_data(df=df)
    df = formating_output(df=df)
    finished_writing = write_output_to_csv(df=df, filename=final_output_filename)
    if finished_writing:
        clean_processed_files(filepath=file, rename=True, remove=False)


def main(): 
    SEARCH_PATH = Path(__file__).parents[2] / 'data'
    OUTPUT_PATH = Path(__file__).parents[2] / 'output'
    today = datetime.today().strftime(r'%Y%m%d')
    output_file_name = OUTPUT_PATH / f'{today}_{Path(__file__).stem}_output.csv'
    run_report(file_search_path=SEARCH_PATH, file_pattern=FILE_PATTERN, final_output_filename=output_file_name)


if __name__ == '__main__':
    main()