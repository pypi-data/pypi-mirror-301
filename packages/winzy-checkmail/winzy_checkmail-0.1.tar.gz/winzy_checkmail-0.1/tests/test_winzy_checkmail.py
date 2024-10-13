import pytest
import winzy_checkmail as w


def test_plugin(capsys):
    w.mail_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out
