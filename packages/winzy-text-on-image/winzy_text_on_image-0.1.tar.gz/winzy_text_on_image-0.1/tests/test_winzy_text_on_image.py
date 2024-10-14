import pytest
import winzy_text_on_image as w

from argparse import Namespace, ArgumentParser

def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_known_args(['hello' , "-i", "imagepath.png"])[0]
    assert result.text == ["hello"]
    assert result.image_path == "imagepath.png"
    assert result.font_size == 24
    assert result.padding == 100


def test_plugin(capsys):
    w.txtonimg_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out
