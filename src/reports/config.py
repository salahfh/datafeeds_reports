import inspect
from datetime import datetime
from typing import Callable
from pathlib import Path
from dataclasses import dataclass
from reports import monthly_beneficiary_cleanup_report 
from reports import monthly_test_report


@dataclass
class FileTypeReport:
    filename_pattern: str
    reports: list[Callable] # contains modules

    @classmethod
    def get_report_name(cls, mod: Callable):
        return mod.__name__.split('.')[-1]

    def __post_init__(self):
        # Make sure new reports have the same run_report function
        for report in self.reports:
            assert hasattr(report, 'run_report'), f'{report} do not have a "run_report" function.'
            module_run_report_signature = inspect.getfullargspec(report.run_report).args 
            expected_run_report_signature = inspect.getfullargspec(monthly_beneficiary_cleanup_report.run_report).args 
            assert module_run_report_signature == expected_run_report_signature,\
                  f'{report} ({module_run_report_signature}) The run_report signature must match with the "monthly_beneficiary_cleanup_report.run_report"'


@dataclass
class Configs:
    input_search_folder: Path = Path.home() / 'Datafeed_reports' / 'Input'
    output_search_folder: Path = Path.home() / 'Datafeed_reports' / 'Output'
    output_filename_preffix: str = f"{datetime.now().strftime(r'%Y%m%d')}"
    available_report: list[FileTypeReport] = None
    rename_files_after_processing: bool = True
    remove_files_after_processing: bool = False


    def __post_init__(self):
        # Create folders if do not exist
        for folder in [self.input_search_folder, self.output_search_folder]:
            if not folder.exists():
                print('Creating folder: ', folder)
                folder.mkdir(parents=True)
        
        if self.available_report == None:
            self.available_report = AVAILBLE_REPORTS


# Register new report here.
# Every report must have a function run_report
AVAILBLE_REPORTS = [
    FileTypeReport(
        filename_pattern='Sheet.*MonthEndProcessing_BeneficiaryPercentage',
        reports=[
            monthly_beneficiary_cleanup_report,
            # monthly_test_report
            ]
    )
]


if __name__ == '__main__':
    c = Configs()
    



