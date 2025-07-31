from assistant.python.command_parser import CommandParser

command_parser = CommandParser()


def test_gibberish():
    text = "what yaks bah"
    assert command_parser.parse(text) == ("unknown", None)


def test_greeting():
    text = ""
    assert command_parser.parse(text) == ("greeting", None)


def test_set_name():
    text = "change your name to bob"
    assert command_parser.parse(text) == ("set_name", "bob")


def test_set_personality():
    text = "set personality to sassy"
    assert command_parser.parse(text) == ("set_personality", "sassy")
