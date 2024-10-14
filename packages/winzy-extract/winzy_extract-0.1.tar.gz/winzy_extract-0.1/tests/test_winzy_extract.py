import pytest
import winzy_extract as w


def test_plugin(capsys):
    w.extract_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out


def test_extract():
    text= "Line 1\nLine 2\nLine 3\nLine 4\nLine 5"
    # Test extracting lines 2 to 4 from the temporary test file
    expected_output = "Line 2\nLine 3\nLine 4"
    assert w.extract_text_from_file(text, 2, 4) == expected_output