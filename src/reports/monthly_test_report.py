from pathlib import Path
import inspect


def run_report(input_file: Path, output_path: Path):
    ...


if __name__ == '__main__':
    print(inspect.getfullargspec(run_report).args)