import pytest
import winzy_wc as w

from argparse import Namespace, ArgumentParser

def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_known_args(['hello'])[0]
    assert result.text == ["hello"]


def test_plugin(capsys):
    w.wc_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out

def test_wc():
    text = "Hello, how are you?\nI am doing well, thank you."
    expected_lines = 2
    expected_words = 10
    expected_chars = 46

    lines, words, characters = w.wc(text)
    assert lines == expected_lines
    assert words == expected_words
    assert characters == expected_chars