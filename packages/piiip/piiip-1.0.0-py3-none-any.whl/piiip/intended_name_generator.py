from __future__ import annotations

import json
import math
import sys

from piiip._logger import logger

if sys.version_info < (3, 10):
    from importlib_resources import files
    from importlib_resources.abc import Traversable
else:
    from importlib.abc import Traversable
    from importlib.resources import files


PYPI_ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyz1234567890-"
PATH_TO_TOKENS = files("piiip.resources").joinpath("tokens_selection.txt")
PATH_TO_ALTERNATE_SPELLINGS = files("piiip.resources").joinpath("us_to_uk.json")
MAX_CHARS_TO_REPLACE = (
    5  # replace at most this many characters in homographic replacement
)

# ascii homographs from Neupane et al. Beyond Typosquatting An In-depth Look at Package Confusion:
# https://github.com/ldklab/typomind-release/blob/main/core/homographic.py"
ASCII_HOMOGRAPHS = {
    "a": "eoq4",
    "b": "dp",
    "c": "o",
    "d": "bpq",
    "e": "ao",
    "f": "t",
    "g": "q",
    "h": "b",
    "i": "lj",
    "j": "il",
    "k": "",
    "l": "ij1",
    "m": "n",
    "n": "rmu",
    "o": "ea0",
    "p": "qg",
    "q": "pg",
    "r": "n",
    "s": "",
    "t": "f",
    "u": "",
    "v": "",
    "w": "",
    "x": "",
    "y": "",
    "z": "",
    "_": "",
}


