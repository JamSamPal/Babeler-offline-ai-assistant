from assistant.python.command_parser import CommandParser
from assistant.python.semantics import Triple

command_parser = CommandParser()


#########################
# Personality queries
#########################
def test_gibberish():
    text = "what yaks bah"
    assert command_parser.parse(text) == ("unknown", None)


def test_set_name():
    text = "change your name to bob"
    assert command_parser.parse(text) == ("set_name_to", "bob")


def test_set_personality():
    text = "set your personality to sassy"
    assert command_parser.parse(text) == ("set_personality_to", "sassy")


#########################
# Question Queries
#########################


def test_is_an_x_a_type_of_y():
    text = "is an ant a type of insect"
    t = Triple(
        subject="ant",
        predicate="is a",
        obj="insect",
    )
    assert command_parser.parse(text)[0] == "is_a_x_a_type_of_y"
    assert command_parser.parse(text)[1].to_dict() == t.to_dict()


def test_is_a_x_a_type_of_y():
    text = "is a dog a type of mammal"
    t = Triple(
        subject="dog",
        predicate="is a",
        obj="mammal",
    )
    assert command_parser.parse(text)[0] == "is_a_x_a_type_of_y"
    assert command_parser.parse(text)[1].to_dict() == t.to_dict()


def test_does_a_x_have_y():
    text = "does a dog have fur"
    t = Triple(
        subject="dog",
        predicate="has",
        obj="fur",
    )
    assert command_parser.parse(text)[0] == "does_a_x_have_y"
    assert command_parser.parse(text)[1].to_dict() == t.to_dict()


def test_remember_x_y_z():
    text = "remember a spade is a spade"
    t = Triple(
        subject="spade",
        predicate="is a",
        obj="spade",
    )
    assert command_parser.parse(text)[0] == "remember_x_y_z"
    assert command_parser.parse(text)[1].to_dict() == t.to_dict()


def test_facts_about_x():
    text = "tell me some facts about dogs"
    t = Triple(
        subject="dog",
        predicate="",
        obj="",
    )

    assert command_parser.parse(text)[0] == "facts_about_x"
    assert command_parser.parse(text)[1].to_dict() == t.to_dict()


def test_what_things_are_x():
    text = "what things are fruits"
    t = Triple(
        subject="",
        predicate="is a",
        obj="fruit",
    )
    assert command_parser.parse(text)[0] == "what_things_are_x"
    assert command_parser.parse(text)[1].to_dict() == t.to_dict()


def test_what_things_have_x():
    text = "what things have windows"
    t = Triple(
        subject="",
        predicate="has",
        obj="windows",
    )
    assert command_parser.parse(text)[0] == "what_things_have_x"
    assert command_parser.parse(text)[1].to_dict() == t.to_dict()


def test_what_things_have_x():
    text = "what things have two legs"
    t = Triple(
        subject="",
        predicate="has",
        obj="two legs",
    )
    assert command_parser.parse(text)[0] == "what_things_have_x"
    assert command_parser.parse(text)[1].to_dict() == t.to_dict()


def test_who_x_y():
    text = "who discovered relativity"
    t = Triple(
        subject="",
        predicate="discovered",
        obj="relativity",
    )
    assert command_parser.parse(text)[0] == "who_x_y"
    assert command_parser.parse(text)[1].to_dict() == t.to_dict()
