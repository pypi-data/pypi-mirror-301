import pytest
import winzy_webcam as w
import tempfile

from argparse import Namespace, ArgumentParser

def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_known_args()[0]
    assert result.path == tempfile.gettempdir()


def test_plugin(capsys):
    w.webcam_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out
