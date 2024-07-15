import re
from pathlib import Path
import click
from reports.__init__ import config
from reports.config import FileTypeReport
from reports.utils import ProcessUserChoices, clean_processed_file


# if pattern match add return avaliable reports
# offer an interactive list of choices when there's more than one report
# Otherwise proceed automatically with the report

def determine_report_type(file: Path) -> list[FileTypeReport]:
    for report in config.available_report:
        if re.match(report.filename_pattern, file.stem):
            return report.reports
    return []


already_parsed_file = lambda f: f.stem.startswith('Parsed')


def discover_files(search_path: Path=config.input_search_folder):
    valid_files = []
    for file in list(search_path.glob('*.csv')):
        if already_parsed_file(file):
            print('- SKIP: file already processed.', file.stem)
            continue

        reports = determine_report_type(file=file)
        if reports:
            valid_files.append((file, reports))
        else:
            print('- SKIP: Uncognized file format.', file.stem)
    return valid_files


def select_report_and_run(valid_files: list[(Path, FileTypeReport)]):
    if valid_files:
        print("Start Report Processing.\n")
        for file, reports in valid_files:
            if len(reports) == 1:
                report_module = reports[0]
            elif len(reports) > 1:
                print("Select which report to run for the file: ", file.stem)
                report_module = ProcessUserChoices(reports,
                                    choice_prompt_func=lambda x: FileTypeReport.get_report_name(x)).get_user_choice()

            report_name = FileTypeReport.get_report_name(report_module)
            output_filepath = config.output_search_folder / f"{config.output_filename_preffix}_{report_name}.csv"

            print(f'- Running report for "{report_name}" on file: {file.stem}')
            report_module.run_report(input_file=file, output_file=output_filepath)

            clean_processed_file(filepath=file,
                                  rename=config.rename_files_after_processing,
                                  remove=config.remove_files_after_processing)
        print("\nReport Finished Running")
    return True
        

@click.command()
def run_reports():
    files = discover_files()
    select_report_and_run(valid_files=files)

if __name__ == '__main__':
    run_reports()