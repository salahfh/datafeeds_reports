from pathlib import Path
import shutil
import pytest
from reports.config import FileTypeReport, Configs
from reports import monthly_test_report
from reports import monthly_test_report as monthly_test_report2
from reports.cli import discover_files, determine_report_type, select_report, ReportAndItsFiles


ONE_FILE_TEST_REPORT = FileTypeReport(
    filename_patterns=['Sheet_.*_MonthEndProcessing_BeneficiaryPercentage'],
    reports=[monthly_test_report],
    )

TWO_FILES_TEST_REPORT = FileTypeReport(
    filename_patterns=['Sheet_.*_MonthEndProcessing_BeneficiaryPercentage',
                        'Sheet_.*_FirstdayProcessing_BeneficiaryPercentage'],
    reports=[monthly_test_report],
    )

ONE_FILE_MULTIPLE_TEST_REPORT = FileTypeReport(
    filename_patterns=['Sheet_.*_MonthEndProcessing_BeneficiaryPercentage'],
    reports=[monthly_test_report,
             monthly_test_report2],
    )


is_not_parsed_fltr = lambda f: not f.stem.startswith('Parsed_')


@pytest.fixture()
def config():
    test_path = Path.home() / 'datafeed_reports_tests' 
    config = Configs(data_folder=test_path)
    yield config
    shutil.rmtree(test_path)


def create_files(folder: Path, filenames: list[str]) -> list[Path]:
    filepaths = []
    for filename in filenames:
        if not folder.exists():
            folder.mkdir(parents=True)
        filename = filename.replace('.*', '1234_test_1234')
        filepath = folder / f'{filename}'
        filepath.touch()
        filepaths.append(filepath)
    return filepaths


def test_my_test_setup_is_working_correctly(config):
    assert isinstance(config, Configs)


# Testing selection of the correct report type
def test_discover_files(config):
    filepaths = create_files(folder=config.input_search_folder, filenames=['first.csv', 'second.csv', 'third.txt'])
    _ = create_files(folder=config.input_search_folder / 'a_folder', filenames=['first.csv', 'second.csv', 'third.txt'])
    expected_output = {
        'Input': [
            config.input_search_folder / 'first.csv',
            config.input_search_folder / 'second.csv',
            config.input_search_folder / 'third.txt',
        ],
        'a_folder': [
            config.input_search_folder / 'a_folder' / 'first.csv',
            config.input_search_folder / 'a_folder' / 'second.csv',
            config.input_search_folder / 'a_folder' / 'third.txt',
        ]
    }

    assert all(isinstance(f, Path) for f in filepaths)
    assert isinstance(discover_files(search_path=config.input_search_folder), dict)
    assert sorted(discover_files(search_path=config.input_search_folder)) == sorted(expected_output)
    

def test_report_with_single_file(config):
    created_files = create_files(folder=config.input_search_folder, filenames=['Sheet_1_MonthEndProcessing_BeneficiaryPercentage.csv'])
    files = discover_files(config.input_search_folder)
    reports_with_files = determine_report_type(folder_structure=files, available_reports=(ONE_FILE_TEST_REPORT, )) 
    assert len(reports_with_files) == 1
    assert isinstance(reports_with_files[0], ReportAndItsFiles)
    assert reports_with_files[0].files == created_files


def test_report_with_single_file_and_one_parsed_file_already(config):
    created_files = create_files(folder=config.input_search_folder, 
                                 filenames=['Sheet_1_MonthEndProcessing_BeneficiaryPercentage.csv',
                                            'Parsed_Sheet_2_MonthEndProcessing_BeneficiaryPercentage.csv'])
    files = discover_files(config.input_search_folder)
    reports_with_files = determine_report_type(folder_structure=files, available_reports=(ONE_FILE_TEST_REPORT, )) 
    assert len(reports_with_files) == 1
    assert reports_with_files[0].files == sorted(filter(is_not_parsed_fltr, created_files))

    
