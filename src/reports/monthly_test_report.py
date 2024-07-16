from pathlib import Path
import inspect


def run_report(input_files: list[Path], output_path: Path):
    ...


if __name__ == '__main__':
    print(inspect.getfullargspec(run_report).args)