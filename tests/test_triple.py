from assistant.python.babbeler import Triple


def test_to_dict():
    t = Triple("cat", "has", "fur")
    assert t.to_dict() == {"subject": "cat", "predicate": "has", "object": "fur"}
