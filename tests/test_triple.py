from assistant.python.semantics import Triple
import pytest


def test_to_dict():
    t = Triple("cat", "has", "fur")
    assert t.to_dict() == {"subject": "cat", "predicate": "has", "object": "fur"}


def test_invalid_predicate_raises():
    with pytest.raises(ValueError):
        # Simulating an invalid predicate
        Triple(subject="cat", predicate="fnjaksgndfj", obj="fish")
