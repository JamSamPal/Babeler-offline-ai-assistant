from assistant.python.command_parser import CommandParser
from assistant.python.semantics import Triple, predicate_map

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


def test_what_has():
    text = "what things have windows"
    t = Triple(
        subject=None,
        predicate=predicate_map["have"],
        obj="windows",
    )
    assert command_parser.parse(text)[0] == "get_inverse_answer"
    assert command_parser.parse(text)[1].to_dict() == t.to_dict()
