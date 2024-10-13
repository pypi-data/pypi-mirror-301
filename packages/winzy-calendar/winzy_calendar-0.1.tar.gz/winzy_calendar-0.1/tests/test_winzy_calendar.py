import pytest
import winzy_calendar as w


def test_plugin(capsys):
    w.cal_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out
