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


def read_and_filter_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    fltr = df_raw['beneftype'].isin(BENEFFTYPE_MIN_COUNT.keys())
    df = df_raw[fltr].groupby(['Registration_Number', 'beneftype'])['beneftype'].count()
    df = df.unstack()
    df = df.fillna(0)
    df = df.astype(int)
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
    return df


def merge_into_orignal_data(df: pd.DataFrame, df_raw: pd.DataFrame) -> pd.DataFrame:
    df_raw = df_raw.set_index('Registration_Number')
    df = df_raw.join(df[['Error', 'Audit']], lsuffix='left', on='Registration_Number')
    return df


def formating_output(df: pd.DataFrame) -> pd.DataFrame:
    # filter only those without errors
    df = df[df['Error'] != True]
    header = [col for col in df.columns.to_list() if col not in ['Audit', 'Error']]
    return df[header]


def run_report(file_search_path: Path, file_pattern: str, final_output_filename: Path) -> None:
    file = discover_file(search_path=file_search_path, file_pattern=file_pattern)
    df_raw = pd.read_csv(file)
    df = read_and_filter_data(df_raw=df_raw)
    df = flag_errors_in_data(df=df)
    df = merge_into_orignal_data(df=df, df_raw=df_raw)
    df = formating_output(df=df)
    finished_writing = write_output_to_csv(df=df, filename=final_output_filename)
    if finished_writing:
        clean_processed_files(filepath=file, rename=False, remove=False)


def main(): 
    SEARCH_PATH = Path(__file__).parents[2] / 'data'
    OUTPUT_PATH = Path(__file__).parents[2] / 'output'
    today = datetime.today().strftime(r'%Y%m%d')
    output_file_name = OUTPUT_PATH / f'{today}_{Path(__file__).stem}_output.csv'
    run_report(file_search_path=SEARCH_PATH, file_pattern=FILE_PATTERN, final_output_filename=output_file_name)


if __name__ == '__main__':
    main()