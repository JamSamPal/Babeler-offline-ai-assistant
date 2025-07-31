from assistant.python.semantics import triple


def test_to_dict():
    t = triple("cat", "has", "fur")
    assert t.to_dict() == {"subject": "cat", "predicate": "has", "object": "fur"}
