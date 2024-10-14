import pytest
import winzy_laptop_battery as w


def test_plugin(capsys):
    w.battery_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out
