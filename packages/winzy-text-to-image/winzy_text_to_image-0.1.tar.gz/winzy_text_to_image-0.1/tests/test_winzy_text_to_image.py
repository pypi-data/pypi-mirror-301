import pytest
import winzy_text_to_image as w

from argparse import Namespace, ArgumentParser
from unittest.mock import patch, MagicMock

def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result, _ = parser.parse_known_args(['-p', 'hello'])
    assert result.prompt == "hello"
    assert result.seed is None
    assert result.width is None
    assert result.height is None
    assert result.model is None
    assert result.show == False
    assert result.output == "generated_image.jpg"


def test_plugin(capsys):
    w.txt2img_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out