def test_report_with_multiple_files(config):
    created_files = create_files(folder=config.input_search_folder, 
                                 filenames=['Sheet_2_FirstdayProcessing_BeneficiaryPercentage.csv',
                                            'Sheet_1_MonthEndProcessing_BeneficiaryPercentage.csv',])
    files = discover_files(config.input_search_folder)
    reports_with_files = determine_report_type(folder_structure=files, available_reports=(TWO_FILES_TEST_REPORT,)) 
    assert len(reports_with_files) == 1
    assert sorted(reports_with_files[0].files) == sorted(created_files)


def test_report_with_multiple_files_and_some_already_parsed(config):
    created_files = create_files(folder=config.input_search_folder, 
                                 filenames=['Sheet_2_FirstdayProcessing_BeneficiaryPercentage.csv',
                                            'Parsed_Sheet_3_FirstdayProcessing_BeneficiaryPercentage.csv',
                                            'Sheet_1_MonthEndProcessing_BeneficiaryPercentage.csv',])
    files = discover_files(config.input_search_folder)
    reports_with_files = determine_report_type(folder_structure=files, available_reports=(TWO_FILES_TEST_REPORT,)) 
    assert len(reports_with_files) == 1
    assert sorted(reports_with_files[0].files) == sorted(filter(is_not_parsed_fltr, created_files))


def test_filename_pattern_shared_between_multiple_reports(config):
    created_files = create_files(folder=config.input_search_folder, 
                                 filenames=['Sheet_2_FirstdayProcessing_BeneficiaryPercentage.csv',
                                            'Parsed_Sheet_3_FirstdayProcessing_BeneficiaryPercentage.csv',
                                            'Sheet_1_MonthEndProcessing_BeneficiaryPercentage.csv',])
    files = discover_files(config.input_search_folder)
    reports_with_files = determine_report_type(folder_structure=files, available_reports=(TWO_FILES_TEST_REPORT, ONE_FILE_TEST_REPORT)) 
    assert len(reports_with_files) == 2


def test_filename_pattern_with_multiple_reports(config):
    created_files = create_files(folder=config.input_search_folder, 
                                 filenames=['Sheet_1_MonthEndProcessing_BeneficiaryPercentage.csv',])
    files = discover_files(config.input_search_folder)
    reports_with_files = determine_report_type(folder_structure=files, available_reports=(ONE_FILE_MULTIPLE_TEST_REPORT, ))
    assert len(reports_with_files) == 1


def test_report_with_multiple_files_inside_folder(config):
    created_files = create_files(folder=config.input_search_folder / 'folder', 
                                 filenames=['Sheet_2_FirstdayProcessing_BeneficiaryPercentage.csv',
                                            'Parsed_Sheet_3_FirstdayProcessing_BeneficiaryPercentage.csv',
                                            'Sheet_1_MonthEndProcessing_BeneficiaryPercentage.csv',])
    files = discover_files(config.input_search_folder)
    reports_with_files = determine_report_type(folder_structure=files, available_reports=(TWO_FILES_TEST_REPORT,)) 
    assert len(reports_with_files) == 1
    assert sorted(reports_with_files[0].files) == sorted(filter(is_not_parsed_fltr, created_files))


def test_report_with_multiple_files_but_not_placed_in_same_folder(config):
    _ = create_files(folder=config.input_search_folder / 'folder', 
                                 filenames=['Sheet_2_FirstdayProcessing_BeneficiaryPercentage.csv'])
    _ = create_files(folder=config.input_search_folder,  
                                 filenames=[ 'Sheet_1_MonthEndProcessing_BeneficiaryPercentage.csv'])
    files = discover_files(config.input_search_folder)
    reports_with_files = determine_report_type(folder_structure=files, available_reports=(TWO_FILES_TEST_REPORT,)) 
    assert len(reports_with_files) == 0


def test_report_with_invalid_filename_pattern(config):
    _ = create_files(folder=config.input_search_folder, filenames=['first.csv', 'second.csv', 'third.txt'])
    files = discover_files(config.input_search_folder)
    reports_with_files = determine_report_type(folder_structure=files, available_reports=(TWO_FILES_TEST_REPORT, ONE_FILE_TEST_REPORT)) 
    assert len(reports_with_files) == 0