"""
Flashcard module for crablang application.
This module handles managing flashcards and storing study infor
"""

import re
from typing import Dict, List, Tuple, Optional
import chardet


class Flashcard:
    def __init__(self, term: str, definition: str):
        pass

    def correct_guess(self) -> None:
        pass

    def incorrect_guess(self) -> None:
        pass

    @property
    def get_correct_guesses_number(self) -> int:
        pass

    @property
    def get_incorrect_guesses_number(self) -> int:
        pass

    @property
    def get_guesses_number(self) -> int:
        pass


class FlashcardManager:
    def __init__(self):
        pass

    def load_from_file(path: str):
        pass

    def add_card(term: str, definition: str):
        pass

    def remove_card(term: str):
        pass

    def get_random_card() -> Flashcard:
        pass

    def get_all_cards() -> List[Flashcard]:
        pass

    def reverse_direction() -> None:
        pass