class IntendedNameGenerator:
    TOKENS: list[str] = []

    def generate_possibly_intended_names(self, package_name: str) -> list[str]:
        """
        Returns a list of names that might have been intended instead of the
        given package_name.
        """
        generated_names: set[str] = set()
        self.missed_character(package_name, generated_names)
        self.added_character(package_name, generated_names)
        self.prefix_suffix_augmentation(package_name, generated_names)
        self.swapped_character(package_name, generated_names)
        self.substituted_character(package_name, generated_names)
        logger.debug(f"Number of generated names: {len(generated_names)}")
        return list(generated_names)

    def missed_character(self, package_name: str, generated_names: set[str]) -> None:
        """
        Someone might have missed a character by accident. Add a character
        between every other character.
        """
        for i in range(
            len(package_name) + 1
        ):  # for every position in which a character could have been added
            for char in PYPI_ALLOWED_CHARS:
                generated_name = package_name[:i] + char + package_name[i:]
                generated_names.add(generated_name)

    def added_character(self, package_name: str, generated_names: set[str]) -> None:
        """
        Someone might have typed an additional character.
        Remove every character.
        """
        for i in range(
            len(package_name)
        ):  # for every position in which a character could have been added
            generated_name = package_name[:i] + package_name[i + 1 :]
            generated_names.add(generated_name)

    def swapped_character(self, package_name: str, generated_names: set[str]) -> None:
        for character_pos_to_shift, _ in enumerate(package_name):
            swapped = self.swap_char_on_pos(package_name, character_pos_to_shift, 1)
            if swapped != package_name:
                generated_names.add(swapped)

    def swap_char_on_pos(
        self,
        package_name: str,
        character_pos_to_shift: int,
        distance: int,
    ) -> str:
        """
        Given a string, a source position in that string and a distance,
        moves the character on the source position <distance> positions to the right
        and the character on the destination position back to the origin position

        If distance is negative, the character is shifted to the left
        If the destination position is out of bounds, the swap is not performed
        """
        generated_name = ""  # start with an empty string
        for i, current_char in enumerate(package_name):  # go over every char in name
            if i == character_pos_to_shift:
                if i + distance >= len(package_name) or i + distance < 0:
                    generated_name += current_char  # cannot swap, do not perform swap
                    continue
                generated_name += package_name[i + distance]
                continue  # if this is the position to be swaped, swap forward
            if (i - distance) == character_pos_to_shift:
                generated_name += package_name[character_pos_to_shift]
                continue  # if this is the position the swaped char will end up, swap back
            generated_name += current_char  # if the char is not to be swapped, just add
        return generated_name

    def substituted_character(
        self, package_name: str, generated_names: set[str]
    ) -> None:
        """
        Substitutes every character in package_name with all possible characters
        in PYPI_ALLOWED_CHARS and puts them in the given set generated_names
        """
        for i, _ in enumerate(package_name):
            generated_names |= self.substitute_char(i, package_name)

    def substitute_char(self, char_pos: int, pkg_name: str) -> set[str]:
        """
        Substitutes the character on position char_pos in pkg_name with
        all characters in PYPI_ALLOWED_CHARS and returns it as a set.
        pkg_name itself is not included in the set
        """
        generated_names = set()
        for c in PYPI_ALLOWED_CHARS:
            if c == pkg_name[char_pos]:
                continue
            generated_names.add(pkg_name[:char_pos] + c + pkg_name[char_pos + 1 :])
        return generated_names

    def prefix_suffix_augmentation(
        self, package_name: str, generated_names: set[str]
    ) -> None:
        """
        Prefix/suffix augmentation [NHWDC23] also called Combosquatting [LPMB23]
        """
        if len(package_name) < 3:
            return

        if not IntendedNameGenerator.TOKENS:
            IntendedNameGenerator.TOKENS = self.load_file_to_list(PATH_TO_TOKENS)

        for token in IntendedNameGenerator.TOKENS:
            generated_names.add(token + package_name)
            generated_names.add(package_name + token)
            generated_names.add(token + "-" + package_name)
            generated_names.add(package_name + "-" + token)

    def alternate_spelling(self, package_name: str, generated_names: set[str]):
        """
        Alternate spelling [NHWDC23]. Replaces every British word in a package
        name with its American counterpard and vice versa.
        """
        with PATH_TO_ALTERNATE_SPELLINGS.open() as f:
            # source: https://github.com/hyperreality/American-British-English-Translator/blob/master/data/american_spellings.json
            am_to_br = json.load(f)
        for key, value in am_to_br.items():
            if key in package_name:
                generated_names.add(package_name.replace(key, value))
            if value in package_name:
                generated_names.add(package_name.replace(value, key))

    def homographic_replacement(self, package_name: str, generated_names: set[str]):
        """
        Homographic replacement [NHWDC23]. Generates all
        package names that are homographically similair to the
        given package name. For example, for the name "bck", the
        b can be replaced with an 'd' or 'p' and the 'c' can be
        replaced with an 'o', so the following names are generated:
        dck, pck, bok, dok, pok.
        """
        chars_in_package_name = len(package_name)
        # if all characters that can be replaced are replaced, there
        # are too many combinations to compute if the package name
        # is long.
        # therefore, the number number of characters that is
        # replaced is limited if the package name gets longer
        if chars_in_package_name > 170:
            max_length = 1
        elif chars_in_package_name > 40:
            max_length = 2
        elif chars_in_package_name > 22:
            max_length = 3
        elif chars_in_package_name > 12:
            max_length = 4
        elif chars_in_package_name > 8:
            max_length = 5
        else:
            max_length = 256
        if len(package_name) > 0:
            self.replace_letters(package_name, generated_names, 0, 0, max_length)

    def replace_letters(
        self,
        package_name: str,
        generated_names: set[str],
        index: int,
        length: int,
        max_length: int,
    ):
        """
        Recursive function to generate permutations of the given package name.

        The character at the current index is replaced in one branch of the
        recursion and not in the other branch of the recursion.

        Therefore, at every index every character is either replaced or not.

        If at more than max_length indices the character has been replaced,
        recursion is stopped.
        """
        if index >= len(package_name) or length >= max_length:
            return

        # branch to not replace this character and continue
        self.replace_letters(
            package_name, generated_names, index + 1, length, max_length
        )

        letter_to_replace = package_name[index]
        letters_to_replace_with = ASCII_HOMOGRAPHS[letter_to_replace]

        # branch to replace this character and continue
        for letter in letters_to_replace_with:
            new_package_name = package_name[:index] + letter + package_name[index + 1 :]
            generated_names.add(new_package_name)
            self.replace_letters(
                new_package_name, generated_names, index + 1, length + 1, max_length
            )

    def load_file_to_list(self, path: Traversable) -> list[str]:
        """
        Loads a file into a list.

        Every line is turned into an entry in the list.
        Leading and trailing on a line are removed.
        """
        lines = []
        with path.open() as f:
            for line in f:
                lines.append(line.strip())
        return lines
