import pytest
from reports.utils import ProcessUserChoices


CHOICES = ['first', 'second', 'third']


def test_valid_choice(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "1")
    choice = ProcessUserChoices(CHOICES).get_user_choice()
    assert choice == 'first'


def test_selecting_correct_choice_after_multiple_attempts(monkeypatch):
    user_choices = ['1', '9', '8']
    monkeypatch.setattr('builtins.input', lambda _: user_choices.pop())
    choice_processor = ProcessUserChoices(CHOICES)
    choice = choice_processor.get_user_choice()
    assert choice == 'first'


def test_unvalid_choice_string(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "x")
    choice_processor = ProcessUserChoices(CHOICES)
    choice_processor.testing = True
    with pytest.raises(NotImplementedError):
        choice = choice_processor.get_user_choice()


def test_choice_not_in_the_list(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "9")
    choice_processor = ProcessUserChoices(CHOICES)
    choice_processor.testing = True
    with pytest.raises(NotImplementedError):
        choice = choice_processor.get_user_choice()