from pathlib import Path
import shutil
import pytest
from reports.config import ReportFileType, Configs
from reports import monthly_test_report
from reports.cli import determine_report_type


@pytest.fixture()
def config():
    # Set the configure object
    # Create folder 
    test_path = Path.home() / 'datafeed_reports_tests'
    config = Configs(data_folder=test_path)
    yield config
    # shutil.rmtree(test_path)


def create_files(config: Configs, filenames: list[str], extension='.csv') -> Path:
    filepaths = []
    for filename in filenames:
        filename = filename.replace('.*', '1234_test_1234')
        filepath = config.input_search_folder / f'{filename}{extension}'
        filepath.touch()
        filepaths.append(filepath)
    return filepaths


def test_my_test_setup_is_working_correctly(config):
    assert isinstance(config, Configs)


# Testing selection of the correct report type
def test_report_with_single_file(config):
    report = ReportFileType(
        report=monthly_test_report,
        filename_patterns=['Sheet_.*_MonthEndProcessing_BeneficiaryPercentage']
        )
    filepaths = create_files(config=config, filenames=report.filename_patterns)
    
    


def test_report_with_multiple_files():
    assert False


def test_report_with_multiple_files_inside_folder():
    assert False


def test_filename_pattern_shared_between_multiple_reports():
    assert False


def test_invalid_filename_pattern():
    assert False