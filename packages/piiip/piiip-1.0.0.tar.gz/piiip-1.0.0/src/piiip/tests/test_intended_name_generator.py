from __future__ import annotations

from piiip.intended_name_generator import (
    PATH_TO_TOKENS,
    PYPI_ALLOWED_CHARS,
    IntendedNameGenerator,
)


def test_load_file_to_list() -> None:
    tokens = IntendedNameGenerator().load_file_to_list(PATH_TO_TOKENS)
    assert len(tokens) == 4
    assert tokens[0] == "python"


def test_prefix_suffix_augmentation() -> None:
    generated_pckg_names: set[str] = set()
    IntendedNameGenerator().prefix_suffix_augmentation("test", generated_pckg_names)
    assert len(generated_pckg_names) > 15
    assert "pythontest" in generated_pckg_names
    assert "python-test" in generated_pckg_names
    assert "testpython" in generated_pckg_names
    assert "test-python" in generated_pckg_names


def test_swapped_character() -> None:
    generated_pckg_names: set[str] = set()
    name = "abcd"
    IntendedNameGenerator().swapped_character(name, generated_pckg_names)
    assert len(generated_pckg_names) == len(name) - 1


def test_swap_char_on_pos() -> None:
    # Normal operation
    assert IntendedNameGenerator().swap_char_on_pos("abcd", 0, 1) == "bacd"
    assert IntendedNameGenerator().swap_char_on_pos("abcd", 0, 2) == "cbad"
    assert IntendedNameGenerator().swap_char_on_pos("abcd", 3, -1) == "abdc"
    assert IntendedNameGenerator().swap_char_on_pos("abcd", 3, -2) == "adcb"
    assert IntendedNameGenerator().swap_char_on_pos("abcd", 0, 0) == "abcd"

    # Impossible cases
    assert IntendedNameGenerator().swap_char_on_pos("abcd", 0, -1) == "abcd"
    assert IntendedNameGenerator().swap_char_on_pos("abcd", 3, 1) == "abcd"
    assert IntendedNameGenerator().swap_char_on_pos("abcd", 0, 6) == "abcd"
    assert IntendedNameGenerator().swap_char_on_pos("abcd", 0, -20) == "abcd"


def test_substituted_character() -> None:
    generated_package_names: set[str] = set()
    name = "abcd"
    IntendedNameGenerator().substituted_character(name, generated_package_names)
    total_substituted_characters = len(PYPI_ALLOWED_CHARS) - 1
    assert len(generated_package_names) == total_substituted_characters * len(name)


def test_substitute_char() -> None:
    generated_names = IntendedNameGenerator().substitute_char(0, "abcd")
    assert "bbcd" in generated_names
    assert "cbcd" in generated_names
    assert "0bcd" in generated_names
    assert "-bcd" in generated_names
    assert "abcd" not in generated_names
    assert len(generated_names) == len(PYPI_ALLOWED_CHARS) - 1


def test_alternate_spelling() -> None:
    candidates = set()
    IntendedNameGenerator().alternate_spelling("colourama", candidates)
    assert "colorama" in candidates
    IntendedNameGenerator().alternate_spelling("colorama", candidates)
    assert "colourama" in candidates


def test_homographic_replacement() -> None:
    candidates = set()
    IntendedNameGenerator().homographic_replacement("bck", candidates)
    assert "dck" in candidates
    assert "pck" in candidates
    assert "bok" in candidates
    assert "dok" in candidates
    assert "pok" in candidates
