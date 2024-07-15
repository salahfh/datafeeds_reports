from pathlib import Path
import pandas as pd
from typing import Callable
from dataclasses import dataclass


@dataclass
class UserChoice:
    index: int
    obj: object
    choice_prompt: str


# CLI utility
class ProcessUserChoices:
    '''
    Tasks a list of objects and a formating function and return a choice selector.
    '''
    def __init__(self, 
                 objects: list[object],
                 choice_prompt_func: Callable = lambda x: str(x)) -> None:
        self.objects = objects
        self.choice_prompt = choice_prompt_func
        self.choices = self.__generate_list_of_choices()

    def validate_input(self):
        if len(self.objects) <= 0:
            raise ValueError('List of choices must be more than 0')
        return True

    def __generate_list_of_choices(self) -> list[UserChoice]:
        choices = []
        for index, choice in enumerate(self.objects):
            choices.append(
                UserChoice(
                    index=index,
                    obj=choice,
                    choice_prompt=self.choice_prompt(choice)
                )
            )
        return choices

    def get_user_choice(self) -> object:
        if self.validate_input():
            pass

        choice_index = -1
        for choice in self.choices:
            print(f'{choice.index}) {choice.choice_prompt}')
        while True: 
            try: 
                choice_index = input('Enter the index of your choice to process -> ')
            except KeyboardInterrupt:
                print('Bye!')
                exit()
            if int(choice_index) not in (choice.index for choice in self.choices):
                print('Please try again! ', end=' ')
                continue
            else:
                return self.choices.pop(int(choice_index)).obj



def write_output_to_csv(df: pd.DataFrame, filename: Path) -> bool:
    df.to_csv(filename)
    return True


def discover_file(search_path: Path, file_pattern: str) -> Path:
    # Delete this code [TODO]
    # Return first most recent file or raise exception
    for f in sorted(search_path.glob(file_pattern), key=lambda f: f.stat().st_birthtime, reverse=True):
        # validate file matches?
        return f
    raise FileNotFoundError(f'No file with this pattern ("{file_pattern}") was found in the folder "{search_path}".')


def clean_processed_file(filepath: Path, rename: bool=True, remove: bool=False) -> bool:
    if remove:
        if filepath.exists():
            filepath.unlink()
    elif rename:
        new_filepath = filepath.parents[0] / f'Parsed_{filepath.name}'
        filepath.rename(new_filepath)
    return True

 