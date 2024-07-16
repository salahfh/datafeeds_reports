from pprint import pprint
from collections import defaultdict, namedtuple
import re
from pathlib import Path
import click
from reports.__init__ import config
from reports.config import FileTypeReport
from reports.utils import ProcessUserChoices, clean_processed_file


# if pattern match add return avaliable reports
# offer an interactive list of choices when there's more than one report
# Otherwise proceed automatically with the report


ReportAndItsFiles = namedtuple('ReportAndItsFiles', 'report files')


def already_parsed_file(file: Path) -> bool:
    return file.stem.startswith('Parsed')


def discover_files(search_path: Path=config.input_search_folder) -> dict[str: list[Path]]:
    folder_structure = defaultdict(list)
    for item in search_path.rglob('*'):
        if item.is_file():
            if already_parsed_file(item):
                print('- SKIP: file already processed.', item)
                continue
            folder_structure[item.parents[0].stem].append(item)
    return folder_structure 


def determine_report_type(folder_structure: dict[str, list[Path]],
                          available_reports: list[FileTypeReport] = config.available_report
                          ) -> list[ReportAndItsFiles]:
    report_with_corresponding_files = []
    for folder in folder_structure:
        for report in available_reports:
            files = sorted(folder_structure.get(folder))
            for filename_pattern in report.filename_patterns:
                matches = list(filter(re.compile(filename_pattern).match, [f.stem for f in files]))
                if not len(matches):
                    # filename don't match pattern
                    break
            else:
                report_with_corresponding_files.append(ReportAndItsFiles(report, files=files))
    return report_with_corresponding_files


def select_report(item: list[ReportAndItsFiles]) -> FileTypeReport:
    '''
    For files that accepts multiple report types. Offer option to select report for given file.
    '''
    reports = item.report
    files = item.files
    if len(reports.reports) == 1:
        report = reports.reports[0]
    elif len(reports.reports) > 1:
        print("Select which report to run for the file(s): ", [file.stem for file in files])
        report = ProcessUserChoices(reports,
                            choice_prompt_func=lambda x: FileTypeReport.get_report_name(x)).get_user_choice()
    return report


def process_reports(valid_reports: list[ReportAndItsFiles]) -> bool:
    for item in valid_reports:
        report = select_report(item)
        files = item.files
        report_name = FileTypeReport.get_report_name(report)
        output_filepath = config.output_search_folder / f"{config.output_filename_preffix}_{report_name}.csv"

        print(f'- Running report for "{report_name}" on file: {[file.stem for file in item.files]}')
        report.run_report(input_files=files, output_file=output_filepath)

        for file in item.files:
            clean_processed_file(filepath=file,
                            rename=config.rename_files_after_processing,
                            remove=config.remove_files_after_processing)


@click.command()
def run_reports():
    folder_structure = discover_files()
    report_with_files = determine_report_type(folder_structure)
    process_reports(report_with_files)


if __name__ == '__main__':
    run_reports()